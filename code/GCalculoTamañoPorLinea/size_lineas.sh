#!/bin/bash

cat ficheroFiltradoHorarios.txt | while read line
do
	a=$(echo $line | wc -c)
	a=$((a-1))
	echo $a 
done
