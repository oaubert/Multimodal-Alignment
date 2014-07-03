# -*- coding: utf-8 -*-

import codecs
from xml.dom import minidom
from xml.sax.saxutils import escape
from collections import Counter

import sys


#Fonction utile

def top(ligne):
	"""Renvoie la coordonnée en y du haut d'une ligne"""
	return int(ligne.getAttribute('top'))

def left(ligne):
	"""Renvoie la coordonnée en x de la limite gauche d'une ligne"""
	return int(ligne.getAttribute('left'))

def height(ligne):
	"""Renvoie la hauteur d'une ligne"""
	return int(ligne.getAttribute('height'))

def width(ligne):
	"""Renvoie la largeur d'une ligne"""
	return int(ligne.getAttribute('width'))

def bottom(ligne):
	"""Calcule et renvoie la coordonnée en y du bas d'une ligne"""
	return top(ligne) + height(ligne)

def right(ligne):
	"""Calcule et renvoie la coordonnée en x de la limite droite d'une ligne"""
	return left(ligne) + width(ligne)

def font(ligne):
	"""Renvoie la police d'une ligne"""
	return ligne.getAttribute('font')

def fontId(element):
	"""Renvoie l'id d'une police"""
	return element.getAttribute('id')

def fontSize(element):
	"""Renvoie la taille d'une police"""
	return element.getAttribute('size')

def fontFamily(element):
	"""Renvoie la famille d'une police"""
	return element.getAttribute('family')

def fontColor(element):
	"""Renvoie la couleur d'une police"""
	return element.getAttribute('color')

def getText(node):
	child = node.childNodes
	texte = ""

	for e in child:
		if e.nodeType != e.TEXT_NODE:
			texte += getText(e)
		if e.nodeValue != None:
			texte += e.nodeValue

	return texte

def setText(doc, node, texte):
	child = node.firstChild

	while child:
		nextChild = child.nextSibling
		node.removeChild(child)
		child = nextChild

	text = doc.createTextNode(texte)

	node.appendChild(text)



#Classe Resultat

class TraitementPdf:
	"""Traite un fichier xml de l'article pour en extraire les informations nécessaires"""

	def __init__(self, nbCol, file_in, option):
		"""Initialise la classe Resultat
		
		:param nbCol: Le nombre de colonne du document
		:type nbCol: int
		:param file_in: Chemin du fichier obtenu par pdftohtml
		:type file_in: str
		:param option: Les options de traitement. Ex : option = {"alinea" : True, "interligne" : True, "changementColonne" : True, "trierPolice" : False, "trierMargeGauche" : False}
		:type option: dict

		"""

		self.nbCol = int(nbCol)
		self.file_in = file_in
		self.size_page = []
		self.resultat = []


		self.option = option;


	def parsexml(self):
		"""Analyse le fichier xml pour trouver les paragraphes

		L'analyse se divise en plusieurs étapes.
		D'abord un pré-traitement obligatoire :
			-Détermination de la police standard du texte
			-Pré-traitement sur le texte
			-Détermination des valeurs de la marge à droite et de l'alinéa du texte, ainsi que de l'interligne
		Ensuite un pré-traitement optionnel (décidé en fonction des options):
			-Suppression des lignes avec polices non standard
			-Suppression des lignes avec un marge non standard
		Le traitement, qui liste les pages avec leur hauteur et leur largent, puis qui parse chaque page grâce aux informations du pré-traitement
		Puis un post-traitement, qui repasse sur les paragraphes trouvé pour supprimer des paragraphes non utile (hearder, footer, quelques légendes)
		"""

		page = []
		self.doc = minidom.parse(self.file_in)

		#Partie obligatoire
	
		police, taille, otherPolice = self.findPolice()

		self.preTraitement(police, otherPolice) #On ne garde que l'utile et l'agréable

		colonne = self.findColonne() #On trouve les valeurs des left des deux colonnes
		alinea = self.findAlinea(colonne)
		interligne = self.findInterligne(colonne)


		#Partie optionnelle

		if self.option["trierPolice"]:
			self.garderPolicePrincipale(police)

		if self.option["trierMargeGauche"]:
			self.supprimerNonColonne(colonne, alinea)


		#Traitement		

		current = self.doc.childNodes[1].firstChild

		while current: #Prend en compte les sauts de ligne : c'est les #text
			page.append(current)
			self.size_page.append((height(current), width(current)))
			current = current.nextSibling

		for item in page:
			self.resultat.append(self.parsePage(item, colonne, alinea, interligne))

		
		#Post-traitement
		self.virerHeaderFooterNumPage(self.resultat)



	def preTraitement(self, mainFont, otherFont):
		"""Pré-traite le document pour supprimer ce qui ne nous intéresse pas
		Pré-traitement obligatoire		

		:param mainFont: La police usuelle
		:type mainFont: str
		:param otherFont: Tous les doublons de la police usuelle
		:type otherFont: List of str

		1) ne garde que les lignes de texte (balise.nodeName == 'text', doc.childNodes[1] == 'page')
		Enlève donc les sauts de ligne (#text) les images et les fonts. Remplace les doublons de la police usuelle par la police usuelle

		2) réunir les lignes splitée
		Suppositions : deux balises sont supposée de la même ligne si la différence des hauteurs < 10
		"""

		# 1) 
		self.garderPage()
		self.garderTexte()
		self.replaceFont(mainFont, otherFont)
	
		# 2)
		self.unsplitLine(mainFont)
	

	def garderPage(self):
		"""Ne garde que les noeuds des pages"""

		current = self.doc.childNodes[1].firstChild

		while current:
			if current.nodeName != 'page':
				nextCurrent = current.nextSibling
				try:
					self.doc.childNodes[1].removeChild(current)
					current.unlink()
				except ValueError: print 'Failed removing not page node'
				current = nextCurrent
			else:
				current = current.nextSibling


	def garderTexte(self):
		"""Pour chaque page, ne garde que les noeuds de texte"""

		current = self.doc.childNodes[1].firstChild
	
		while current:
			ligne = current.firstChild

			while ligne:
				if ligne.nodeName != 'text':
					nextLigne = ligne.nextSibling
					try:
						current.removeChild(ligne)
						ligne.unlink()
					except ValueError: print 'Failed removing line'
					ligne = nextLigne
				else:
					ligne = ligne.nextSibling
		
			current = current.nextSibling

	
	def replaceFont(self, mainFont, otherFont): 
		"""Remplace les doublons de polices par la police usuelle

		:param mainFont: La police usuelle
		:type mainFont: str
		:param otherFont: Tous les doublons de la police usuelle
		:type otherFont: List of str

		On considère garderTexte déjà exécuté
		"""

		current = self.doc.childNodes[1].firstChild

		while current:
			ligne = current.firstChild

			while ligne:
				if font(ligne) in otherFont:
					ligne.setAttribute("font", mainFont)

				ligne = ligne.nextSibling
		
			current = current.nextSibling



	def unsplitLine(self, mainFont):
		"""Réuni des lignes séparées à cause de caractères spéciaux

		L'extracteur de pdf définit une ligne comme un ensemble sur la "même ligne", avec une même police et une même taille. Ainsi, si il y a un changement de police sur une même ligne, on aura deux lignes (ou plus) dans le xml. Il faut donc réunir ces lignes, et mettre leurs coordonnées en commun.
		On définit deux lignes à réunir si la différence des hauteurs est inférieur à 10
		"""

		current = self.doc.childNodes[1].firstChild

		while current:
			ligne = current.firstChild
	
			while ligne:
				nextLigne = ligne.nextSibling

				while nextLigne and top(nextLigne) < bottom(ligne) and top(ligne) < bottom(nextLigne):
					newTop = min(top(ligne), top(nextLigne))
					newBottom = max(bottom(ligne), bottom(nextLigne))
					newHeight =  newBottom - newTop

					ligne.setAttribute('top', str(newTop))
					#left : on garde celui de la première ligne

					ligne.setAttribute('height', str(newHeight))

					#espace = left(nextLigne) - (left(ligne) + width(ligne))
					#ligne.setAttribute('width', str(width(ligne) + width(nextLigne) + espace))
					#Simplifiable en :
					ligne.setAttribute('width', str(left(nextLigne) - left(ligne) + width(nextLigne)))


					texte1 = getText(ligne)
					texte2 = getText(nextLigne)

					if texte1 == None:
						texte1 = ""
					else:
						texte1 = texte1.replace("\n", " ")
						texte1 = texte1.replace("\r", " ")

					if texte2 == None:
						texte2 = ""
					else:
						texte2 = texte2.replace("\n", " ")
						texte2 = texte2.replace("\r", " ")

					setText(self.doc, ligne, texte1 + ' ' + texte2)

					if font(nextLigne) == mainFont:
						ligne.setAttribute('font', mainFont)

					try:
						current.removeChild(nextLigne)
						nextLigne.unlink()
					except ValueError: print 'failed'

					nextLigne = ligne.nextSibling

				ligne = nextLigne
		
			current = current.nextSibling



	def findPolice(self):
		"""Trouve la police principale du document
		
		:returns: (str, str, List of str) - La police principale, la taille d'une ligne et la liste des doublons de la police principale
	
		On suppose que la police principale est celle du texte lui -même, on pourra donc virer le reste
		Problème : il y a parfois plusieurs fois la même police (même size, même family, même color) pour différent numéro
			Ces doublons sont stocké dans otherPolice
		
		"""

		allFont = []
		res = []
	
		font = Counter()

		current = self.doc.childNodes[1].firstChild

		while current:
			if current.nodeName == 'page':
				ligne = current.firstChild

				while ligne:
					if ligne.nodeName == 'fontspec':
						allFont.append(ligne) #Trouve toutes les polices
					if ligne.nodeName == 'text':
						font[(ligne.getAttribute('font'), height(ligne))] += 1 #Trouve la police principale
				
					ligne = ligne.nextSibling
			
			current = current.nextSibling

		res = font.most_common(1)[0][0]

		otherPolice = []

		policePrincipale = [element for element in allFont if element.getAttribute('id') == res[0]][0]

		otherPolice = [fontId(e) for e in allFont if fontSize(e) == fontSize(policePrincipale) and fontFamily(e) == fontFamily(policePrincipale) and fontColor(e) == fontColor(policePrincipale) and fontId(e) != fontId(policePrincipale)]

		return res[0], res[1], otherPolice


	def findColonne(self):
		"""Trouver les coordonnées left des paragraphes pour chaque colonne
		
		:returns: Tuple de nbCol int :  Les coordonnés left des nbCol colonnes

		Suppose que la coordonnee d'une colonne est toujours la meme, et est celle qui revient le plus souvent
		Permet de virer les contenus autres (intro, num de page, tableau etc etc)

		"""

		cnt = Counter()

		current = self.doc.childNodes[1].firstChild

		while current:
			ligne = current.firstChild

			while ligne:
				if ligne.nodeName == 'text':
					cnt[left(ligne)] += 1
				
				ligne = ligne.nextSibling
		
			current = current.nextSibling


		print cnt

		somme = sum(cnt.values())

		print "Sum : " + str(somme)

		allmax = cnt.most_common()

		cpt = 1

		marge = 10./100. * somme
		
		print marge

		while allmax[cpt-1][1] - allmax[cpt][1] < marge:
			cpt += 1

		
		print cpt	

		nmax = cnt.most_common(self.nbCol)

		return map(lambda x: x[0], nmax)


	def findAlinea(self, colonne):
		"""Trouve les valeurs left des alinéa de chaque colonne

		:param colonne: Les valeurs left des colonnes
		:type colonne: Tuple de nbCol int
		:returns: Tuple de int : les alinéas de chaque colonne

		On considère un paragraphe comme au moins trois ligne avec la bonne valeur left

		"""

		alinea = []
		for i in range(self.nbCol):
			alinea.append(Counter())

		current = self.doc.childNodes[1].firstChild

		while current:
			ligne = current.firstChild
			ligne2 = ligne.nextSibling
			ligne3 = ligne2.nextSibling
			ligne4 = ligne3.nextSibling

			while ligne4:
				if left(ligne) not in colonne:
					for i, val in enumerate(colonne):
						if left(ligne2) == val and left(ligne3) == val and left(ligne4) == val:
							alinea[i][left(ligne)] += 1
							break


				ligne = ligne2
				ligne2 = ligne3
				ligne3 = ligne4
				ligne4 = ligne4.nextSibling

			current = current.nextSibling
				
		return map(lambda x: x.most_common(1)[0][0], alinea)


	def findInterligne(self, colonne):
		"""Trouve l'interligne usuel entre deux lignes de texte

		:param colonne: Les valeurs left des colonnes
		:type colonne: Tuple de nbCol int
		:returns: int : La valeur de l'interligne

		"""
		
		interligne = Counter()

		current = self.doc.childNodes[1].firstChild

		while current:
			ligne = current.firstChild
			ligne2 = ligne.nextSibling

			while ligne2:
				if left(ligne) in colonne and left(ligne2) in colonne:
					interligne[top(ligne2) - bottom(ligne)] += 1

				ligne = ligne2
				ligne2 = ligne2.nextSibling

			current = current.nextSibling
				
		return interligne.most_common(1)[0][0]





	def garderPolicePrincipale(self, font):
		"""Ne garde que la police principale du document, enlève les autres lignes

		:param font: La police principale
		:type font: str

		"""
		
		current = self.doc.childNodes[1].firstChild

		while current:
			if current.nodeName == 'page':
				ligne = current.firstChild

				while ligne:
					if ligne.getAttribute('font') != font:
						nextLigne = ligne.nextSibling

						try:
							current.removeChild(ligne)
						except ValueError: print 'failed'
						
						ligne = nextLigne
					else:
						ligne = ligne.nextSibling
			
			current = current.nextSibling

	
	


	def supprimerNonColonne(self, colonne, alinea):
		"""Supprime toutes les lignes qui n'ont pas une marge à gauche de paragraphe

		:param colonne: Les valeurs left des colonnes
		:type colonne: Tuple de nbCol int
		:param alinea: Les valeurs left des alineas
		:type alinea: Tuple de nbCol in

		Problème : Supprime trop de choses, par ex Abstract, Liste à puce (ou numéroté) etc etc

		"""
		
		current = self.doc.childNodes[1].firstChild

		while current:
			ligne = current.firstChild

			while ligne:
				if left(ligne) not in colonne and left(ligne) not in alinea:
					nextLigne = ligne.nextSibling

					try:
						current.removeChild(ligne)
						ligne.unlink()
					except ValueError: print 'failed'
					
					ligne = nextLigne
				else:
					ligne = ligne.nextSibling

			current = current.nextSibling
				

	def virerHeaderFooterNumPage(self, paragraphe):
		"""Supprimer les hearders, footers et quelques légendes

		:param paragraphe : le résultat des traitements
		:type paragraphe : dict

		On supprime les paragraphes composé seulement de numéro ou trop court
		"""

		paragrapheCourt = {}
		toDelete = []

		suite = 0

		for i, page in enumerate(paragraphe):
			suite = 0
			for j,p in enumerate(page):
				if len(p[4]) < 100:				
					if p[4].isnumeric():
						toDelete.append((i,j))

					if p[4] not in paragrapheCourt:
						paragrapheCourt[p[4]] = ([(i,j)],1)
					else:
						l,c = paragrapheCourt[p[4]]
						l.append((i,j))
						paragrapheCourt[p[4]] = (l,c+1)

					if len(p[4].split()) == 1: #Un seul mot
						suite += 1
					else:
						if suite > 3:
							toDelete.extend(zip([i]*(suite), range(j-suite, j)))

						suite = 0


		for k,v in paragrapheCourt.iteritems():
			if v[1] > len(paragraphe) / 3:
				for p in v[0]:
					if p not in toDelete:
						toDelete.append(p)

		toDelete.sort()
		toDelete.reverse()

		for i,j in toDelete:
			paragraphe[i].pop(j)

		
	def parsePage(self, page, colonne, alinea, interligne):
		"""Pour chaque page, trouve les paragraphes dans la page

		:param page: L'objet xml pour chaque page
		:type page: Tableau d'objet xml
		:param colonne: Le tuple des coordonnées left des colonnes
		:type colonne: Tuple de nbCol int
		:param alinea: Le tuple des coordonnées left des alinéa de chaque colonne
		:type alinea: Tuple de nbCol int
		:param interligne: L'interligne usuelle
		:type interligne: int
		:returns: Liste de int : [top, left, right, bottom]

		Chaque paragraphe peut être défini de plusieurs manières :
			-Un nouvel alinéa
			-Une interligne trop grande
			-Un changement de colonne
		On peut choisir d'appliquer ces choix grâce aux options "alinea", "interligne", et "changementColonne"

		Les paragraphes sont définis par page, ainsi un paragraphe s'étalant sur deux pages sera coupé.
		
		On définit une marge d'erreur pour travailler sur les différences de hauteur (interligne ou changement de colonne).
		"""

		paragraphe = []
		ligne = page.firstChild

		lastBottom = 0
		margeErreur = 3

		while ligne:
			if (self.option["alinea"] and left(ligne) in alinea) or (self.option["interligne"] and (top(ligne) - lastBottom) > interligne + margeErreur) or (self.option["changementColonne"] and top(ligne) - lastBottom < 0 - margeErreur) :
				if len(paragraphe) > 0 :
					paragraphe[-1][3] = lastBottom
	
					
				paragraphe.append([top(ligne), left(ligne), right(ligne), 0, getText(ligne)])
				
			#elif left(ligne) in colonne:
			else:
				if len(paragraphe) > 0:
					if paragraphe[-1][1] > left(ligne):
						paragraphe[-1][1] = left(ligne)
					if paragraphe[-1][2] < right(ligne):
						paragraphe[-1][2] = right(ligne)

					if paragraphe[-1][4][-1] == '-':
						paragraphe[-1][4] = paragraphe[-1][4][:-1]
						paragraphe[-1][4] += getText(ligne)
					else:
						paragraphe[-1][4] += " " + getText(ligne)


			lastBottom = bottom(ligne)
			ligne = ligne.nextSibling

		if len(paragraphe) > 0 :
			paragraphe[-1][3] = lastBottom

		return paragraphe


	def formatResultat(self, document):
		"""Prend un objet Documents (voir segment.py) et y ajoute tous les paragraphes et les pages trouvés"""

		idParagraphe = 0;

		for idPage, page in enumerate(self.resultat):
			document.addPage(idPage, idPage+1, float(self.size_page[idPage][0]), float(self.size_page[idPage][1]))
			h = document.pages[idPage].hauteur
			w = document.pages[idPage].largeur

			for paragraphe in page:
				p = document.addParagraphe(idParagraphe, idPage, paragraphe[4])
				p.position(100*paragraphe[0]/h, 100*paragraphe[1]/w, 100 - (100*paragraphe[2]/w), 100 - (100*paragraphe[3]/h))

				idParagraphe += 1


	def ecrireResultat(self, file_out):
		"""Ecrit le resultat du traitement, dans un format utilisable par l'interface web"""

		fichier = codecs.open(file_out, "w", "utf-8")

		fichier.write('<?xml version="1.0" encoding="UTF-8"?>\n<pdf>\n')

		id_ = 0

		for i, page in enumerate(self.resultat):
			fichier.write('\t<page numero="' + str(i+1) + '">\n')

			h = float(self.size_page[i][0])
			w = float(self.size_page[i][1])

			for paragraphe in page:
				fichier.write('\t\t<texte id="' + str(id_) + '" time="0.0_0.0" style="top:' + str(100*paragraphe[0] / h) + '%; left:' + str(100*paragraphe[1]/w) + '%; right:' + str(100 - (100*paragraphe[2]/w)) + '%; bottom:' + str(100 - (100*paragraphe[3]/h)) + '%;"/>\n')
				id_ = id_ + 1

			fichier.write('\t</page>\n')

		fichier.write('</pdf>')
		fichier.close()






#Programme lui même
if __name__ == '__main__':
	if len(sys.argv) != 3 and len(sys.argv) != 8:
		print "Syntax: %s nbColonne input_file [alinea interligne changementColonne trierPolice trierMargeGauche]" % sys.argv[0]
		sys.exit(1)

	nbColonne = int(sys.argv[1])
	file_in = sys.argv[2]

	if len(sys.argv) == 8:
		option = {"alinea" : not (sys.argv[3] == "False"), "interligne" : not (sys.argv[4] == "False"), "changementColonne" : not (sys.argv[5] == "False"), "trierPolice" : not (sys.argv[6] == "False"), "trierMargeGauche" : not (sys.argv[7] == "False")};
	
	else:
		option = {"alinea" : True, "interligne" : True, "changementColonne" : True, "trierPolice" : False, "trierMargeGauche" : False};

 
	res = TraitementPdf(nbColonne, file_in, option)
	res.parsexml()
	res.ecrireResultat("res.xml")

