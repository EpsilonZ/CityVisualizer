#!/bin/bash


echo "Dime el nombre que quieres darle a tus trazas para la posterior visualizacion"

read nombre

#echo "Unificando trazas, espera..."

#./unifica_trazas.sh $nombre

echo "Generando mapa de calor, espera..."

nombreMapaCalor=$nombre'-colores.txt'

./filtra_colores $nombre $nombreMapaCalor

echo "Unificando mapa de calor con traza final, espera..."

python3 unifica_registro_mapaCalor.py $nombre $nombreMapaCalor $nombre'-unificado'

echo "Generando los tamaños de cada linea, espera..."

nombreFicheroSizes=$nombre'-unificado-sizes.txt'

awk '{print length($0) }' $nombre'-unificado' >> $nombreFicheroSizes

echo "Proceso completado con exito"
