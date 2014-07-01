#!/bin/bash

#$1 : pdf
#$2 : transcript
#$3 : slide
#$4 : nbColonnePdf
#$5 : humainTranscript
#$6 : dossierResultat

mkdir $6

cp $1 $6/paper.pdf
cp $2 $6/transcript.xml
cp $3 $6/slide.xml

mkdir $6/img

pdftohtml -xml $1 $6/pdf.xml

rm -f $6/*.png

python main.py $6/pdf.xml $6/transcript.xml $6/slide.xml $4 $5 $6/paragraphe.html $6/speech.html $6/page.html $6/alignement.html

convert -density 300 $1 $6/img/PICTURE.jpg

i=0

while [ -f "$6/img/PICTURE-$i.jpg" ]; do
	mv "$6/img/PICTURE-$i.jpg" "$6/img/PICTURE_$((i+1)).jpg"
	((i++))
done
