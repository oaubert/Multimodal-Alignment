# -*- coding: utf-8 -*-

import codecs
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy
import scipy.sparse as sp
from collections import Counter
import stem

class Tfidf:
	
	def __init__(self, paragraphe, slide):
		self.paragraphe = paragraphe
		self.slide = slide

		self.set = list(self.paragraphe) #recopie
		self.set.extend(self.slide)


	def count(self, traitement=None):
		if traitement == "lemmatize":
			self.tokenizer = stem.LemmaTokenizer()
		else:
			self.tokenizer = None
		self.tfidf_vectorizer = CountVectorizer(strip_accents='unicode', stop_words='english', tokenizer=self.tokenizer)
		self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.set)

		self.vocabulary = self.tfidf_vectorizer.vocabulary_
		self.stop_words = self.tfidf_vectorizer.get_stop_words()

		print self.stop_words


	def do_tf(self, ponderation):
		#ponderation de la forme [0.8,0.2] == 1*tf[i] + 0.8*tf[i+1] + 0.8*tf[i-1] + 0.2tf[i-2] + 0.2tf[i+2], tf[i] tjr pondéré à 1
		self.tf = sp.lil_matrix(self.tfidf_matrix, dtype=float)
	

		id_set = 0
		for s in [self.paragraphe, self.slide]:
			for j in range(len(s)):
				for i in range(len(self.vocabulary)):
					for k,p in enumerate(ponderation):
						if j - (k+1) >= 0:
							self.tf[id_set,i] += p*float(self.tfidf_matrix[id_set-(k+1),i])
					
						if j + (k+1) < len(s):
							self.tf[id_set,i] += p*float(self.tfidf_matrix[id_set+(k+1),i])

				id_set += 1

	
	def do_df(self):
		self.df = Counter()

		for _, i in self.vocabulary.iteritems():
			for j in range(len(self.set)):
				if self.tfidf_matrix[j,i] != 0:
					self.df[i] += 1


	def do_idf(self): #idf simple de wikipédia (même que Davy)
		self.idf = list(map(lambda x : numpy.log10((len(self.set)) / float(x)), self.df.values())) 


	def do_idf2(self): #même idf que sclearn, pour norm=None
		self.idf = list(map(lambda x : numpy.log((len(self.set) + 1.0) / float(x + 1.0)) + 1.0, self.df.values()))

	def do_idf_original(self):
		tfidf_transformer = TfidfTransformer()
		tfidf_transformer.fit(self.tfidf_matrix)

		self.idf = tfidf_transformer.idf_



	def do_tfidf(self):
		self.tfidf = []
		for j in range(len(self.set)):
			self.tfidf.append([])
			for i in range(len(self.vocabulary)):
				self.tfidf[j].append(0.)

		for j in range(len(self.set)):
			for k,i in self.vocabulary.iteritems():				
				self.tfidf[j][i] = (self.tf[j,i] * self.idf[i])


	def do_tfidf_original(self):
		tfidf_v = TfidfVectorizer(strip_accents='unicode', stop_words='english', norm=None)
		self.tfidf = tfidf_v.fit_transform(self.set)



	def mesure(self):
		cosine_liste = cosine_similarity(self.tfidf[len(self.paragraphe):], self.tfidf[:len(self.paragraphe)]) #set1 to set2

		self.similarite = {}

		for i, cosine in enumerate(cosine_liste):
			for j, value in enumerate(cosine):
				if i in self.similarite:
					self.similarite[i][j] = value
				else:
					self.similarite[i] = {j : value}

				#print "Slide : ", i, "  Paragraphe : ", j, "  Similarite : ", value

	def do_infoMesure(self):
		self.moyenne = {}
		self.ecartType = {}
		self.percentZero = {}

		for id_slide,slide in self.similarite.iteritems():
			somme = 0.
			nbZero = 0

			for v in slide.values():
				somme += v
				if v == 0:
					nbZero += 1

			self.moyenne[id_slide] = somme / float(len(slide))
			self.percentZero[id_slide] = float((nbZero * 100)) / float(len(slide))

			somme = 0.

			for v in slide.values():
				somme += (v - self.moyenne[id_slide])**2

			self.ecartType[id_slide] = numpy.sqrt(somme) / float(len(slide))


	def do_matchingWords(self):
		self.matchingWords = {}

		for j,slide in enumerate(self.tfidf[len(self.paragraphe):]):
			self.matchingWords[j] = {}
			for i,paragraphe in enumerate(self.tfidf[:len(self.paragraphe)]):
				self.matchingWords[j][i] = {}
				for w in range(len(self.vocabulary)):
					value = self.tfidf[len(self.paragraphe) + j][w] * self.tfidf[i][w]
					if value > 0.:
						self.matchingWords[j][i][w] = value

	def getMaxMatchingWords(self, slide, paragraphe, n):
		max_matchingWords = [(0,0)]*n

		for word,value in enumerate(self.matchingWords[slide][paragraphe]):
			for m,(w,v) in enumerate(max_matchingWords):
				if value > v:
					max_matchingWords.insert(m, (word,value))
					max_matchingWords.pop()
					break

		return max_matchingWords

	def getMotCommun(self, slide):
		motCommun = []

		for i in range(len(self.paragraphe)):
			motCommun.append([])
			for k in [k for k,v in self.vocabulary.iteritems() if self.tfidf_matrix[len(self.paragraphe) + slide,v] != 0 and self.tfidf_matrix[i,v] != 0]:
				motCommun[i].append(k)
				

		return motCommun

	def do_match(self, n=None):
		self.match = {}
		for i,s1 in enumerate(self.slide):
			if n:
				self.match[i] = sorted(self.similarite[i].iteritems(), key=lambda (k,v) : (v,k))[-n:]
			else:
				self.match[i] = sorted(self.similarite[i].iteritems(), key=lambda (k,v) : (v,k))


	
#voir exemple de tfidf wikipedia (en)

	def go(self, ponderation, n=None, lemmatizer=None):
		
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

#t = Tfidf(["Je parle de poire", "Je parle de pomme", "Je parle de fraise"], ["This is pomme poire fraise"]) 
#t.go([0.5], 1)
