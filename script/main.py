import sys
import codecs
import segment
import traitementPdf
import traitementVideo
import similarite

"""
Ce module définit la classe Main, qui coordine les différents scripts, et permet de l'appeler avec des arguments
"""

class Main:
	"""Génère les données nécessaires pour trouver un alignement global en effectuant des traitement successifs sur plusieurs fichiers

	Pour cela, elle a besoin de plusieurs fichiers en entrée :
		- L'article au format pdf
		- La transcription de la vidéo
		- La transcription des slides
		- Le nombre de colonne par page dans l'article
		- Un booléen spécifiant si la transcription vidéo est humaine ou automatique
	Elle construira au fur et à mesure un objet Document contenant tous les informations récoltées, qui sera ensuite écrit dans plusieurs fichiers html, spécifiés en paramètres :
		- Un fichier pour les paragraphes de l'article
		- Un fichier pour les passages (speechs) de la vidéo
		- Un fichier pour les pages de l'article
		- Un fichier pour les liens entre les paragraphes et les speechs
	"""
	def __init__(self):
		"""Instancie l'objet Document"""

		self.document = segment.Documents()

	def run(self, filePdf, fileTranscript, fileSlide, nbColonnePdf, humanTranscript):
		"""Lance dans l'ordre tous les traitements et remplie l'objet Document

		Les différents traitements, dans l'ordre, sont :
			-Le découpage de l'article en paragraphes
			-Le découpage de la vidéo en morceaux, appelés speechs
			-Le calcule des mesures de similarités entre les paragraphes et les speechs
		"""

		#Option pour le découpage de l'article (elles peuvent être modifiées)
		optionPdf = {"alinea" : True, "interligne" : True, "changementColonne" : True, "trierPolice" : False, "trierMargeGauche" : False};

		#Découpage de l'article
		traitePdf = traitementPdf.TraitementPdf(nbColonnePdf, filePdf, optionPdf)
		traitePdf.parsexml()
		traitePdf.formatResultat(self.document)

		#Découpage de la vidéo
		traiteVideo = traitementVideo.TraitementVideo(fileTranscript, fileSlide, humanTranscript)
		traiteVideo.traiter()
		traiteVideo.formatResultat(self.document)

		#Mesure de similarité
		sim = similarite.Similarite(self.document, "lemmatize")
		sim.analyse_resultat()

	

	def generateHtml(self, fileParagraphe, fileSpeech, filePage, fileAlignement):
		"""Génère des fichiers html à partir de l'objet Document"""

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



#On vérifie le nombre d'argument, puis on instancie et utilise la classe Main
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
