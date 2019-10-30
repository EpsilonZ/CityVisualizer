echo "This program will generate your city, please, be patient since we have to look a lot of steps"
echo "Now I'll generate all the scheduled routes. FIRST STEP"

python3 GScheduledRoutesParallel/pythonVersion/peticion_rutas_reales.py "192.168.1.42" "5000" 1

echo "Scheduled routes have been generated. I'll copy your generated files to /var/www/html/Data to process them."

sudo cp horarios.txt /var/www/html/Data
sudo cp rutas.txt /var/www/html/Data

echo "Please open this URL in your browser since some process needs to be done. http://localhost/GeneradorPruebas.html"
google-chrome localhost/GeneradorPruebas.html

echo "Press any key when you have downloaded the two files from the browser"

read userfeedback

echo "I'll copy the two generated files to this directory to keep processing. You won t need to do anything else for me."

sudo mv ~/Descargas/rutas_simples_traducidas.txt ficheroFiltrado.txt
sudo mv ~/Descargas/horarios_traducidos.txt horarios_filtrados.txt

echo "I'll create smoother paths to create a more pleasant visualization and improve analytics..."

echo "Generating smoothing for visualization"
python3 GSmootherPath/genera_intermedios.py ficheroFiltrado.txt ficheroIntermedios.txt

echo "Generating smoothing for gps analysis"

echo "Processing raw routes file..."
python3 GProcessGPSTraces/filter_gps_raw_file.py rutas.txt rutas_processed.txt
echo "Smoothing gps file..."
python3 GSmootherPath/generate_gps_intermediates.py rutas_processed.txt rutas_intermedios.txt

echo "I'm going to do the execution to the file now..."

echo "Please give this simulation a name. Choose a good one since you will know them based on the name"

read nombre

echo "THIS TAKES A LOT OF RAM SO YOU MAY GET AN ERROR IF YOU DONT HAVE ENOUGH!"
echo "Note: If you happen to have your process killed is due to a ram error. See README.md to know how to solve it"

echo "Executing to file for visualization"
#python3 GExecuteToFile/genera_log.py ficheroIntermedios.txt horarios_filtrados.txt $nombre
python3 GExecuteToFile/generate_optimized_log.py ficheroIntermedios.txt horarios_filtrados.txt $nombre

echo "Execution to file for gps analysis"
python3 GExecuteToFile/generate_optimized_log.py rutas_intermedios.txt horarios.txt $nombre'gps'


echo "Ill create the heatmap now..."

nombreMapaCalor=$nombre'-colores.txt'

Features/filtra_colores $nombre $nombreMapaCalor

echo "Unifying heatmap and execution written to the file to boost the visualization and improve analytics, wait..."

python3 Features/unifica_registro_mapaCalor.py $nombre $nombreMapaCalor $nombre'-unificado'

echo "Generating line sizes..."

nombreFicheroSizes=$nombre'-unificado-sizes.txt'

awk '{print length($0) }' $nombre'-unificado' >> $nombreFicheroSizes


echo "Ill delete all temporal files I've created you don't need anymore, wait..."

rm $nombreMapaCalor
rm ficheroIntermedios.txt
rm $nombre
rm ficheroFiltrado.txt
rm horarios_filtrados.txt


echo "Process finished with complete success. I'll move this to your /var/www/html/Data so you can visualize it!"

sudo mv $nombre'-unificado' /var/www/html/Data
sudo mv $nombre'-unificado-sizes.txt' /var/www/html/Data

echo "Head to http://localhost/SimulacionFinal.html and then click Seleccionar archivo and select your generated traces with the name you have probably wrote (navigate to /var/www/html/Data)"
google-chrome localhost/SimulacionFinal.html

