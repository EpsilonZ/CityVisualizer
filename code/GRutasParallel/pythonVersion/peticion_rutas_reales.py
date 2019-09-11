import random
import json
from random import randint
import requests

#TODA ESTA INFO SERA INTRODUCIDA POR BASE DE DATOS EN UN FUTURO


cantidadPersonasPorEdad=[549,571,558,681,698,705,713,785,729,732,696,746,754,684,649,706,669,598,642,615,575,618,569,668,631,666,653,641,\
667,660,711,802,827,852,893,1000,990,1094,1186,1165,1178,1176,1174,107,1114,1109,1086,1087,1136,1051,1083,1063,995,955,932,\
942,966,932,910,857,780,800,786,762,673,700,733,694,627,633,569,573,575,505,450,547,355,383,478,460,456,387,389,380,348,352,239,247,172,203,126,110,84,76,55,33,16,18,9,7,9]

tasaParo = 0.1181

#ESTUDIANTE

coordenadasCentrosEducativos = [[1.698466,41.225163],[1.690294,41.221331],[1.699993,41.225366],[1.721580,41.214520],[1.739690,41.227335],[1.682698,41.218490],[1.685359,41.205092],[1.735355,41.231337],[1.738789,41.221267],[1.707761,41.226915]]

horarioCentrosEducativos = [ [9.00,17.00],[9.00,15.00],[7.30,18.00],[9.00,12.30],[8.00,13.30],[8.00,14.30],[8.00,14.30],[8.30,12.30],[7.00,19],[8.00,14.30] ]

edadesPorCentro = [[0,24],[3,11],[3,11],[3,11],[3,16],[3,18],[3,21],[11,21],[11,24],[18,24]]

#TRABAJADOR

coordenadasCentrosTrabajo = [[1.696801,41.224012], [1.701366,41.215391], [1.699993,41.225366],[1.721580,41.214520],[1.739690,41.227335],[1.682698,41.218490],[1.685359,41.205092],[1.735355,41.231337],[1.738789,41.221267],[1.707761,41.226915]]

horarioCentrosTrabajo = [[6.20,14.00],[9.00,15.00],[7.30,18.00],[9.00,12.30],[8.00,13.30],[8.00,14.30],[8.00,14.30],[8.30,12.30],[7.00,19.00],[8.00,14.30] ]

#ZONAS DE OCIO

coordenadasLudico = [[1.699865,41.225515], [1.7314,41.2329], [1.7345,41.2315], [1.7251,41.2171], [1.72152,41.22387], [1.72191,41.21798], [1.72474,41.21865] ]


horarios = open("horarios.txt","w")
rutas = open("rutas.txt","w")


#COORDENADAS DE BARRIO

def get_porcentaje_poblacion_barrio(i):

	porcentaje=0.0

	if(i==0):
		porcentaje = 8.3823 / 100

	elif(i==1):
		porcentaje = 2.6057 / 100

	elif(i==2):
		porcentaje = 12.650821561 / 100

	elif(i==3):
		porcentaje = 1.105 / 100

	elif(i==4):
		porcentaje = 2.0175 / 100

	elif(i==5):
		porcentaje = 6.996907779 / 100

	elif(i==6):
		porcentaje = 5.901 / 100

	elif(i==7):
		porcentaje = 1.2733 / 100

	elif(i==8):
		porcentaje = 15.0852 / 100

	elif(i==9):
		porcentaje = 0.4593 / 100

	elif(i==10):
		porcentaje = 9.4131 / 100

	elif(i==11):
		porcentaje = 6.9241 / 100

	elif(i==12):
		porcentaje = 6.0768 / 100

	elif(i==13):
		porcentaje = 0.6897 / 100

	elif(i==14):
		porcentaje = 2.7754 / 100

	elif(i==15):
		porcentaje = 20.7239 / 100

	elif(i==16):
		porcentaje = 1.0868 / 100

	elif(i==17):
		porcentaje = 1.5749 / 100

	return porcentaje


def get_limites_barrio(i):

	limites=[[]]

	if(i==0):
		limites=[[1.7043,41.2208],[1.6976,41.2156],[1.70055,41.2127],[1.7079,41.2155]]
	
	elif(i==1):
		limites=[[1.72418,41.23307],[1.72748,41.2332],[1.72795,41.2305],[1.72479,41.2304]]

	elif(i==2):
		limites=[[1.7212,41.2204],[1.7394,41.2249],[1.7417,41.2192],[1.7243,41.2144]]

	elif(i==3):
		limites=[[1.723,41.2225],[1.7245,41.2229],[1.7243,41.2203],[1.7257,41.2208]]

	elif(i==4):
		limites=[[1.7249,41.2285],[1.7244,41.2301],[1.7297,41.2305],[1.7303,41.2285]]

	elif(i==5):
		limites=[[1.72803,41.22741],[1.7195,41.2248],[1.7258,41.2207],[1.733,41.223]]

	elif(i==6):
		limites=[[1.7037,41.2202],[1.7096,41.224],[1.7076,41.2259],[1.7025,41.2254],[1.6973,41.2284],[1.6913,41.2302],[1.6916,41.2259],[1.6934,41.2233],[1.6963,41.2206],[1.7005,41.2228]]

	elif(i==7):
		limites=[[1.6961,41.222],[1.6933,41.2239],[1.6854,41.2207],[1.6916,41.2152],[1.6956,41.2169]]

	elif(i==8):
		limites=[[1.7238,41.2213],[1.7337,41.2364],[1.7461,41.2222],[1.7242,41.2203]]

	elif(i==9):
		limites=[[1.74,41.23077],[1.74045,41.22994],[1.74279,41.23094],[1.74235,41.23181]]

	elif(i==10):
		limites=[[1.7034,41.2206],[1.7106,41.2247],[1.7165,41.2185],[1.7079,41.215]]

	elif(i==11):
		limites=[[1.7167,41.2278],[1.7198,41.2246],[1.72803,41.22741],[1.72203,41.22998]]

	elif(i==12):
		limites=[[1.7238,41.2212],[1.7255,41.2185],[1.7227,41.2174],[1.7163,41.219],[1.7252,41.2216]]

	elif(i==13):
		limites=[[1.6818,41.2052],[1.6872,41.2064],[1.6876,41.2048],[1.6829,41.2028]]

	elif(i==14):
		limites=[[1.7228,41.2174],[1.7146,41.2119],[1.7261,41.2134],[1.7231,41.217]]

	elif(i==15):
		limites=[[1.7106,41.2245],[1.7163,41.2189],[1.7238,41.2213],[1.7149,41.2272]]

	elif(i==16):
		limites=[[1.6758,41.2178],[1.6825,41.2212],[1.6849,41.2185],[1.6847,41.2163],[1.6797,41.2219]]

	elif(i==17):
		limites=[[1.7252,41.2363],[1.7285,41.2366],[1.7297,41.2339],[1.7258,41.2333]]

	return limites


def obten_coordenadasX(arrayCoords):
	
	arrayX = []

	for i in range(len(arrayCoords)):
		if(i%2==0):
			arrayX.append(arrayCoords[i])

	return arrayX


def obten_coordenadasY(arrayCoords):
	
	arrayY = []

	for i in range(len(arrayCoords)):
		if(i%2==1):
			arrayY.append(arrayCoords[i])

	return arrayY



def esta_dentro_barrio(x,y,poly):
# Funcion para detectar si un punto esta dentro de un poligono --> https://wrf.ecse.rpi.edu//Research/Short_Notes/pnpoly.html

    """
    x, y -- x and y coordinates of point
    poly -- a list of tuples [(x, y), (x, y), ...]
    """
    num = len(poly)
    i = 0
    j = num - 1
    c = False
    for i in range(num):
        if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
                                  (poly[j][1] - poly[i][1])):
            c = not c
        j = i
    return c


def arregla_hora(horaRaw):
	
	hora, minutos = str(horaRaw).split(".")
	minutos = int(minutos)
	hora = int(hora)
	while(minutos>59):
		minutos = minutos - 59
		hora = hora + 1

	if(minutos>=0 and minutos<=9): # Por ejemplo, 17.3 --> 17.03
		minutos = "0" + str(minutos)	

	horaArreglada = str(hora) + "." + str(minutos)

	return horaArreglada


def obten_rutina(edad,tasaParo,cantidadEdadDelBarrio,persona,coordsBarrio):

	casa = []

	casa.append(-1.0)
	casa.append(-1.0)
	casaAsignada= False

	while(casaAsignada==False):
		casa[0] = round(random.uniform(1.64,1.76),6)
		casa[1] = round(random.uniform(41.0,41.4),6)
		casaAsignada = esta_dentro_barrio(casa[0],casa[1],coordsBarrio)

	casa[0] = format(casa[0],'.6f')
	casa[1] = format(casa[1],'.6f')

	rutina=[]

	if(edad<=21):
		rutina = rutina_estudiante(casa)
	elif( (tasaParo*cantidadEdadDelBarrio) > persona ):
		rutina = rutina_parado(casa)
	elif(edad >= 67):
		rutina = rutina_jubilado(casa)
	else:
		rutina = rutina_trabajador(casa)

	return rutina

def rutina_estudiante(casa):

	rutina=[]

	colegioEscogido = randint(0,len(coordenadasCentrosEducativos)-1)

	horaPrimerPaso = format(horarioCentrosEducativos[colegioEscogido][0],'.2f') #sino si es .30 coge .3
	rutina.append([casa,horaPrimerPaso])

	coordsSegundoPaso = coordenadasCentrosEducativos[colegioEscogido]
	coordsSegundoPaso[0] = format(float(coordsSegundoPaso[0]),'.6f')
	coordsSegundoPaso[1] = format(float(coordsSegundoPaso[1]),'.6f')
	horaSegundoPaso = format(horarioCentrosEducativos[colegioEscogido][1],'.2f')
	rutina.append([coordsSegundoPaso,horaSegundoPaso])

	horaTercerPaso = format(float(horaSegundoPaso) + random.uniform(1,2),'.2f') #para obtener un decimal solo
	horaTercerPaso = arregla_hora(horaTercerPaso)
	
	zonaLudicaAleatoria = randint(0,len(coordenadasLudico)-1)
	coordsZonaLudica = coordenadasLudico[zonaLudicaAleatoria]
	coordsZonaLudica[0] = format(float(coordsZonaLudica[0]),'.6f')
	coordsZonaLudica[1] = format(float(coordsZonaLudica[1]),'.6f')
	rutina.append([coordsZonaLudica,horaTercerPaso])

	horaCuartoPaso = format(float(horaTercerPaso) + random.uniform(2,3),'.2f')
	horaCuartoPaso = arregla_hora(horaCuartoPaso)
	rutina.append([casa,horaCuartoPaso])

	return rutina,"estudiante"

def rutina_trabajador(casa):

	rutina=[]

	trabajoEscogido = randint(0,len(coordenadasCentrosTrabajo)-1)
	horaPrimerPaso = format(horarioCentrosTrabajo[trabajoEscogido][0],'.2f')
	horaPrimerPaso = arregla_hora(horaPrimerPaso)
	rutina.append([casa,horaPrimerPaso])

	coordenadasSegundoPaso = coordenadasCentrosTrabajo[trabajoEscogido]
	coordenadasSegundoPaso[0] = format(float(coordenadasSegundoPaso[0]),'.6f')
	coordenadasSegundoPaso[1] = format(float(coordenadasSegundoPaso[1]),'.6f')
	horaSegundoPaso = format(horarioCentrosTrabajo[trabajoEscogido][1],'.2f')
	horaSegundoPaso = arregla_hora(horaSegundoPaso)		
	rutina.append([coordenadasSegundoPaso,horaSegundoPaso])

	#tiempoCaminoHastaZonaOcio = AQUI SE HACE LA PETICION PARA CONOCER EL TIEMPO DE LLEGADA

	horaTercerPaso = format(float(horaSegundoPaso) + random.uniform(1,2),'.2f')
	horaTercerPaso = arregla_hora(horaTercerPaso)

	zonaLudicaAleatoria = randint(0,len(coordenadasLudico)-1)
	coordsZonaLudica = coordenadasLudico[zonaLudicaAleatoria]
	coordsZonaLudica[0] = format(float(coordsZonaLudica[0]),'.6f')
	coordsZonaLudica[1] = format(float(coordsZonaLudica[1]),'.6f')
	rutina.append([coordsZonaLudica,horaTercerPaso])
	
	
	horaCuartoPaso = format(float(horaTercerPaso) + random.uniform(2,3),'.2f')
	horaCuartoPaso = arregla_hora(horaCuartoPaso)
	rutina.append([casa,horaCuartoPaso])

	return rutina,"trabajador"

def rutina_jubilado(casa):

	rutina=[]

	primeraZonaDeOcioEscogida = randint(0,len(coordenadasLudico)-1)
	horaPrimerPaso = format(random.uniform(7,8),'.2f')
	horaPrimerPaso = arregla_hora(horaPrimerPaso)
	rutina.append([casa,horaPrimerPaso])

	coordenadasSegundoPaso = coordenadasLudico[primeraZonaDeOcioEscogida]
	coordenadasSegundoPaso[0] = format(float(coordenadasSegundoPaso[0]),'.6f')
	coordenadasSegundoPaso[1] = format(float(coordenadasSegundoPaso[1]),'.6f')
	horaSegundoPaso = format(random.uniform(14,15),'.2f')
	horaSegundoPaso = arregla_hora(horaSegundoPaso)
	rutina.append([coordenadasSegundoPaso,horaSegundoPaso])

	horaTercerPaso = format(float(horaSegundoPaso) + random.uniform(2,3),'.2f')
	horaTercerPaso = arregla_hora(horaTercerPaso)

	zonaLudicaAleatoria = randint(0,len(coordenadasLudico)-1)
	coordsZonaLudica = coordenadasLudico[zonaLudicaAleatoria]
	coordsZonaLudica[0] = format(float(coordsZonaLudica[0]),'.6f')
	coordsZonaLudica[1] = format(float(coordsZonaLudica[1]),'.6f')
	rutina.append([coordsZonaLudica,horaTercerPaso])

	horaCuartoPaso = format(float(horaTercerPaso) + random.uniform(2,3),'.2f')
	horaCuartoPaso = arregla_hora(horaCuartoPaso)
	rutina.append([casa,horaCuartoPaso])

	return rutina,"jubilado"

def rutina_parado(casa):

	rutina=[]

	primeraZonaDeOcioEscogida = randint(0,len(coordenadasLudico)-1)
	horaPrimerPaso = format(random.uniform(7,8),'.2f')
	horaPrimerPaso = arregla_hora(horaPrimerPaso)
	rutina.append([casa,horaPrimerPaso])

	coordenadasSegundoPaso = coordenadasLudico[primeraZonaDeOcioEscogida]
	coordenadasSegundoPaso[0] = format(float(coordenadasSegundoPaso[0]),'.6f')
	coordenadasSegundoPaso[1] = format(float(coordenadasSegundoPaso[1]),'.6f')
	horaSegundoPaso = format(random.uniform(14,15),'.2f')
	horaSegundoPaso = arregla_hora(horaSegundoPaso)
	rutina.append([coordenadasSegundoPaso,horaSegundoPaso])

	horaTercerPaso = format(float(horaSegundoPaso) + random.uniform(2,3),'.2f')
	horaTercerPaso = arregla_hora(horaTercerPaso)

	zonaLudicaAleatoria = randint(0,len(coordenadasLudico)-1)
	coordsZonaLudica = coordenadasLudico[zonaLudicaAleatoria]
	coordsZonaLudica[0] = format(float(coordsZonaLudica[0]),'.6f')
	coordsZonaLudica[1] = format(float(coordsZonaLudica[1]),'.6f')
	rutina.append([coordsZonaLudica,horaTercerPaso])

	horaCuartoPaso = format(float(horaTercerPaso) + random.uniform(2,3),'.2f')
	horaCuartoPaso = arregla_hora(horaCuartoPaso)
	rutina.append([casa,horaCuartoPaso])

	return rutina,"parado"


def escribe_en_fichero_horarios(rutina):

	for i in range(len(rutina)):
		lineaAescribir = str(rutina[i][0][0]) + " " + str(rutina[i][0][1]) + " " + str(rutina[i][1])
		if(i<len(rutina)-1):
			lineaAescribir+=" "		
		horarios.write(lineaAescribir)

	horarios.write("\n")


def arregla_formato_ruta(rutina,ruta,i):

	if(i==0):
		rutaTxt = str(ruta)
		rutaTxt = rutaTxt[:-1] # le quitamos el ultimo caracter ]
		#print(rutaTxt)
	else:
		rutaTxt = str(ruta)
		rutaTxt = rutaTxt[:-1]
		rutaTxt = rutaTxt[2:]
		rutaTxt = ", " + rutaTxt
		#print(rutaTxt)
		
	return rutaTxt

def arregla_hora_rutina(i,duracion,rutina):
		
	horaRutina = rutina[i][1]
	hora, minutos = rutina[i][1].split(".")
	minutos = int(minutos) - (float(duracion)/60)
	minutos = round(int(minutos))
	while(minutos<0):
		minutos = minutos + 59
		hora = int(hora) - 1

	if(minutos>=0 and minutos<=9): # Por ejemplo, 17.3 --> 17.03
		minutos = "0" + str(minutos)

	nuevaHoraRutina = str(hora) + "." + str(minutos)	

	return nuevaHoraRutina


def escribe_en_fichero_rutas(rutaPaso):

	rutas.write(rutaPaso)


def realiza_peticiones(rutina,tipo):

#http://192.168.1.41:5000/route/v1/walking/coordX1,coordY1;coordX2,coordY2?steps=false&geometries=geojson por ejemplo

	print(tipo)
	for i in range(len(rutina)):	
		if(i<len(rutina)-1):
			coordInicioX = rutina[i][0][0]
			coordInicioY = rutina[i][0][1]
			coordFinX = rutina[i+1][0][0]
			coordFinY = rutina[i+1][0][1]
			url = "http://192.168.1.41:5000/route/v1/walking/" + str(coordInicioX) + "," + str(coordInicioY) + ";" + str(coordFinX) + "," + str(coordFinY) + "?steps=false&geometries=geojson"			
			peticion = requests.get(url)
			datos = peticion.json()
			ruta = datos['routes'][0]['geometry']['coordinates']

			rutina[i][0][0] = format(ruta[0][0],'.6f')
			rutina[i][0][1] = format(ruta[0][1],'.6f')

			rutaPaso = arregla_formato_ruta(rutina,ruta,i)
			escribe_en_fichero_rutas(rutaPaso)

			if(i==0 and (tipo=="estudiante" or tipo=="trabajador")):
				duracion = datos['routes'][0]['duration']
				horaSalida = arregla_hora_rutina(i,duracion,rutina)
				rutina[i][1] = horaSalida
		else:
			rutina[i][0] = rutina[0][0]
			ultimoPunto = ", " + str(rutina[0][0]) + "]\n"
			escribe_en_fichero_rutas(ultimoPunto)

	return rutina

if __name__ == '__main__':

	print ("ESTAS EN EL GENERADOR DE RUTAS Y HORARIOS GPS, DEPENDE DEL SERVIDOR QUE TENGAS CONFIGURADO ESTO LLEVARA MAS O MENOS TIEMPO")

	totalHabitantes = 65972
	totalBarrios = 18
	divisionParaIgualar = (65972-64783) / totalBarrios


	for i in range(totalBarrios):
		coordsBarrio = get_limites_barrio(i)
		print("Barrio",i)
		for edad in range(len(cantidadPersonasPorEdad)):
			cantidadEdadDelBarrio = int(round(cantidadPersonasPorEdad[edad]*get_porcentaje_poblacion_barrio(i)))
			for persona in range(cantidadEdadDelBarrio):
				rutina,tipo = obten_rutina(edad,tasaParo,cantidadEdadDelBarrio,persona,coordsBarrio)
				rutina = realiza_peticiones(rutina,tipo)
				escribe_en_fichero_horarios(rutina)
				print(rutina)

				
		
		

