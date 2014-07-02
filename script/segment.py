# -*- coding: utf-8 -*-
"""
Définit les classes nécessaires pour contenir les informations obtenus par les différents scripts
On a 7 classes :
	-Documents : Contient tous les informations (speech, paragraphe, page et liens)
	-Segment : Définit les fonctions communes aux speechs et aux paragraphes
	-Speech : Définit un speech
	-Paragraphe : Définit un paragraphe
	-Page : Définit une page (de l'article)
	-Link : Définit un lien entre un speech et un paragraphe
	-Word : Définit un mot (dans un paragraphe ou un speech)
On instancie pour le module un tokenizer, appelé lem.
"""

import codecs
import stem

lem = stem.LemmaTokenizer()

class Documents:
	"""Contient toutes les informations"""

	def __init__(self):
		"""Initialise les structures de données

		Un objet Documents va contenir des informations sur les speechs, les paragraphes, les pages de l'article et les liens entre speechs et paragraphes.
		Pour cela, il fera appel aux autres classes de ce module.
		"""
		self.speechs = {}
		self.paragraphes = {}
		self.pages = {}
		self.links = {}

	def infoDureeSpeech(self, duree):
		"""Spécifie la durée totale de la vidéo"""
		self.dureeSpeech = duree

	def defineVocabulary(self, vocabulary, stop_words):
		"""Définit le vocabulaire des documents

		Le vocabulaire est l'ensemble des mots "significatifs" (c'est-à-dire en supprimant la ponctuation et les stop-words) présents dans l'ensemble des speechs et des paragraphes.
		Les stop-words sont les mots courants, et donc peu significatifs.
		"""
		self.vocabulary = vocabulary
		self.stop_words = stop_words

		#Définit ce vocabulaire pour chaque paragraphe
		for paragraphe in self.paragraphes.values():
			paragraphe.defineVocabulary(self.vocabulary, self.stop_words)

		#Ainsi que pour chaque speech
		for speech in self.speechs.values():
			speech.defineVocabulary(self.vocabulary, self.stop_words)

	def addSpeech(self, idSpeech, idSlide, doc):
		"""Ajoute un speech dans les documents
		
		On précise son id, l'id de son slide, ainsi son texte
		"""

		self.speechs[idSpeech] = Speech(idSpeech, idSlide, doc)
		return self.speechs[idSpeech]

	def addPage(self, idPage, numero, hauteur, largeur):
		"""Ajoute une page dans les documents

		On précise son id, son numéro (l'id commence à 0, le numéro pas forcément), sa hauteur et sa largeur
		"""

		self.pages[idPage] = Page(idPage, numero, hauteur, largeur)
		return self.pages[idPage]

	def addParagraphe(self, idParagraphe, idPage, doc):
		"""Ajoute un paragraphe dans les documents

		On précise son id, l'id de sa page, et son texte
		"""

		self.paragraphes[idParagraphe] = Paragraphe(idParagraphe, idPage, doc)
		return self.paragraphes[idParagraphe]

	def addLink(self, idSpeech, idParagraphe):
		"""Ajoute un lien dans les documents

		On précise les id du speech et du paragraphe liés
		"""

		if idSpeech not in self.links:
			self.links[idSpeech] = {}

		self.links[idSpeech][idParagraphe] = Link(idSpeech, idParagraphe)

		return self.links[idSpeech][idParagraphe]

	def generateHtmlParagraphe(self):
		"""Renvoie les informations des paragraphes au format html"""

		text = ""

		tfidf_max = 0
		
		for paragraphe in self.paragraphes.values():
			if tfidf_max < paragraphe.tfidf_max:
				tfidf_max = paragraphe.tfidf_max

			text += paragraphe.generateHtml()

		text = "<div id=\"data_pdf\" data-number=\"" + str(len(self.paragraphes)) + "\" data-tfidf_max=\"" + str(tfidf_max) + "\" >\n" + text + "</div>"

		return text

	def generateHtmlSpeech(self):
		"""Renvoie les informations des speechs au format html"""

		text = ""

		tfidf_max = 0
		
		for speech in self.speechs.values():
			if tfidf_max < speech.tfidf_max:
				tfidf_max = speech.tfidf_max

			text += speech.generateHtml()

		text = "<div id=\"data_transcript\" data-number=\"" + str(len(self.speechs)) + "\" data-duree=\"" + str(self.dureeSpeech) + "\" data-tfidf_max=\"" + str(tfidf_max) + "\" >\n" + text + "</div>"

		return text

	def generateHtmlPage(self):
		"""Renvoie les informations des pages au format html"""

		text = "<div id=\"data_pagePdf\" data-number=\"" + str(len(self.pages)) + "\" >\n"
		
		for page in self.pages.values():
			text += page.generateHtml()

		text += "</div>"

		return text

	def generateHtmlLink(self):
		"""Renvoie les informations des liens au format html"""

		text = "<div id=\"data_alignement\" data-number=\"" + str(len(self.links)) + "\" >\n"

		list_links = [link for speech in self.links.values() for link in speech.values()]

		list_links.sort(key=lambda x : x.similarite, reverse=True)
		
		for link in list_links:
			text += link.generateHtml()

		text += "</div>"

		return text



class Segment:
	"""Définit un segment, soit un paragraphe, soit un speech"""


	def __init__(self, idSegment, doc):
		"""Initialise le segment

		On précise son id, et son texte
		"""

		self.idSegment = idSegment
		self.doc = doc
		self.words = []

	def defineVocabulary(self, vocabulary, stop_words):
		"""Définit le vocabulaire du segment

		À partir du vocabulaire et des stops-words de l'ensemble des documents, on va tokenizer et lemmatizer le segment, pour trouver son vocabulaire
		"""

		for word, pos in stem.lem.tokenize(self.doc):
			self.words.append(Word(word, pos, vocabulary, stop_words))

	def infoWords(self, df, idf, tf, tfidf, idSegment):
		"""Ajoute les informations pour chaque mot
	
		On précise leurs df, idf, tf et tfidf pour le segment donné
		On calcule au passage le tfidf maximum du segment
		"""
		
		self.tfidf_max = 0

		for word in self.words:
			word.addInfo(df[word.idWord], idf[word.idWord], tf[idSegment, word.idWord], tfidf[idSegment][word.idWord])

			if word.info['tfidf'] > self.tfidf_max:
				self.tfidf_max = word.info['tfidf']


class Speech(Segment):
	"""Définit un speech

	La classe hérite aussi des fonctions définit dans la classe Segment
	"""

	def __init__(self, idSegment, idSlide, doc):
		"""Initialise le speech

		On précise son id, l'id de son slide et son texte
		"""

		Segment.__init__(self, idSegment, doc)
		self.idSlide = idSlide

	def generateHtml(self):
		"""Renvoie les informations du speech au format html (balise div)

		On indique différentes informations, en attribut dans la balise :
			-class : un identifiant pour tous les speechs = "data_speech"
			-id : un identifiant unique à ce speech = "speech_" + idSegment
			-data-id : l'id du speech (juste un numéro, donc redondant avec les paragraphes, d'où la différence entre id et data-id)
			-data-idSlide : l'id du slide
			-data-begin : le temps de début du speech
			-data-end : le temps de fin du speech
			-data-moyenne : la moyenne des similarités avec les paragraphes
			-data-ecart_type : l'écart type des similarités avec les paragraphes
			-data-zero : le nombre de zéro dans les similarités avec les paragraphes
			-data-tfidf_max : la valeur de tfidf maximum parmi les mots du speech

		En contenu de la balise, on met le texte du speech, avec des informations supplémentaires pour chaque mot (voir classe Word)
		"""

		text = "<div class=\"data_speech\" id=\"speech_" + str(self.idSegment) + "\" data-id=\"" + str(self.idSegment) + "\" data-idSlide=\"" + str(self.idSlide) + "\" data-begin=\"" + str(self.begin) + "\" data-end=\"" + str(self.end) + "\" data-moyenne=\"" + str(self.moyenne) + "\" data-ecart_type=\"" + str(self.ecart_type) + "\" data-zero=\"" + str(self.zero) + "\" data-tfidf_max=\"" + str(self.tfidf_max) + "\" >\n"

		for word in self.words:
			text += word.generateHtml() + ' '

		text += "\n</div>\n"

		return text

	def temps(self, begin, end):
		"""Définit les temps de début et de fin du speech"""

		self.begin = begin
		self.end = end
	
	def info(self, moyenne, ecart_type, zero):
		"""Définit la moyenne, l'écart type et le nombre de zéro pour les similarités avec les paragraphes"""

		self.moyenne = moyenne
		self.ecart_type = ecart_type
		self.zero = zero


class Paragraphe(Segment):
	"""Définit un paragraphe

	La classe hérite aussi des fonctions définit dans la classe Segment
	"""

	def __init__(self, idSegment, idPage, doc):
		"""Initialise le paragraphe

		On précise son id, l'id de sa page et son texte
		"""

		Segment.__init__(self, idSegment, doc)
		self.idPage = idPage

	def generateHtml(self):
		"""Renvoie les informations du paragraphe au format html (balise div)

		On indique différentes informations, en attribut de la balise :
			-class : un identifiant pour tous les paragraphes = "data_paragraphe"
			-id : un identifiant unique à ce paragraphe = "paragraphe_" + idSegment
			-data-id : l'id du paragraphe (juste un numéro, donc redondant avec les speechs, d'où la différence entre id et data-id)
			-data-idPage : l'id de la page
			-data-top : la coordonnée en y (verticale) du haut du paragraphe
			-data-left : la coordonnée en x (horizontale) de la limite gauche du paragraphe
			-data-bottom : la coordonnée en y (verticale) du bas du paragraphe
			-data-right : la coordonnée en x (horizontale) de la limite droite du paragraphe
			-data-tfidf_max : la valeur de tfidf maximum parmi les mots du paragraphe

		En contenu de la balise, on met le texte du paragraphe, avec des informations supplémentaires pour chaque mot (voir classe Word)
		"""

		text = "<div class=\"data_paragraphe\" id=\"paragraphe_" + str(self.idSegment) + "\" data-id=\"" + str(self.idSegment) + "\" data-idPage=\"" + str(self.idPage) + "\" data-top=\"" + str(self.top) + "\" data-left=\"" + str(self.left) + "\" data-bottom=\"" + str(self.bottom) + "\" data-right=\"" + str(self.right) + "\" data-tfidf_max=\"" + str(self.tfidf_max) + "\" >\n"

		for word in self.words:
			text += word.generateHtml() + ' '

		text += "\n</div>\n"

		return text

	def position(self, top, left, right, bottom):
		"""Définit les coordonnées haute, gauche, droite et basse du paragraphe

		Les valeurs sont données en pourcentage dans la page. On peut donc retrouver les coordonnées en pixel dans la page avec la hauteur et la largeur de cette dernière
		"""

		self.top = top
		self.left = left
		self.right = right
		self.bottom = bottom


class Page:
	"""Définit une page de l'article"""	

	def __init__(self, idPage, numero, hauteur, largeur):
		"""Instancie un page

		On précise son id, son numéro (peut-être différent, les numéros de page ne démarre pas à zéro), sa hauteur et sa largeur
		"""

		self.idPage = idPage
		self.numero = numero
		self.hauteur = hauteur
		self.largeur = largeur

	
	def generateHtml(self):
		"""Renvoie les informations de la page au format html

		On indique différentes informations :
			-class : un identifiant pour tous les pages = "data_page"
			-id : un identifiant unique à cette page = "page_" + idPage
			-data-id : l'id de la page (juste un numéro, donc redondant avec les segments, d'où la différence entre id et data-id)
			-data-numero : le numéro de la page
			-data-hauteur : la hauteur de la page
			-data-largeur : la largeur de la page
		"""

		text = "<div class=\"data_page\" id=\"page_" + str(self.idPage) + "\" data-id=\"" + str(self.idPage) + "\" data-numero=\"" + str(self.numero) + "\" data-hauteur=\"" + str(self.hauteur) + "\" data-largeur=\"" + str(self.largeur) + "\" ></div>\n"

		return text

class Link:
	"""Définit un lien entre un paragraphe et un speech"""
	
	def __init__(self, idSpeech, idParagraphe):
		"""Initialise le lien

		On précise l'id du speech et l'id du paragraphe
		"""

		self.idSpeech = idSpeech
		self.idParagraphe = idParagraphe
		self.matchingWords = {}

	def generateHtml(self):
		"""Renvoie les informations du lien au format html

		On indique différentes informations :
			-class : un identifiant pour tous les liens = "data_link"
			-id : un identifiant unique à ce lien = "speech_" + idSpeech + "paragraphe_" + idParagraphe
			-data-idSpeech : l'id du speech
			-data-idParagraphe : l'id du paragraphe
			-data-similarite : la mesure de similarité entre le paragraphe et le speech

		En contenu de la balise, on met les mots en commun au speech et au paragraphe (appelés matching words), en précisant plusieurs informations :
			-class : "matchingWords"
			-data-lemme : le mot, sous la forme lemmatisée
			-data-value : une valeur de similarité pour le mot = le produit scalaire entre le tfidf du mot dans le paragraphe et le tfidf du mot dans le speech
				Attention : la valeur de similarité du lien est une mesure cosinus, alors qu'on a ici un produit scalaire, on ne peut donc pas faire de lien direct entre ses deux valeurs de similarité
		"""

		text = "<div class=\"data_link\" id=\"speech_" + str(self.idSpeech) + "-paragraphe_" + str(self.idParagraphe) + "\" data-idSpeech=\"" + str(self.idSpeech) + "\" data-idParagraphe=\"" + str(self.idParagraphe) + "\" data-similarite=\"" + str(self.similarite) + "\" >\n"

		list_matchingWords = self.matchingWords.items()

		list_matchingWords.sort(key=lambda x : x[1], reverse=True)

		for word,value in list_matchingWords:
			text += "<span class=\"matchingWords\" data-lemme=\"" + word + "\" data-value=\"" + str(value) + "\">" + word + "</span>\n"

		text += "</div>\n"

		return text


	def infoSimilarite(self, similarite):
		"""Définit la valeur de similarité entre le speech et le paragraphe"""

		self.similarite = similarite

	def addMatchingWord(self, word, value):
		"""Ajoute un mot commun au speech et au paragraphe

		On précise le mot (sous sa forme lemmatisée) et sa valeur de similarité (le produit scalaire entre les tfidf du mot dans le speech et le paragraphe)
		"""

		self.matchingWords[word] = value

	

class Word:
	"""Définit un mot

	Les documents fournissent un texte, qui va être tokenisé pour retrouver les mots. Ces mots vont ensuite être lemmatisé. On a alors trois catégories de mots (sous forme lemmatisée) :
		-La ponctuation, que le tokenizer nous garde comme un token. Elle n'est pas prise en compte
		-Les stop words, c'est-à-dire les mots du langage trop courant pour être significatif dans la différenciation de deux textes
		-Le reste des mots, qui définisse le vocabulaire du texte
	"""

	def __init__(self, word, pos_tag, vocabulary, stop_words):
		"""Instancie le mot

		On précise le mot, son pos_tag (si c'est un nom, un verbe, ...). Pour l'initialisation, on a aussi besoin du vocabulaire et des stops_words pour l'ensemble des documents, ces derniers contenants les lemmes des mots.
		Le but de cette classe, est de partir du mot complet, de le lemmatiser (à l'aide son pos tag), de retrouver si il fait parti du vocabulaire ou des stop_words :
			-Si son lemme est dans la liste de vocabulaire, on lui attribue l'id qu'il a dans le vocabulaire
			-S'il est dans la liste des stop words, on lui attribue l'id -1
			-S'il n'est dans aucun des deux (comme la ponctuation), on lui attribue l'id -2

		Enfin, on peut rajouter à chaque mot des informations (surtout ceux du vocabulaire) : le df, l'idf, le tf et le tfidf.
		"""

		self.word = word
		self.pos_tag = pos_tag
		self.lemme = stem.lem.lemmatize(self.word.lower(), self.pos_tag)

		if self.word.lower() in stop_words:
			self.idWord = -1
		elif self.lemme in vocabulary:
			self.idWord = vocabulary[self.lemme]
		else:
			self.idWord = -2

		self.info = {}

	def addInfo(self, df, idf, tf, tfidf):
		"""Ajoute des informations au mot"""

		self.info["df"] = df
		self.info["idf"] = idf
		self.info["tf"] = tf
		self.info["tfidf"] = tfidf

	def generateHtml(self):
		"""Renvoie les informations du mot au format html (balise span)

		Si le mot a l'id -2, on renvoie juste le mot, sinon on le met dans une balise span
		Si c'est un stop_word (id -1), on lui donne la class "stop_word"
		Sinon, on indique différentes informations :
			-class : "keyword"
			-data-lemme : le lemme du mot
			-data-... : un attribut pour chaque info ajouté au mot (voir fonction addInfo)
		"""

		if self.idWord == -1 :
			return "<span class=\"stop_word\">" + self.word + "</span>"
		elif self.idWord == -2:
			return self.word
		else:
			string = "<span class=\"keyword\" data-lemme=\"" + self.lemme + "\" "

			for data, value in self.info.iteritems():
				string +=  "data-" + data + "=\"" + str(value) + "\" "

			string += ">" + self.word + "</span>"

			return string

