import codecs
import stem

class Documents:
	def __init__(self):
		self.speechs = {}
		self.paragraphes = {}
		self.pages = {}
		self.links = {}

	def infoDureeSpeech(self, duree):
		self.dureeSpeech = duree

	def defineVocabulary(self, vocabulary, stop_words):
		self.vocabulary = vocabulary
		self.stop_words = stop_words

		for paragraphe in self.paragraphes.values():
			paragraphe.defineVocabulary(self.vocabulary, self.stop_words)

		for speech in self.speechs.values():
			speech.defineVocabulary(self.vocabulary, self.stop_words)

	def addSpeech(self, idSpeech, idSlide, doc):
		self.speechs[idSpeech] = Speech(idSpeech, idSlide, doc)
		return self.speechs[idSpeech]

	def addPage(self, idPage, numero, hauteur, largeur):
		self.pages[idPage] = Page(idPage, numero, hauteur, largeur)
		return self.pages[idPage]

	def addParagraphe(self, idParagraphe, idPage, doc):
		self.paragraphes[idParagraphe] = Paragraphe(idParagraphe, idPage, doc)
		return self.paragraphes[idParagraphe]

	def addLink(self, idSpeech, idParagraphe):
		if idSpeech not in self.links:
			self.links[idSpeech] = {}

		self.links[idSpeech][idParagraphe] = Link(idSpeech, idParagraphe)

		return self.links[idSpeech][idParagraphe]

	def generateHtmlParagraphe(self):
		text = ""

		tfidf_max = 0
		
		for paragraphe in self.paragraphes.values():
			if tfidf_max < paragraphe.tfidf_max:
				tfidf_max = paragraphe.tfidf_max

			text += paragraphe.generateHtml()

		text = "<div id=\"data_pdf\" data-number=\"" + str(len(self.paragraphes)) + "\" data-tfidf_max=\"" + str(tfidf_max) + "\" >\n" + text + "</div>"

		return text

	def generateHtmlSpeech(self):
		text = ""

		tfidf_max = 0
		
		for speech in self.speechs.values():
			if tfidf_max < speech.tfidf_max:
				tfidf_max = speech.tfidf_max

			text += speech.generateHtml()

		text = "<div id=\"data_transcript\" data-number=\"" + str(len(self.speechs)) + "\" data-duree=\"" + str(self.dureeSpeech) + "\" data-tfidf_max=\"" + str(tfidf_max) + "\" >\n" + text + "</div>"

		return text

	def generateHtmlPage(self):
		text = "<div id=\"data_pagePdf\" data-number=\"" + str(len(self.pages)) + "\" >\n"
		
		for page in self.pages.values():
			text += page.generateHtml()

		text += "</div>"

		return text

	def generateHtmlLink(self):
		text = "<div id=\"data_alignement\" data-number=\"" + str(len(self.links)) + "\" >\n"

		list_links = [link for speech in self.links.values() for link in speech.values()]

		list_links.sort(key=lambda x : x.similarite, reverse=True)
		
		for link in list_links:
			text += link.generateHtml()

		text += "</div>"

		return text



class Segment:
	
	def __init__(self, idSegment, doc):
		self.idSegment = idSegment
		self.doc = doc
		self.words = []

	def defineVocabulary(self, vocabulary, stop_words):
		for word, pos in stem.lem.tokenize(self.doc):
			self.words.append(Word(word, pos, vocabulary, stop_words))

	def infoWords(self, df, idf, tf, tfidf, idSegment):
		self.tfidf_max = 0

		for word in self.words:
			word.info['df'] = df[word.idWord]
			word.info['idf'] = idf[word.idWord]
			word.info['tf'] = tf[idSegment, word.idWord]
			word.info['tfidf'] = tfidf[idSegment][word.idWord]

			if word.info['tfidf'] > self.tfidf_max:
				self.tfidf_max = word.info['tfidf']


class Speech(Segment):

	def __init__(self, idSegment, idSlide, doc):
		Segment.__init__(self, idSegment, doc)
		self.idSlide = idSlide

	def generateHtml(self):
		text = "<div class=\"data_speech\" id=\"speech_" + str(self.idSegment) + "\" data-id=\"" + str(self.idSegment) + "\" data-idSlide=\"" + str(self.idSlide) + "\" data-begin=\"" + str(self.begin) + "\" data-end=\"" + str(self.end) + "\" data-moyenne=\"" + str(self.moyenne) + "\" data-ecart_type=\"" + str(self.ecart_type) + "\" data-zero=\"" + str(self.zero) + "\" data-tfidf_max=\"" + str(self.tfidf_max) + "\" >\n"

		for word in self.words:
			text += word.generateHtml() + ' '

		text += "\n</div>\n"

		return text

	def toJson(self):
		return {'idSpeech' : self.idSegment, 'moyenne' : self.moyenne, 'ecart_type' : self.ecart_type, 'zero' : self.zero, 'html' : self.generateHtml()}

	def temps(self, begin, end):
		self.begin = begin
		self.end = end
	
	def info(self, moyenne, ecart_type, zero):
		self.moyenne = moyenne
		self.ecart_type = ecart_type
		self.zero = zero


class Paragraphe(Segment):

	def __init__(self, idSegment, idPage, doc):
		Segment.__init__(self, idSegment, doc)
		self.idPage = idPage

	def generateHtml(self):
		text = "<div class=\"data_paragraphe\" id=\"paragraphe_" + str(self.idSegment) + "\" data-id=\"" + str(self.idSegment) + "\" data-idPage=\"" + str(self.idPage) + "\" data-top=\"" + str(self.top) + "\" data-left=\"" + str(self.left) + "\" data-bottom=\"" + str(self.bottom) + "\" data-right=\"" + str(self.right) + "\" data-tfidf_max=\"" + str(self.tfidf_max) + "\" >\n"

		for word in self.words:
			text += word.generateHtml() + ' '

		text += "\n</div>\n"

		return text

	def position(self, top, left, right, bottom): #En pourcentage
		self.top = top
		self.left = left
		self.right = right
		self.bottom = bottom

	def toJson(self):
		return {'idParagraphe' : self.idSegment, 'html' : self.generateHtml()}
	

class Page:
	
	def __init__(self, idPage, numero, hauteur, largeur):
		self.idPage = idPage
		self.numero = numero
		self.hauteur = hauteur
		self.largeur = largeur

	
	def generateHtml(self):
		text = "<div class=\"data_page\" id=\"page_" + str(self.idPage) + "\" data-id=\"" + str(self.idPage) + "\" data-numero=\"" + str(self.numero) + "\" data-hauteur=\"" + str(self.hauteur) + "\" data-largeur=\"" + str(self.largeur) + "\" ></div>\n"

		return text

class Link:
	
	def __init__(self, idSpeech, idParagraphe):
		self.idSpeech = idSpeech
		self.idParagraphe = idParagraphe
		self.matchingWords = {}

	def generateHtml(self):
		text = "<div class=\"data_link\" id=\"speech_" + str(self.idSpeech) + "-paragraphe_" + str(self.idParagraphe) + "\" data-idSpeech=\"" + str(self.idSpeech) + "\" data-idParagraphe=\"" + str(self.idParagraphe) + "\" data-similarite=\"" + str(self.similarite) + "\" >\n"

		list_matchingWords = self.matchingWords.items()

		list_matchingWords.sort(key=lambda x : x[1], reverse=True)

		for word,value in list_matchingWords:
			text += "<span class=\"matchingWords\" data-lemme=\"" + word + "\" data-value=\"" + str(value) + "\">" + word + "</span>\n"

		text += "</div>\n"

		return text


	def infoSimilarite(self, similarite):
		self.similarite = similarite

	def addMatchingWord(self, word, value):
		self.matchingWords[word] = value

	

class Word:
	def __init__(self, word, pos, vocabulary, stop_words):
		self.word = word
		self.pos = pos
		self.lemme = stem.lem.lemmatize(self.word.lower(), self.pos)

		if self.word.lower() in stop_words:
			self.idWord = -1
		elif self.lemme in vocabulary:
			self.idWord = vocabulary[self.lemme]
		else:
			self.idWord = -2

		self.info = {}

	def generateHtml(self):
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
	



#vocabulary = {"apple" : 5, "eat" : 2}
#seg = Segment(1, "I am eating an apple")

#print seg.doc
#print seg.generateHtml(vocabulary)
