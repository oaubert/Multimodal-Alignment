from xml.dom import minidom
import codecs
import sys


def begin(node):
	return float(node.getAttribute('b'))

def end(node):
	return float(node.getAttribute('e'))

def sI(node):
	return node.getAttribute('sI')

def text(node):
	return node.firstChild.nodeValue

def isIn(temps, interval):
	return temps >= interval['b'] and temps < interval['e']


class TraitementVideo:

	def __init__(self, file_in, file_slide, human):
		self.file_in = file_in
		self.file_slide = file_slide

		self.doc = minidom.parse(self.file_in)
		self.doc_body = self.doc.firstChild.getElementsByTagName('body')[0]
		self.slide = minidom.parse(self.file_slide)

		self.format = self.findFormat()
		self.duree = self.findDuree()
		self.human = bool(human)

	def traiter(self):
		self.splitTime = self.findSilenceAroundSlide(self.compareSlide(), self.splitSilence())


	def formatResultat(self, document):	

		for idSpeech, infoSpeech in self.splitTime.iteritems():
			text = infoSpeech['texte'].replace("~SILENCE~", "").replace("[SILENCE]", '').replace("\n", "")

			speech = document.addSpeech(idSpeech, infoSpeech['sI'], text)
			speech.temps(infoSpeech['begin'], infoSpeech['end'])

		document.infoDureeSpeech(self.duree)

			
	
	def ecrireResultat(self, file_out):

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




	def splitSilence(self):
	
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

		for e in [s for s in silence if s['duree'] > 0.5]:
			print e

		return silence


	def findSilenceAroundSlide(self, slides, silences):

		for key, word in slides.iteritems():
			silences_around_start = [e for e in silences if min(abs(word['begin'] - e['end']), abs(word['begin'] - e['begin'])) < 5.]

			max_silence = [e for e in silences_around_start if e['duree'] == max([f['duree'] for f in silences_around_start])][0]

			word['begin'] = max_silence['begin']


		return slides
			

	def compareSlide(self):
		
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

	def addVideo(self, transcript, video_info, slide_id):
		video = self.res.createElement('speech')
		transcript.appendChild(video)

		video.setAttribute('id', str(slide_id))
		video.setAttribute('id', str(slide_id))
		video.setAttribute('begin', str(video_info['begin']))
		video.setAttribute('end', str(video_info['end']))
		video.setAttribute('sI', str(video_info['sI']))
		
		video.appendChild(self.res.createTextNode(video_info['texte'].replace("~SILENCE~", "").replace("[SILENCE]", '').replace("\n", "")))


	def concatVideo(self, video1, video2):
		video1['end'] = video2['end']
		video1['texte'] += " " + video2['texte']

		
	def findSlide(self):
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

	def findFormat(self):
		return self.doc.firstChild.getElementsByTagName('head')[0].getElementsByTagName('tl:d')[0].getAttribute('aI')

	def findDuree(self):
		return self.doc.firstChild.getElementsByTagName('head')[0].getElementsByTagName('tl:d')[0].getAttribute('e')
		

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "Syntax: %s videofile slidefile" % sys.argv[0]
		exit(1)
	else:
		t = TraitementVideo(sys.argv[1], sys.argv[2], "res.xml")
		t.traiter()
		t.ecrireResultat()
