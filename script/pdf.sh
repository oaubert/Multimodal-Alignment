#!/bin/bash

#$1 : article au format pdf
#$2 : transcription de la vidéo
#$3 : transcription des slides
#$4 : nombre de colonnes par page dans l'article
#$5 : booleen, true si la transcription est humaine, false sinon
#$6 : chemin du dossier résultat

#Création du dossier résultat
mkdir $6

#Copie des fichiers initiaux
cp $1 $6/paper.pdf
cp $2 $6/transcript.xml
cp $3 $6/slide.xml

#Création du dossier pour les images du pdf
mkdir $6/img

#Génaration d'un fichier xml à partir de l'article
pdftohtml -xml $1 $6/pdf.xml

#Suppression des fichiers inutiles
rm -f $6/*.png

#Lancement du script
python main.py $6/pdf.xml $6/transcript.xml $6/slide.xml $4 $5 $6/paragraphe.html $6/speech.html $6/page.html $6/alignement.html $6/vocabulary.html

#Génération des images de l'article
convert -density 300 $1 $6/img/PICTURE.jpg

i=0

while [ -f "$6/img/PICTURE-$i.jpg" ]; do
	mv "$6/img/PICTURE-$i.jpg" "$6/img/PICTURE_$((i+1)).jpg"
	((i++))
done
