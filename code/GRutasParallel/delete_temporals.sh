#!/bin/sh

baseName="tempFile"
cont=0

while [ -e "$baseName$cont" ]
do
	rm $baseName$cont
	cont=$((cont+1))
done
