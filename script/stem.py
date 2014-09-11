# -*- coding: utf-8 -*-

"""
Ce module donne une classe qui tokenize puis lemmatize un texte (paragraphe ou speech).
"""

from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
import string

class LemmaTokenizer(object):
	"""Permet de tokernizer et lemmatizer un texte

	Cette classe peut être utilisé de deux manières. Elle peut être appelé comme une fonction (grâce à la méthode __call__ ). Dans ce cas, elle va tokenizer puis lemmatizer le texte en même temps. Si on veut avoir un peu plus de liberté, on peut utilisé la fonction tokenize qui renvoie l'ensemble des tokens avec leur pos_tag, puis la fonction lemmatize qui lemmatize un mot grâce à son pos_tag. Cela permet d'effectuer des opérations entre la tokenization et la lemmatization.
	"""

	def __init__(self):
		"""Initialise l'objet, en instanciant un tokenizer de phrase et un lemmatizer

		On utilise que des classes ou fonctions de nltk.
		Pour tokenizer, on commence par séparé le texte en phrase avec une instance de PunktSentenceTokenizer, qui doit donc être initalisé ici. Puis on tokenize chaque phrase avec word_tokenize, qui est une fonction, et ne nécessite donc pas d'initialisation, de même que pos_tag qui permet de pos_taguer chaque mot. Enfin, on lemmatize chaque mot avec une instance WordNetLemmatizer, qui est donc initialisé.
		"""

		self.tk = PunktSentenceTokenizer()
		self.wnl = WordNetLemmatizer()

	def __call__(self, doc):
		"""Tokenize puis lemmatize un texte

		Cette fonction renvoie la liste des lemmes à partir du texte.
		"""

		res = []

		for sentence in self.tk.tokenize(doc):
			for word, pos in pos_tag(word_tokenize(sentence)):
				if word not in string.punctuation:
					lem = self.wnl.lemmatize(word, self.get_wordnet_pos(pos))
					res.append(lem)

		return res

	def tokenize(self, doc):
		"""Tokenize un texte

		Cette fonction renvoie la liste des couples (token, pos_tag) à partir du texte
		"""

		res = []

		for sentence in self.tk.tokenize(doc):
			res.extend(pos_tag(word_tokenize(sentence)))

		return res

	def lemmatize(self, word, pos):
		"""Lemmatize un mot avec son pos_tag

		Cette fonction renvoie le lemme du mot
		"""

		return self.wnl.lemmatize(word, self.get_wordnet_pos(pos))


	def get_wordnet_pos(self, treebank_tag):
		"""Converti le pos_tag obtenu en tokenisant pour qu'il soit utilisable par le lemmatizer

		Ici, on a 4 tags possibles : adjectif, verbe, nom et adverbe. Le tag par défaut (si aucun autre ne convient) est le nom.
		Cette fonction a été trouvée sur http://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
		"""

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



#lem = LemmaTokenizer()
#print lem("Figure 1: Partial monitoring games and their minimax regret as it was known previously. The big rectangle denotes the set of all games. Inside the big rectangle, the games are ordered from left to right based on their minimax regret. In the “hard” area, l.e.p. denotes label-efficient prediction. The grey area contains games whose");
#print lem("falling")
#print lem.wnl.lemmatize("ate", wordnet.VERB)

