# -*- coding: utf-8 -*-

import codecs
from xml.dom import minidom
from xml.sax.saxutils import escape
from collections import Counter

import sys


#Fonction utile

def top(ligne):
	return int(ligne.getAttribute('top'))

def left(ligne):
	return int(ligne.getAttribute('left'))

def height(ligne):
	return int(ligne.getAttribute('height'))

def width(ligne):
	return int(ligne.getAttribute('width'))

def bottom(ligne):
	return top(ligne) + height(ligne)

def right(ligne):
	return left(ligne) + width(ligne)

def font(ligne):
	return ligne.getAttribute('font')

def fontId(element):
	return element.getAttribute('id')

def fontSize(element):
	return element.getAttribute('size')

def fontFamily(element):
	return element.getAttribute('family')

def fontColor(element):
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
	"""Stocke les résultats du traitement"""

	def __init__(self, nbCol, file_in, option):
		"""Initialise la classe Resultat
		
		:param nbCol: Le nombre de colonne du document
		:type nbCol: int
		:param file_in: Chemin du fichier obtenu par pdftohtml
		:type file_in: str
		:param file_out: Chemin du fichier de sortie
		:type file_out: str

		"""

		self.nbCol = int(nbCol)
		self.file_in = file_in
		self.size_page = []
		self.resultat = []


		self.option = option;

	def go(self, file_out, file_out2):
		"""Lance le traitement, et écrit le résultat"""
		self.parsexml()
		self.ecrireResultat(file_out, file_out2)



	def parsexml(self):
		"""Analyse le fichier xml pour trouver les paragraphes"""

		page = []
		self.doc = minidom.parse(self.file_in)

		#Partie obligatoire
	
		police, taille, otherPolice = self.findPolice()

		self.preTraitement(police, taille, otherPolice) #On ne garde que l'utile et l'agréable

		colonne = self.findColonne() #On trouve les valeurs des left des deux colonnes
		alinea = self.findAlinea(colonne)
		interligne = self.findInterligne(colonne)


		#Partie optionnelle

		if self.option["trierPolice"]:
			self.garderPolicePrincipale(police)

		if self.option["trierMargeGauche"]:
			self.supprimerNonColonne(colonne, alinea)


		#self.ecrirePreTraitement()



		#Traitement		

		current = self.doc.childNodes[1].firstChild

		while current: #Prend en compte les sauts de ligne : c'est les #text
			page.append(current)
			self.size_page.append((height(current), width(current)))
			current = current.nextSibling

		for item in page:
			self.resultat.append(self.parsePage(item, colonne, alinea, interligne))

		
		self.virerHeaderFooterNumPage(self.resultat)



	def preTraitement(self, mainFont, taille, otherFont):
		"""Pré-traite le document pour supprimer ce qui ne nous intéresse pas
		Pré-traitement obligatoire		

		:param mainFont: La police usuelle
		:type mainFont: str
		:param taille: Taille usuelle d'une ligne
		:type taille: int
		:param otherFont: Tous les doublons de la police usuelle
		:type otherFont: List of str

		Garde seulement les lignes, par page
		Remplace tous les doublons de la police usuelle par la police usuelle

		Problème à régler :
			Ne garder que les paragraphes (pour le moment)
			Virer les noeuds de saut de ligne
			Réunir en une ligne les lignes spliter à cause des caractères spéciaux

		On considère :
			findColonne nous trouve les indices left des colonnes
		"""

		# 1) ne garde que les lignes de texte (balise.nodeName == 'text', doc.childNodes[1] == 'page')
		# Enlève donc les sauts de ligne (#text) les images et les fonts
		
		self.garderPage()
		self.garderTexte()
		self.replaceFont(mainFont, otherFont)
	
		# 2) réunir les lignes splitée
		# Suppositions : deux balises sont supposée de la même ligne si la différence des hauteurs < 10

		self.unsplitLine(mainFont)
	

	def garderPage(self):
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

	
	def replaceFont(self, mainFont, otherFont): #On considère garderTexte déjà exécuté
		current = self.doc.childNodes[1].firstChild

		while current:
			ligne = current.firstChild

			while ligne:
				if font(ligne) in otherFont:
					ligne.setAttribute("font", mainFont)

				ligne = ligne.nextSibling
		
			current = current.nextSibling



	def unsplitLine(self, mainFont):
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
		:returns: Liste de int : [top, left, right, bottom]

		Ne marche pas quand la ligne du pdf est divise en plusieurs lignes html (caractere speciaux). Exemple : page 2 "and l"
		D'où la nécessité du preTraitement

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

		idParagraphe = 0;

		for idPage, page in enumerate(self.resultat):
			document.addPage(idPage, idPage+1, float(self.size_page[idPage][0]), float(self.size_page[idPage][1]))
			h = document.pages[idPage].hauteur
			w = document.pages[idPage].largeur

			for paragraphe in page:
				p = document.addParagraphe(idParagraphe, idPage, paragraphe[4])
				p.position(100*paragraphe[0]/h, 100*paragraphe[1]/w, 100 - (100*paragraphe[2]/w), 100 - (100*paragraphe[3]/h))

				idParagraphe += 1



	def ecrirePreTraitement(self, file_tmp):
		fichier = codecs.open(file_tmp, 'w', "utf-8")
		fichier.write(self.doc.toprettyxml())
		fichier.close()



	def ecrireResultat(self, file_out, file_out2):
		"""Ecrit le resultat du traitement, dans un format utilisable par l'interface web"""

		fichier = codecs.open(file_out, "w", "utf-8")
		fichier2 = codecs.open(file_out2, "w", "utf-8")

		fichier.write('<?xml version="1.0" encoding="UTF-8"?>\n<pdf>\n')
		fichier2.write('<?xml version="1.0" encoding="UTF-8"?>\n<pdf nbParagraphe="' + str(sum(len(x) for x in self.resultat)) + '" >\n')

		id_ = 0

		for i, page in enumerate(self.resultat):
			fichier.write('\t<page numero="' + str(i+1) + '">\n')

			h = float(self.size_page[i][0])
			w = float(self.size_page[i][1])

			for paragraphe in page:
				fichier.write('\t\t<texte id="' + str(id_) + '" time="0.0_0.0" style="top:' + str(100*paragraphe[0] / h) + '%; left:' + str(100*paragraphe[1]/w) + '%; right:' + str(100 - (100*paragraphe[2]/w)) + '%; bottom:' + str(100 - (100*paragraphe[3]/h)) + '%;"/>\n')
				fichier2.write('\t<paragraphe id="' + str(id_) + '" begin="0.0" end="0.0">' + escape(paragraphe[4]) + '</paragraphe>\n')
				id_ = id_ + 1

			fichier.write('\t</page>\n')

		fichier.write('</pdf>')
		fichier2.write('</pdf>')
		fichier.close()






#Programme lui même
if __name__ == '__main__':
	if len(sys.argv) != 3 and len(sys.argv) != 8:
		print "Syntax: %s nbColonne input_file [alinea interligne changementColonne trierPolice trierMargeGauche]" % sys.argv[0]
		sys.exit(1)

	nbColonne = int(sys.argv[1])
	file_in = sys.argv[2]
	file_out = "conf.xml"
	file_out2 = "res.xml"

	if len(sys.argv) == 8:
		option = {"alinea" : not (sys.argv[3] == "False"), "interligne" : not (sys.argv[4] == "False"), "changementColonne" : not (sys.argv[5] == "False"), "trierPolice" : not (sys.argv[6] == "False"), "trierMargeGauche" : not (sys.argv[7] == "False")};
	
	else:
		option = {"alinea" : True, "interligne" : True, "changementColonne" : True, "trierPolice" : False, "trierMargeGauche" : False};

	print option
 
	res = TraitementPdf(nbColonne, file_in, option)
	res.go(file_out, file_out2)

