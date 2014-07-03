# -*- coding: utf-8 -*-

"""Ce module permet de traiter le fichier de transcription de la vidéo en le comparant au fichier de transcription des slides pour découper le texte de la vidéo en speech selon les temps de changement des slides"""

from xml.dom import minidom
import codecs
import sys


def begin(node):
	"""Renvoie le temps de début d'un segment"""
	return float(node.getAttribute('b'))

def end(node):
	"""Renvoie le temps de fin d'un segment"""
	return float(node.getAttribute('e'))

def sI(node):
	"""Renvoie l'id d'un segment"""
	return node.getAttribute('sI')

def text(node):
	"""Renvoie le texte d'un segment"""
	return node.firstChild.nodeValue

def isIn(temps, interval):
	"""Renvoie vrai si temps appartient à interval, faux sinon

	Pour les bornes, le début de l'interval est inclus, la fin est exclue
	"""
	return temps >= interval['b'] and temps < interval['e']


class TraitementVideo:
	"""Permet d'extraire de découpé la transcription de la vidéo en speech

	Pour cela, on utilisera le fichier de transcription des slides pour trouver les temps de début et de fin de chaque slide, pour ensuite découper la transcription de la vidéo en morceaux, sur ces temps.
	"""

	def __init__(self, file_in, file_slide, human):
		"""Initialise le traitement

		Parse les fichiers d'entrées, et récupère les données nécessaire.
		Entrée :
			-file_in : transcription de la vidéo
			-file_slide : transcription des slides
			-human : "True" si la transcription est humaine, "False" si elle est automatique
		"""

		self.file_in = file_in
		self.file_slide = file_slide

		self.doc = minidom.parse(self.file_in)
		self.doc_body = self.doc.firstChild.getElementsByTagName('body')[0]
		self.slide = minidom.parse(self.file_slide)

		self.format = self.findFormat()
		self.duree = self.findDuree()
		self.human = (human in ["True", "true", "0"])


	def findFormat(self):
		"""Renvoie le format de la transcription

		Si la transcription est humaine, il est posible d'avoir plusieurs formats (sur les transcriptions de translectures) :
			-emlDecoder : c'est le cas pour les conférences en anglais
			-XEROX : c'est le cas pour les transcriptions traduites en anglais à partir des conférences slovènes
		"""
		return self.doc.firstChild.getElementsByTagName('head')[0].getElementsByTagName('tl:d')[0].getAttribute('aI')

	def findDuree(self):
		"""Renvoie la durée de la transcription"""
		return self.doc.firstChild.getElementsByTagName('head')[0].getElementsByTagName('tl:d')[0].getAttribute('e')



	def traiter(self):
		"""Détermine les temps de découpe des speechs"""
		self.splitTime = self.findSilenceAroundSlide(self.compareSlide(), self.splitSilence())


	#CompareSlide

	def compareSlide(self):
		"""Découpe la transcription de la vidéo d'après les temps des slides

		Sortie : la transcription découpée, en précisant le début, la fin, l'id et le textes
		"""

		temps_slide = self.findSlide()

		if self.format == "emlDecoder" and self.human == False:
			nodes = [w for w in [self.doc_body.getElementsByTagName('tl:w')]][0]
		elif self.format == "XEROX" or self.human == True:
			nodes = [p for p in [s for s in [self.doc_body.getElementsByTagName('tl:s')]][0] if p.hasAttribute('aT') and p.getAttribute('aT') == 'human']



		temps_slide.append({'sI' : temps_slide[-1]['sI'], 'b' : temps_slide[-1]['e'], 'e' : end(nodes[-1])})


		bloc_video = {}

		for v in nodes:
			paire = [{'id' : int(s['id']), 'video' : {'begin' : begin(v), 'end' : end(v), 'sI' : int(s['sI']), 'texte' : text(v)}} for s in filter(lambda x : isIn(begin(v), x), temps_slide)][0]
			
			if paire['id'] in bloc_video:
				self.concatVideo(bloc_video[paire['id']], paire['video'])
			else:
				bloc_video[paire['id']] = paire['video']
			

		return bloc_video


	def concatVideo(self, video1, video2):
		"""Concatène deux passages de vidéo

		On modifie en place video1 pour qu'il inclu video2, c'est-à-dire que la fin de video1 deviennent celle de video2, et que le texte soit la concaténation des deux.
		Attention, on suppose que video2 arrive après video1, et qu'il n'y a pas de trou entre les deux.
		"""
		video1['end'] = video2['end']
		video1['texte'] += " " + video2['texte']

		
	def findSlide(self):
		"""Trouve les temps de début et de fin des slides

		On fait attention à gérer les cas où il y aurait un trou dans les slides (la fin de l'un n'est pas en même temps que le début du suivant), ce qui se passe surtout au tout début : le conférencier commence à parler avant le premier slide. 
		Ainsi, pour chaque période découpé, on a :
			-id : un identifiant unique
			-sI : id de segment, qui correspond à l'id du slide correspondant, ou zéro si il n'y a pas de slide correspondant
			-b : temps de début
			-e : temps de fin

		Sortie : un tableau de ces découpes
		"""

		nodes_slides = self.slide.firstChild.getElementsByTagName('body')[0].getElementsByTagName('tl:s')
	
		if begin(nodes_slides[0]) == 0.:
			temps_slide = [{'id' : 0, 'sI' : sI(nodes_slides[0]), 'b' : begin(nodes_slides[0]), 'e' : end(nodes_slides[0])}]
			id_ = 1
		else:
			temps_slide = [{'id' : 0, 'sI' : '0', 'b' : 0., 'e' : begin(nodes_slides[0])}, {'id' : 1, 'sI' : sI(nodes_slides[0]), 'b' : begin(nodes_slides[0]), 'e' : end(nodes_slides[0])}]
			id_ = 2

		for current in nodes_slides[1:]:
			if temps_slide[-1]['e'] != begin(current):
				temps_slide.append({'id' : id_, 'sI' : '0', 'b' : temps_slide[-1]['e'], 'e' : begin(current)})
				id_ += 1

			temps_slide.append({'id' : id_, 'sI' : sI(current),  'b' : begin(current), 'e' : end(current)})
			id_ += 1

		return temps_slide



	#SplitSilence

	def splitSilence(self):
		"""Trouve les temps silences dans la vidéo

		Sortie : les informations sur les silences (début, fin, durée)
		"""

		if self.format == "emlDecoder":
			nodes = [w for w in [self.doc_body.getElementsByTagName('tl:w')]][0]
		elif self.format == "XEROX":
			nodes = [s for s in [self.doc_body.getElementsByTagName('tl:s')]][0]
		
		silence = [{'begin' : 0., 'end' : begin(nodes[0]), 'duree' : begin(nodes[0])}]

		previousWord = nodes[0]

		for word in nodes[1:]:
			if text(word) != "~SILENCE~" and text(word) != "[SILENCE]":
				silence.append({'begin' : end(previousWord), 'end' : begin(word), 'duree' : begin(word) - end(previousWord)})
				previousWord = word

		#Affichage
		#for e in [s for s in silence if s['duree'] > 0.5]:
		#	print e

		return silence



	#FindSilenceAroundSlide

	def findSilenceAroundSlide(self, slides, silences):
		"""Trouve les plus grands silences autour des temps de changement de slide

		Le problème de découper la trancription sur les temps de changement de slide est qu'on peut tomber au milieu d'une phrase ou d'un discours. On va donc chercher les plus grands silences autour de ces temps, et prendre ces silences comme point de découpe.
		On cherche dans un intervalle de 5 secondes autour des temps des slides

		Entrée :
			-slides : les informations sur les slides
			-silences : les informations sur les silences
		Sortie : Les informations sur les slides en ayant changé les informations de début et/ou de fin (par rapport aux meilleurs silences)
		"""

		for key, word in slides.iteritems():
			silences_around_start = [e for e in silences if min(abs(word['begin'] - e['end']), abs(word['begin'] - e['begin'])) < 5.]

			max_silence = [e for e in silences_around_start if e['duree'] == max([f['duree'] for f in silences_around_start])][0]

			word['begin'] = max_silence['begin']


		return slides



	#Résultats	

	def formatResultat(self, document):	
		"""Prend un objet Documents (voir segment.py) et y ajoute tous les speechs trouvés"""

		for idSpeech, infoSpeech in self.splitTime.iteritems():
			text = infoSpeech['texte'].replace("~SILENCE~", "").replace("[SILENCE]", '').replace("\n", "")

			speech = document.addSpeech(idSpeech, infoSpeech['sI'], text)
			speech.temps(infoSpeech['begin'], infoSpeech['end'])

		document.infoDureeSpeech(self.duree)



	#Écriture en xml
	
	def ecrireResultat(self, file_out):
		"""Écrit les résultats dans un fichier au format xml"""

		self.res = minidom.Document()

		transcript = self.res.createElement('transcript')

		self.res.appendChild(transcript)

		
		for k,v in splitTime.iteritems():
			self.addVideo(transcript, v, k)

		transcript.setAttribute('nbSpeech', str(len(transcript.childNodes)))
		transcript.setAttribute('duree', self.duree)

		fichier = codecs.open(file_out, 'w', "utf-8")
		
		fichier.write(self.res.toprettyxml())
		fichier.close()


	def addVideo(self, transcript, video_info, slide_id):
		"""Ajoute un noeud xml pour un speech"""

		video = self.res.createElement('speech')
		transcript.appendChild(video)

		video.setAttribute('id', str(slide_id))
		video.setAttribute('begin', str(video_info['begin']))
		video.setAttribute('end', str(video_info['end']))
		video.setAttribute('sI', str(video_info['sI']))
		
		video.appendChild(self.res.createTextNode(video_info['texte'].replace("~SILENCE~", "").replace("[SILENCE]", '').replace("\n", "")))


		

if __name__ == '__main__':
	if len(sys.argv) != 4:
		print "Syntax: %s videofile slidefile humanTranscript" % sys.argv[0]
		exit(1)
	else:
		t = TraitementVideo(sys.argv[1], sys.argv[2], sys.argv[3])
		t.traiter()
		t.ecrireResultat()
