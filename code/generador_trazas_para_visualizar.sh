echo "Este programa te generara las trazas necesarias para visualizarlas. Cogere por defecto el archivo ficheroFiltrado.txt y horarios_filtrados.txt"

echo "ESTE PROCESO VA A LLEVAR MUCHO TIEMPO SEGUN EL TAMAÑO DE LAS TRAZAS. POR FAVOR, NO CORTES EL PROCESO"

echo "Generando puntos intermedios para darle continuidad a la visualizacion..."

python3 generaIntermedios/genera_intermedios.py ficheroFiltrado.txt ficheroIntermedios.txt

echo "Voy a generar el registro total de ejecucion..."

echo "Indica un nombre que le quieres asignar a la traza. Es aconsejable asignarle un nombre distintivo ya que posteriormente sera facil de identificar cual es cual"

read nombre

python3 genera_logTotal/genera_log.py ficheroIntermedios.txt horarios_filtrados.txt $nombre

echo "Voy a generar el mapa de calor..."

nombreMapaCalor=$nombre'-colores.txt'

Features/filtra_colores $nombre $nombreMapaCalor

echo "Unificando mapa de calor con el registro para una visualizacion mas agil, espera..."

python3 Features/unifica_registro_mapaCalor.py $nombre $nombreMapaCalor $nombre'-unificado'

echo "Generando los tamaños de cada linea, espera..."

nombreFicheroSizes=$nombre'-unificado-sizes.txt'

awk '{print length($0) }' $nombre'-unificado' >> $nombreFicheroSizes


echo "Voy a borrarte los ficheros creados de forma temporal, espera... (las trazas generadas no las borrare)"

rm $nombreMapaCalor
rm ficheroIntermedios.txt

echo "Proceso completado con exito, para visualizarlo copia las trazas que puedes observar en el directorio /var/www/html/Data"
