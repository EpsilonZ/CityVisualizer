#!/bin/bash

echo "Generando ruta con los parametros pasados"

echo "arg 1 $1"
echo "arg 2 $2"
echo "arg 3 $3"
echo "arg 4 $4"
echo "arg 5 $5"
echo "arg 6 $6"
echo "arg 6 $6"
echo "arg 7 $7"
echo "arg 8 $8"
echo "arg 9 $9"
echo "arg 10 $10"
echo "arg 11 $11"


echo "Numero de argumentos $#"

#part1="http://router.project-osrm.org/route/v1/foot/"
part1="http://192.168.1.40:5000/route/v1/walking/"
part2="$2,"
part3="$3;"
part4="$4,"
part5="$5;"
part6="$6,"
part7="$7;"
part8="$8,"
part9="$9;"
part10="$2,"
part11="$3"
part12="?steps=false&geometries=geojson"
total="$part1$part2$part3$part4$part5$part6$part7$part8$part9$part10$part11$part12"

#echo "$total"

peticion=$(curl $total)

valor=$(echo $peticion | wc -c)

if [ "$valor" -lt 50 ]
then
	while [ "$valor" -lt 50 ]
	do
		peticion=$(curl $total)
		valor=$(echo $peticion | wc -c)
		if [ "$valor" -ge 50 ]
		then
			echo $peticion > rutaEjemplo.json
			break
		fi
	done
else
	echo $peticion > rutaEjemplo.json
fi

#peticion ruta con los parametros que me pasan

#cat rutaEjemplo.json

./filtra_peticion $1

#hago el filtro para almacenarlo en el fichero de forma correcta



#curl "https://api.mapbox.com/directions/v5/mapbox/walking/-122.42,37.78;-77.03,38.91?steps=false&geometries=geojson&access_token=YOUR API KEY". THIS API IS FOR MAPBOX, IF YOU HAVE A VALID API KEY USE IT! IT HAS A FREE TIER!
