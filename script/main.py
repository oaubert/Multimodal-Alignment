import sys
import codecs
import segment
import traitementPdf
import traitementVideo
import similarite

class Main:

	def __init__(self):
		self.document = segment.Documents()

	def run(self, filePdf, fileTranscript, fileSlide, nbColonnePdf, humanTranscript):

		optionPdf = {"alinea" : True, "interligne" : True, "changementColonne" : True, "trierPolice" : False, "trierMargeGauche" : False};

		traitePdf = traitementPdf.TraitementPdf(nbColonnePdf, filePdf, optionPdf)
		traitePdf.parsexml()
		traitePdf.formatResultat(self.document)

		traiteVideo = traitementVideo.TraitementVideo(fileTranscript, fileSlide, humanTranscript)
		traiteVideo.traiter()
		traiteVideo.formatResultat(self.document)

		sim = similarite.Similarite(self.document, "lemmatize")
		sim.analyse_resultat()

	

	def generateHtml(self, fileParagraphe, fileSpeech, filePage, fileAlignement):
		fichier = codecs.open(fileParagraphe, 'w', "utf-8")
		fichier.write(self.document.generateHtmlParagraphe())
		fichier.close()

		fichier = codecs.open(fileSpeech, 'w', "utf-8")
		fichier.write(self.document.generateHtmlSpeech())
		fichier.close()

		fichier = codecs.open(filePage, 'w', "utf-8")
		fichier.write(self.document.generateHtmlPage())
		fichier.close()

		fichier = codecs.open(fileAlignement, 'w', "utf-8")
		fichier.write(self.document.generateHtmlLink())
		fichier.close()



if len(sys.argv) != 10:
	print "Erreur, argument manquant !"
	exit(1)
else:
	filePdf = sys.argv[1]
	fileTranscript = sys.argv[2]
	fileSlide = sys.argv[3]
	nbColonnePdf = sys.argv[4]
	humanTranscript = sys.argv[5]
	fileParagraphe = sys.argv[6]
	fileSpeech = sys.argv[7]
	filePage = sys.argv[8]
	fileAlignement = sys.argv[9]

	main = Main()

	main.run(filePdf, fileTranscript, fileSlide, nbColonnePdf, humanTranscript)
	main.generateHtml(fileParagraphe, fileSpeech, filePage, fileAlignement)
