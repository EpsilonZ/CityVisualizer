#!/bin/bash

#echo "Generando ruta con los parametros pasados"

#echo "arg 0 $0"
#echo "arg 1 $1"
#echo "arg 2 $2"
#echo "arg 3 $3"
#echo "arg 4 $4"
#echo "arg 5 $5"
#echo "arg 6 $6"
#echo "arg 6 $6"
#echo "arg 7 $7"
#echo "arg 8 $8"
#echo "arg 9 $9"
#echo "arg 10 ${10}"
#echo "arg 11 ${11}"


#echo "Numero de argumentos $#"

#part1="http://router.project-osrm.org/route/v1/foot/"
part1="http://192.168.1.41:5000/route/v1/walking/"
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


partetest="$5"
peticionTiempoPrimerPaso="$part1$part2$part3$part4$partetest$part12"

#echo $peticionTiempoPrimerPaso

peticion=$(curl $peticionTiempoPrimerPaso 2>/dev/null)

tiempoprimerpaso=$(echo $peticion | jq -r '.routes[].duration')

horaPrimerPaso=${14}

horaDividida=(${IN//;/ })

minutos=${horaDividida[0]}
hora=${horaDividida[1]}

minutos=$(($minutos-$tiempoprimerpaso))

if [ ${horaDividida[0]} < $tiempoprimerpaso ]
then
	hora=$((${horaDividida[0]}+1))
fi

horaPr="$hora$minutos"

echo $horaPr

peticion=$(curl $total 2>/dev/null)



echo "$2 $3 ${14} $4 $5 ${15} $6 $7 ${16} $8 $9 ${17}" >> ${13} 

#echo "$total"

peticion=$(curl $total 2>/dev/null )

#echo $peticion

valor=$(echo $peticion | wc -c)

if [ "$valor" -lt 50 ]
then
	while [ "$valor" -lt 50 ]
	do
		peticion=$(curl $total 2>/dev/null )
		valor=$(echo $peticion | wc -c)
		if [ "$valor" -ge 50 ]
		then
			echo $peticion > ${10}
			break
		fi
	done
else
	echo $peticion > ${10}
fi

#peticion ruta con los parametros que me pasan

#cat rutaEjemplo.json

python parsea_json.py $1 ${10}

#hago el filtro para almacenarlo en el fichero de forma correcta




