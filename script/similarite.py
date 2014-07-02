from xml.dom import minidom
from xml.sax.saxutils import escape
import codecs
import tfidf
import stem
import sys
import segment
import json

def text(node):
	return node.firstChild.nodeValue

def json_default(obj):
	return obj.toJson()

def toJson(obj):
	return json.dumps(obj, default=json_default, sort_keys=True, indent=2)

class Similarite:

	def __init__(self, document, lemmatizer = None):
	
		self.document = document

		self.text_paragraphe = [paragraphe.doc for paragraphe in document.paragraphes.values()]
		self.text_speech = [speech.doc for speech in document.speechs.values()]

		#self.text_paragraphe = ["J'aime les pommes.", "Et j'aime les fraises aussi", "Et les oranges"]
		#self.text_speech = ["Je suis malade", "Je suis meme tombe dans les pommes", "Mais j'aime les fraises"]

		#self.text_paragraphe = ["I was sleeping under a tree", "An apple fell from the tree", "I ate the apple"]
		#self.text_speech = ["I am eating an apple"]

		self.tfidf_cal = tfidf.Tfidf(self.text_paragraphe, self.text_speech)
		self.tfidf_cal.go([], lemmatizer=lemmatizer)
		self.res_tfidf = self.tfidf_cal.match


	def analyse_resultat(self):

		self.document.defineVocabulary(self.tfidf_cal.vocabulary, self.tfidf_cal.stop_words)

		inv_vocabulary = dict((v,k) for k, v in self.tfidf_cal.vocabulary.iteritems())

		for idParagraphe in range(len(self.tfidf_cal.paragraphe)):
			self.document.paragraphes[idParagraphe].infoWords(self.tfidf_cal.df, self.tfidf_cal.idf, self.tfidf_cal.tf, self.tfidf_cal.tfidf, idParagraphe)

		
		for idSpeech in range(len(self.tfidf_cal.slide)):
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


	def ecrire_resultat(self):

		paragraphe_string = toJson(self.documents.paragraphes)
		speech_string = toJson(self.documents.speechs)
		link_string = toJson(self.documents.links)

		fichier = codecs.open("paragraphe.json", 'w', "utf-8")
		fichier.write(paragraphe_string)
		fichier.close()

		fichier = codecs.open("speech.json", 'w', "utf-8")
		fichier.write(speech_string)
		fichier.close()

		fichier = codecs.open("link.json", 'w', "utf-8")
		fichier.write(link_string)
		fichier.close()


"""
	def write_result()

		alignment_doc = minidom.Document()

	
		alignment = alignment_doc.createElement('alignment')

		alignment_doc.appendChild(alignment)


		for k,v in res_tfidf.iteritems():
			speech = alignment_doc.createElement('speech')
			speech.setAttribute('id', str(k))
		
			speech.setAttribute('moyenne', str(tfidf_cal.moyenne[k]))
			speech.setAttribute('ecartType', str(tfidf_cal.ecartType[k]))
			speech.setAttribute('percentZero', str(tfidf_cal.percentZero[k]))
	
			for (a,b) in v:
				if b != 0.:
					paragraphe = alignment_doc.createElement('paragraphe')
					paragraphe.setAttribute('id', str(a))
					paragraphe.setAttribute('similarite', str(b))

					str_matchingWords = ""

					#matchingWords = tfidf_cal.getMaxMatchingWords(k, a, 5)
					for c,d in tfidf_cal.matchingWords[k][a].iteritems():
						str_matchingWords += str(c) + ':' + str(d) + ';'

					str_matchingWords = str_matchingWords[:-1]
				
					paragraphe.setAttribute('matchingWords', str_matchingWords)

					speech.appendChild(paragraphe)


			alignment.appendChild(speech)

		fichier = codecs.open("alignment.xml", 'w', "utf-8")
		fichier.write(alignment_doc.toprettyxml())
		fichier.close()





	
		vocabulary_doc = minidom.Document()

		vocabulary = vocabulary_doc.createElement('vocabulary')
		vocabulary_doc.appendChild(vocabulary)


		for k,v in tfidf_cal.vocabulary.iteritems():
			word = vocabulary_doc.createElement('word')
			word.setAttribute('id', str(v))
			word.setAttribute('df', str(tfidf_cal.df[v]))
			word.setAttribute('idf', str(tfidf_cal.idf[v]))
			textNode = vocabulary_doc.createTextNode(escape(k))
			word.appendChild(textNode)
			vocabulary.appendChild(word)


		fichier = codecs.open("vocabulary.xml", 'w', "utf-8")
		fichier.write(vocabulary_doc.toprettyxml())
		fichier.close()


	


	
		infoSpeech_doc = minidom.Document()

		infoSpeech = infoSpeech_doc.createElement('infoSpeech')

		infoSpeech_doc.appendChild(infoSpeech)
	
	
		for i in range(len(tfidf_cal.slide)):
			speech = infoSpeech_doc.createElement('speech')
			speech.setAttribute('id', str(i))

			id_matrix = len(tfidf_cal.paragraphe) + i
		
			for (a,b) in [(a,b) for a,b in tfidf_cal.vocabulary.iteritems() if tfidf_cal.tfidf_matrix[id_matrix,b] != 0]:
				word = infoSpeech_doc.createElement('s_word')
				word.setAttribute('idWord', str(b))
				word.setAttribute('tf_base', str(tfidf_cal.tfidf_matrix[id_matrix, b]))
				word.setAttribute('tf', str(tfidf_cal.tf[id_matrix, b]))
				word.setAttribute('tfidf', str(tfidf_cal.tfidf[id_matrix][b]))
				textNode = infoSpeech_doc.createTextNode(escape(a))
				word.appendChild(textNode)

				speech.appendChild(word)

			html = infoSpeech_doc.createElement('html')
			textNode = infoSpeech_doc.createCDATASection(lem.generateHtmlParagraphe(preprocess(tfidf_cal.tfidf_vectorizer.decode(text_paragraphe[i])), tfidf_cal, id_matrix))
			html.appendChild(textNode)

			speech.appendChild(html)


			infoSpeech.appendChild(speech)


		fichier = codecs.open("infoSpeech.xml", 'w', "utf-8")
		fichier.write(infoSpeech_doc.toprettyxml())
		fichier.close()


		lem = stem.LemmaTokenizer()

		preprocess = tfidf_cal.tfidf_vectorizer.build_preprocessor()


		infoParagraphe_doc = minidom.Document()

		infoParagraphe = infoParagraphe_doc.createElement('infoParagraphe')

		infoParagraphe_doc.appendChild(infoParagraphe)


		for i in range(len(tfidf_cal.paragraphe)):
			paragraphe = infoParagraphe_doc.createElement('paragraphe')
			paragraphe.setAttribute('id', str(i))
		
			for (a,b) in [(a,b) for a,b in tfidf_cal.vocabulary.iteritems() if tfidf_cal.tfidf_matrix[i,b] != 0]:
				word = infoParagraphe_doc.createElement('p_word')
				word.setAttribute('idWord', str(b))
				word.setAttribute('tf_base', str(tfidf_cal.tfidf_matrix[i, b]))
				word.setAttribute('tf', str(tfidf_cal.tf[i, b]))
				word.setAttribute('tfidf', str(tfidf_cal.tfidf[i][b]))
				textNode = infoParagraphe_doc.createTextNode(escape(a))
				word.appendChild(textNode)

				paragraphe.appendChild(word)

			html = infoParagraphe_doc.createElement('html')
			textNode = infoParagraphe_doc.createCDATASection(lem.generateHtmlParagraphe(preprocess(tfidf_cal.tfidf_vectorizer.decode(text_paragraphe[i])), tfidf_cal, i))
			html.appendChild(textNode)

			paragraphe.appendChild(html)

			infoParagraphe.appendChild(paragraphe)


		fichier = codecs.open("infoParagraphe.xml", 'w', "utf-8")
		fichier.write(infoParagraphe_doc.toprettyxml())
		fichier.close()



		if lemmatizer != None:

			infoLemmatizer_doc = minidom.Document()

			infoLemmatizer = infoLemmatizer_doc.createElement('infoLemmatizer')

			infoLemmatizer_doc.appendChild(infoLemmatizer)


			for k,v in tfidf_cal.tokenizer.wordLemmatized.iteritems() :
				word = infoLemmatizer_doc.createElement('l_word')
			
				word.setAttribute('original', escape(k))
				textNode = infoLemmatizer_doc.createTextNode(escape(v))
				word.appendChild(textNode)

				infoLemmatizer.appendChild(word)


			fichier = codecs.open("infoLemmatizer.xml", 'w', "utf-8")
			fichier.write(infoLemmatizer_doc.toprettyxml())
			fichier.close()


"""	

if __name__ == '__main__':
        if len(sys.argv < 4):
                print "Syntaxe: %s pdf.xml transcript.xml" % sys.argv[0]
                sys.exit(1)
	sim = Similarite(sys.argv[1], sys.argv[2], "lemmatize")
	sim.analyse_resultat()
	sim.ecrire_resultat()
