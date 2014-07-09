# -*- coding: utf-8 -*-

import codecs
from xml.dom import minidom
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



#Classe Resultat

class Resultat:
	"""Stocke les résultats du traitement"""

	def __init__(self, nbCol, file_in, file_out="conf.xml"):
		"""Initialise la classe Resultat
		
		:param nbCol: Le nombre de colonne du document
		:type nbCol: int
		:param file_in: Chemin du fichier obtenu par pdftohtml
		:type file_in: str
		:param file_out: Chemin du fichier de sortie
		:type file_out: str

		"""

		self.nbCol = nbCol
		self.file_in = file_in
		self.file_out = file_out
		self.size_page = []
		self.resultat = []

	def go(self):
		"""Lance le traitement, et écrit le résultat"""
		self.parsexml()
		self.ecrireResultat()


	def parsexml(self):
		"""Analyse le fichier xml pour trouver les paragraphes"""

		page = []
		doc = minidom.parse(self.file_in)
	
		police, taille = self.findPolice(doc)

		self.preTraitement(doc, police, taille) #On ne garde que l'utile et l'agréable

		colonne = self.findColonne(doc) #On trouve les valeurs des left des deux colonnes

		alinea = self.findAlinea(doc, colonne)

		interligne = self.findInterligne(doc, colonne)

		self.garderPolicePrincipale(doc, police)

		fichier = codecs.open("xml", 'w', "utf-8")
		fichier.write(doc.toprettyxml())

		fichier.close()

		current = doc.childNodes[1].firstChild

		while current: #Prend en compte les sauts de ligne : c'est les #text
			page.append(current)
			self.size_page.append((current.getAttribute('height'), current.getAttribute('width')))
			current = current.nextSibling

		for item in page:
			self.resultat.append(self.parsePage(item, colonne, alinea, interligne))



	def preTraitement(self, doc, police, taille):
		"""Pré-traite le document pour supprimer ce qui ne nous intéresse pas

		:param doc: Le document
		:type doc: xml
		:param police: La police usuelle
		:type police: str
		:param taille: Taille usuelle d'une ligne
		:type taille: int

		Garde seulement les lignes, par page
		Problème à régler :
			Ne garder que les paragraphes (pour le moment)
			Virer les noeuds de saut de ligne
			Réunir en une ligne les lignes spliter à cause des caractères spéciaux

		On considère :
			findColonne nous trouve les indices left des colonnes
		"""

		# 1) ne garde que les lignes de texte (balise.nodeName == 'text', doc.childNodes[1] == 'page')
		# Enlève donc les sauts de ligne (#text) les images et les fonts

		current = doc.childNodes[1].firstChild

		while current:
			if current.nodeName == 'page':
				ligne = current.firstChild
	
				while ligne:
					if ligne.nodeName != 'text':
						nextLigne = ligne.nextSibling
						try:
							current.removeChild(ligne)
						except ValueError: print 'failed'
						ligne = nextLigne
					else:
						ligne = ligne.nextSibling
			
				current = current.nextSibling
			else:
				nextCurrent = current.nextSibling
				try:
					doc.childNodes[1].removeChild(current)
				except ValueError: print 'failed'
				current = nextCurrent

		current = doc.childNodes[1].firstChild

	
		# 2) réunir les lignes splitée
		# Suppositions : deux balises sont supposée de la même ligne si la différence des hauteurs < 10

		current = doc.childNodes[1].firstChild

		cpt = 0

		while current:
			if current.nodeName == 'page':
				ligne = current.firstChild
	
				while ligne:
					if ligne.nodeName == 'text':
						nextLigne = ligne.nextSibling

						while nextLigne and nextLigne.nodeName == 'text' and top(nextLigne) < bottom(ligne) and top(ligne) < bottom(nextLigne):
							ligne.setAttribute('top', str(min(top(ligne), top(nextLigne))))
							#left : on garde celui de la première ligne

							ligne.setAttribute('height', str(taille))

							ligne.setAttribute('width', str(width(ligne) + width(nextLigne)))

							if font(nextLigne) == police:
								ligne.setAttribute('font', police)

							try:
								current.removeChild(nextLigne)
							except ValueError: print 'failed'

							nextLigne = ligne.nextSibling

						ligne = nextLigne
					else:
						ligne = ligne.nextSibling
			
			current = current.nextSibling

		current = doc.childNodes[1].firstChild
	
	

	def findPolice(self, doc):
		"""Trouve la police principale du document
		
		:param doc: Le document
		:type doc: xml
		:returns: (str, str) - La police principale et la taille d'une ligne
	
		On suppose que la police principale est celle du texte lui -même, on pourra donc virer le reste
		
		"""
	
		font = Counter()

		current = doc.childNodes[1].firstChild

		while current:
			if current.nodeName == 'page':
				ligne = current.firstChild

				while ligne:
					if ligne.nodeName == 'text':
						font[(ligne.getAttribute('font'), height(ligne))] += 1
				
					ligne = ligne.nextSibling
			
			current = current.nextSibling

		return font.most_common(1)[0][0]


	def garderPolicePrincipale(self, doc, font):
		"""Ne garde que la police principale du document, enlève les autres lignes

		:param doc: Le document
		:type doc: xml
		:param font: La police principale
		:type font: str

		"""
		
		current = doc.childNodes[1].firstChild

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

	
	def findColonne(self, doc):
		"""Trouver les coordonnées left des paragraphes pour chaque colonne
		
		:param doc: Le document
		:type doc: xml
		:returns: Tuple de nbCol int :  Les coordonnés left des nbCol colonnes

		Suppose que la coordonnee d'une colonne est toujours la meme, et est celle qui revient le plus souvent
		Permet de virer les contenus autres (intro, num de page, tableau etc etc)

		"""

		cnt = Counter()

		current = doc.childNodes[1].firstChild

		while current:
			if current.nodeName == 'page':
				ligne = current.firstChild

				while ligne:
					if ligne.nodeName == 'text':
						cnt[left(ligne)] += 1
				
					ligne = ligne.nextSibling
			
			current = current.nextSibling

		nmax = cnt.most_common(self.nbCol)

		return map(lambda x: x[0], nmax)


	def findAlinea(self, doc, colonne):
		"""Trouve les valeurs left des alinéa de chaque colonne

		:param doc: Le document
		:type doc: xml
		:param colonne: Les valeurs left des colonnes
		:type colonne: Tuple de nbCol int
		:returns: Tuple de int : les alinéas de chaque colonne

		On considère un paragraphe comme au moins trois ligne avec la bonne valeur left

		"""

		alinea = []
		for i in range(self.nbCol):
			alinea.append(Counter())

		current = doc.childNodes[1].firstChild

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


	def findInterligne(self, doc, colonne):
		"""Trouve l'interligne usuel entre deux lignes de texte

		:param doc: Le document
		:type doc: xml
		:param colonne: Les valeurs left des colonnes
		:type colonne: Tuple de nbCol int
		:returns: int : La valeur de l'interligne

		"""
		
		interligne = Counter()

		current = doc.childNodes[1].firstChild

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
			if ligne.nodeName == 'text' :
				if left(ligne) in alinea or (top(ligne) - lastBottom) > interligne + margeErreur or top(ligne) < lastBottom:
					if len(paragraphe) > 0 :
						paragraphe[-1][3] = lastBottom
				
					paragraphe.append([top(ligne), left(ligne), right(ligne), 0])
				elif left(ligne) in colonne:
					if len(paragraphe) > 0:
						if paragraphe[-1][1] > left(ligne):
							paragraphe[-1][1] = left(ligne)
						if paragraphe[-1][2] < right(ligne):
							paragraphe[-1][2] = right(ligne)
	
				lastBottom = bottom(ligne)
			ligne = ligne.nextSibling
	
		#print paragraphe

		return paragraphe


	def ecrireResultat(self):
		"""Ecrit le resultat du traitement, dans un format utilisable par l'interface web"""

		fichier = open(self.file_out, "w")

		fichier.write('<?xml version="1.0" encoding="UTF-8"?>\n<pdf>\n')

		id_ = 0

		for i, page in enumerate(self.resultat):
			fichier.write('\t<page numero="' + str(i+1) + '">\n')

			h = float(self.size_page[i][0])
			w = float(self.size_page[i][1])

			for paragraphe in page:
				fichier.write('\t\t<texte id="' + str(id_) + '" time="0.0_0.0" style="top:' + str(100*paragraphe[0] / h) + '%; left:' + str(100*paragraphe[1]/w) + '%; right:' + str(100 - (100*paragraphe[2]/w)) + '%; bottom:' + str(100 - (100*paragraphe[3]/h)) + '%;"/>\n')
				id_ = id_ + 1

			fichier.write('\t</page>\n');

		fichier.write('</pdf>');
		fichier.close()

if len(sys.argv) != 2:
	print "Erreur, argument manquant"
	sys.exit(1)

#nbColonne = sys.argv[1]

res = Resultat(int(sys.argv[1]), "cmd.xml", "conf.xml") 
res.go()
