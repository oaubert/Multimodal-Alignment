# -*- coding: utf-8 -*-

"""Ce module prend une instance de Documents (voir stem.py) et calcule les mesures de similarités de ces documents"""

from xml.dom import minidom
from xml.sax.saxutils import escape
import codecs
import tfidf
import stem
import sys
import segment


class Similarite:
	"""Calcule les mesures de similarité des documents passés en paramètre"""

	def __init__(self, document, lemmatizer = None):
		"""Initialise les documents et calcule les mesures de similarité

		
		Entrée :
			-document : une instance de Documents (voir stem.py)
			-lemmatizer : choix du tokenizer/lemmatize utilisé (voir tfidf._init__)
		"""

		self.document = document

		self.text_paragraphe = [paragraphe.doc for paragraphe in document.paragraphes.values()]
		self.text_speech = [speech.doc for speech in document.speechs.values()]

		#Tests :

			#self.text_paragraphe = ["J'aime les pommes.", "Et j'aime les fraises aussi", "Et les oranges"]
			#self.text_speech = ["Je suis malade", "Je suis meme tombe dans les pommes", "Mais j'aime les fraises"]

			#self.text_paragraphe = ["I was sleeping under a tree", "An apple fell from the tree", "I ate the apple"]
			#self.text_speech = ["I am eating an apple"]

		self.tfidf_cal = tfidf.Tfidf(self.text_paragraphe, self.text_speech)
		self.tfidf_cal.go([], lemmatizer=lemmatizer)
		self.res_tfidf = self.tfidf_cal.match


	def analyse_resultat(self):
		"""Ajoute les informations sur les similarités dans l'instance de Documents

		Informations :
			-le vocabulaire (voir segment.Documents.defineVocabulary)
			-les informations sur les mots, pour les speechs et les paragraphes (voir segment.Segment.infoWords)
			-les informations sur les similarités par paragraphes : moyenne, écrat-type et pourcentage de zero (voir segment.Speech.info)
			-les liens (voir segment.Document.addLink), avec les matchingWords
		"""

		self.document.defineVocabulary(self.tfidf_cal.vocabulary, self.tfidf_cal.stop_words)

		inv_vocabulary = dict((v,k) for k, v in self.tfidf_cal.vocabulary.iteritems())

		for idParagraphe in range(len(self.tfidf_cal.paragraphe)):
			self.document.paragraphes[idParagraphe].infoWords(self.tfidf_cal.df, self.tfidf_cal.idf, self.tfidf_cal.tf, self.tfidf_cal.tfidf, idParagraphe)

		
		for idSpeech in range(len(self.tfidf_cal.speech)):
			idSpeechMatrice = idSpeech + len(self.tfidf_cal.paragraphe);
			speech = self.document.speechs[idSpeech]

			speech.info(self.tfidf_cal.moyenne[idSpeech], self.tfidf_cal.ecartType[idSpeech], self.tfidf_cal.percentZero[idSpeech])
			speech.infoWords(self.tfidf_cal.df, self.tfidf_cal.idf, self.tfidf_cal.tf, self.tfidf_cal.tfidf, idSpeechMatrice)

			links = self.res_tfidf[idSpeech]
			

			for idParagraphe, similarite in links:
				if similarite != 0.:				
					link = self.document.addLink(idSpeech, idParagraphe)

					link.infoSimilarite(similarite)

					for word,value in self.tfidf_cal.matchingWords[idSpeech][idParagraphe].iteritems():
						link.addMatchingWord(inv_vocabulary[word], value)


