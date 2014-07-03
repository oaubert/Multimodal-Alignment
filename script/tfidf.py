# -*- coding: utf-8 -*-

"""Ce module permet de calculer les mesures de similarités entre des speechs et des paragraphes"""

import codecs
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy
import scipy.sparse as sp
from collections import Counter
import stem

class Tfidf:
	"""Permet de calculer les mesures de similarités entre des speechs et des paragraphes

	Cela se fait en plusieurs étapes :
		-Tokenisation et lemmatisation de tous les documents (speechs et paragraphes)
		-Détermination du vocabulaire, on compte tous les mots
		-Calcule de plusieurs valeurs : df, idf, tf, tfidf
		-Calcule des mesures cosinus entre les tfidf des speechs et des paragraphes
		-Calcule d'informations supplémentaires sur les mesures calculées
	"""
	
	def __init__(self, paragraphe, speech):
		"""Initialise les données

		Entrée :
			-paragraphe : liste des textes des paragraphes
			-speech : liste des textes des speechs

		On initialise set comme l'ensemble des textes
		"""

		self.paragraphe = paragraphe
		self.speech = speech

		self.set = list(self.paragraphe) #recopie
		self.set.extend(self.speech)


	def count(self, traitement=None):
		"""Définit le vocabulaire, et compte le nombre de mot par document (speech et paragraphe)

		Entrée : 
			-traitement : si traitement == "lemmatize", alors on utilise le tokenizer de stem.py, qui lemmatize en même
				sinon, on utilise le tokenizer par défaut de CountVectorizer (de sklearn), qui ne lemmatize pas

		Résultats :
			-self.tfidf_matrix : matrice creuse contenant pour chaque document, pour chaque mot, le nombre d'apparition du mot dans le document
			-self.vocabulary : dictionnaire contenant le vocabulaire
			-self.stop_words : dictionnaire contenant les stop_words
		"""

		if traitement == "lemmatize":
			self.tokenizer = stem.LemmaTokenizer()
		else:
			self.tokenizer = None

		self.tfidf_vectorizer = CountVectorizer(strip_accents='unicode', stop_words='english', tokenizer=self.tokenizer)
		self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.set)

		self.vocabulary = self.tfidf_vectorizer.vocabulary_
		self.stop_words = self.tfidf_vectorizer.get_stop_words()


	def do_tf(self, ponderation):
		"""Calcul du tf

		Le tf (term frequency), pour un mot dans un document, est le nombre d'apparition du mot dans le document. C'est donc le contenu de self.tfidf_matrix
		Cette fonction permet cependant une amélioration : la prise en compte du contexte. Ainsi, pour mesure la similarité entre un speech et un paragraphe, on va regarder un peu les speechs et les paragraphes autour.
		Pour cela, on va calculer un tf augmenté, qui va compté les mots dans un document, mais aussi les mots des documents autour avec une certaine pondération.

		Entrée :
			-ponderation : un tableau de ponderation, qui s'applique de manière symétrique autour du document observé (qui lui est pondéré à 1)	
				exemple : ponderation de la forme [0.8,0.2] == 1*tf[i] + 0.8*tf[i+1] + 0.8*tf[i-1] + 0.2tf[i-2] + 0.2tf[i+2], tf[i] tjr pondéré à 1

		Pour ne pas prendre en compte le contexte : ponderation = []
		"""

		self.tf = sp.lil_matrix(self.tfidf_matrix, dtype=float)
	

		id_set = 0
		for s in [self.paragraphe, self.speech]:
			for j in range(len(s)):
				for i in range(len(self.vocabulary)):
					for k,p in enumerate(ponderation):
						if j - (k+1) >= 0:
							self.tf[id_set,i] += p*float(self.tfidf_matrix[id_set-(k+1),i])
					
						if j + (k+1) < len(s):
							self.tf[id_set,i] += p*float(self.tfidf_matrix[id_set+(k+1),i])

				id_set += 1



	#Calcul du tfidf

	def do_df(self):
		"""Calcul du df

		Le df (document frequency), pour un mot, correspond au nombre de documents où le mot apparait.
		On vérifie donc, pour chaque document, si le tf du mot dans ce document est non nul
		"""

		self.df = Counter()

		for _, i in self.vocabulary.iteritems():
			for j in range(len(self.set)):
				if self.tfidf_matrix[j,i] != 0:
					self.df[i] += 1


	def do_idf(self): 
		"""Calcul de l'idf

		L'idf (inverse term frequency) = log(nombre de documents / df) pour un mot
		"""

		self.idf = list(map(lambda x : numpy.log10((len(self.set)) / float(x)), self.df.values())) 


	def do_tfidf(self):
		"""Calcul du tfidf

		Le tfidf, pour un mot et un document = tf*idf
		"""

		self.tfidf = []
		for j in range(len(self.set)):
			self.tfidf.append([])
			for i in range(len(self.vocabulary)):
				self.tfidf[j].append(0.)

		for j in range(len(self.set)):
			for k,i in self.vocabulary.iteritems():				
				self.tfidf[j][i] = (self.tf[j,i] * self.idf[i])



	#Variantes de calcul

	def do_idf_variante(self): 
		"""Variante du calcul de l'idf

		Dans cette variante : idf = log( (nombre de document + 1) / (df + 1) ) + 1
		C'est cette variante de l'idf qui est utilisé dans sklearn si on ne spécifie pas de norme (paramètre norm=None)
		"""

		self.idf = list(map(lambda x : numpy.log((len(self.set) + 1.0) / float(x + 1.0)) + 1.0, self.df.values()))


	def do_idf_original(self):
		"""Calcul de l'idf directement avec sklearn

		On calcule ici l'idf directement avec les classe de sklearn. On obtient le même résultat que do_idf_variante.
		Calculer nous même l'idf nous permet de mieux contrôler ce que l'on fait, notamment sur la variante utilisée.
		"""
		tfidf_transformer = TfidfTransformer()
		tfidf_transformer.fit(self.tfidf_matrix)

		self.idf = tfidf_transformer.idf_


	def do_tfidf_original(self):
		"""Calcul du tfidf directement avec sklearn

		Sklearn nous permet de calculer directement les valeurs de tfidf en quelques lignes (incluant la tokenisation, le comptage, et les calculs intermédiaires). Le problème est qu'il ne gère pas le contexte, et qu'on a pas le choix des variantes de calcul.
		"""

		tfidf_v = TfidfVectorizer(strip_accents='unicode', stop_words='english', norm=None)
		self.tfidf = tfidf_v.fit_transform(self.set)




	#Mesure cosinus

	def mesure(self):
		"""Calcul les mesures de similarités entre les speechs et les paragraphes avec une mesure cosinus

		Résultat : 
			-self.similarite : un dictionnaire de la forme : self.similarite[idSpeech][idParagraphe] = valeur_similarite
		"""

		cosine_liste = cosine_similarity(self.tfidf[len(self.paragraphe):], self.tfidf[:len(self.paragraphe)]) #set1 to set2

		self.similarite = {}

		for i, cosine in enumerate(cosine_liste):
			for j, value in enumerate(cosine):
				if i in self.similarite:
					self.similarite[i][j] = value
				else:
					self.similarite[i] = {j : value}


	#Informations

	def do_infoMesure(self):
		"""Calcul des informations sur les mesures de similarités

		On calcule la moyenne et l'écart-type des similarités, ainsi que le pourcentage de zéro, par speech
		"""

		self.moyenne = {}
		self.ecartType = {}
		self.percentZero = {}

		for id_speech,speech in self.similarite.iteritems():
			somme = 0.
			nbZero = 0

			for v in speech.values():
				somme += v
				if v == 0:
					nbZero += 1

			self.moyenne[id_speech] = somme / float(len(speech))
			self.percentZero[id_speech] = float((nbZero * 100)) / float(len(speech))

			somme = 0.

			for v in speech.values():
				somme += (v - self.moyenne[id_speech])**2

			self.ecartType[id_speech] = numpy.sqrt(somme) / float(len(speech))


	def do_matchingWords(self):
		"""Détermine les mots en commun entre chaque speech et paragraphe (les matching words)

		On regarde les mots en commun dans chaque paire speech/paragraphe (tfidf non nul dans les deux documents) et on calcule leur similarité comme un produit scalaire. Attention, on utilise pas la même méthode pour la similarité entre deux mots, et la similarité entre deux documents.
		"""

		self.matchingWords = {}

		for j,speech in enumerate(self.tfidf[len(self.paragraphe):]):
			self.matchingWords[j] = {}
			for i,paragraphe in enumerate(self.tfidf[:len(self.paragraphe)]):
				self.matchingWords[j][i] = {}
				for w in range(len(self.vocabulary)):
					value = self.tfidf[len(self.paragraphe) + j][w] * self.tfidf[i][w]
					if value > 0.:
						self.matchingWords[j][i][w] = value

	
	def do_match(self, n=None):
		"""Trie les n meilleurs similarités pour chaque speech

		Si n = None, on garde toutes les similarités, triées, stockées dans self.match
		"""
		self.match = {}
		for i,s1 in enumerate(self.speech):
			if n:
				self.match[i] = sorted(self.similarite[i].iteritems(), key=lambda (k,v) : (v,k))[-n:]
			else:
				self.match[i] = sorted(self.similarite[i].iteritems(), key=lambda (k,v) : (v,k))



	#Éxécution

	def go(self, ponderation, n=None, lemmatizer=None):
		"""Calcul les mesures de similarités en appliquant toutes les opérations nécessaire

		Entrée :
			-ponderation : un tableau des pondération pour le contexte (voir do_tf)
			-n : le nombre de paragraphes avec les meilleurs similarités que l'on veut garder par speech (voir do_match)
			-lemmatizer : le tokenizer/lemmatizer utilisé (voir __init__)
		"""

		self.count(lemmatizer)
		#print self.vocabulary
		print
		print "tf\n"
		self.do_tf(ponderation)
		print "df\n"
		self.do_df()
		print "idf\n"
		self.do_idf()
		print "tfidf\n"
		self.do_tfidf()
		print "cosine\n"
		self.mesure()
		print "info\n"
		self.do_match(n)
		print
		#print self.match
		self.do_infoMesure()
		self.do_matchingWords()




if __name__ == '__main__':
	#Exemple d'utilisation
	t = Tfidf(["Je parle de poire", "Je parle de pomme", "Je parle de fraise"], ["This is pomme poire fraise"]) 
	t.go([], None, "lemmatize")
