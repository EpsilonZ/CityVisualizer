#!/bin/sh

cont=1
formato=".txt"
nombreTraza=$1

while [ -e "$cont$formato" ]
do
	echo "Existe fichero $cont$formato"
	cat $cont$formato >> $nombreTraza
	rm $cont$formato	
	cont=$((cont+1))

done
