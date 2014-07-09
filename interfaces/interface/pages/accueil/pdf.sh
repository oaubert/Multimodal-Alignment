#!/bin/bash

#$1 : pdf
#$2 : dossier
#$3 : nbColonne
#$4 : xml

pdftohtml -xml $1 cmd.xml

rm -f *.png

python traitePdf.py $3
mv conf.xml $2
cp $2/conf.xml $2/editer/

convert -density 300 $1 $2/img/PICTURE.jpg

i=0

while [ -f "$2/img/PICTURE-$i.jpg" ]; do
	mv "$2/img/PICTURE-$i.jpg" "$2/img/PICTURE_$((i+1)).jpg"
	((i++))
done
