# -*- coding: utf-8 -*-

from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
import string

class LemmaTokenizer(object):
	def __init__(self):
		self.tk = PunktSentenceTokenizer()
		self.wnl = WordNetLemmatizer()
		self.wordLemmatized = {}

	def __call__(self, doc):
		#return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

		res = []

		for sentence in self.tk.tokenize(doc):
			for word, pos in pos_tag(word_tokenize(sentence)):
				if word not in string.punctuation:
					lem = self.wnl.lemmatize(word, self.get_wordnet_pos(pos))
					res.append(lem)
					self.wordLemmatized[word] = lem

		return res

	def tokenize(self, doc):
		res = []

		for sentence in self.tk.tokenize(doc):
			res.extend(pos_tag(word_tokenize(sentence)))

		return res

	def lemmatize(self, word, pos):
		return self.wnl.lemmatize(word, self.get_wordnet_pos(pos))

	def generateHtmlParagraphe(self, doc, resultat, idSegment):
		string = "" 
		for sentence in self.tk.tokenize(doc):
			for word, pos in pos_tag(word_tokenize(sentence)):
				lem = self.wnl.lemmatize(word, self.get_wordnet_pos(pos))
				if lem in resultat.vocabulary:
					id_word = resultat.vocabulary[lem]
					string += "<span class=\"keyword\" data-id=\"" + str(id_word) + "\" data-lem=\"" + lem + "\" data-df=\"" + str(resultat.df[id_word]) + "\" data-idf=\"" + str(resultat.idf[id_word]) + "\" data-tf=\"" + str(resultat.tf[idSegment, id_word]) + "data-tfidf=\"" + str(resultat.tfidf[idSegment][id_word]) + ">" + word + "</span> "
				else:
					string += word + " "

		return string


	#Trouver sur http://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
	def get_wordnet_pos(self, treebank_tag):
		if treebank_tag.startswith('J'):
		    return wordnet.ADJ
		elif treebank_tag.startswith('V'):
		    return wordnet.VERB
		elif treebank_tag.startswith('N'):
		    return wordnet.NOUN
		elif treebank_tag.startswith('R'):
		    return wordnet.ADV
		else:
		    return wordnet.NOUN


lem = LemmaTokenizer()


#lem = LemmaTokenizer()
#print lem("Figure 1: Partial monitoring games and their minimax regret as it was known previously. The big rectangle denotes the set of all games. Inside the big rectangle, the games are ordered from left to right based on their minimax regret. In the “hard” area, l.e.p. denotes label-efficient prediction. The grey area contains games whose");
#print lem("falling")
#print lem.wnl.lemmatize("ate", wordnet.VERB)

