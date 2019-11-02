import datetime
from datetime import timedelta
import numpy as np

hora = 6
minutos = 0
segundos = 0

array_carreteras = []

array_carreterasleftRightBottomTop = []

carretera_id = []

def carga_carreteras():

	with open("city_information/limitesCarreteraTraducidosVilanovaILaGeltru.txt","r") as ficheroCarreteras:
		first = False		
		for carretera in ficheroCarreteras:
			totalDividido = carretera.split("@@@")
			nombreCarretera = totalDividido[0][:-1] #le quitamos el espacio del final al nombre
			carretera = totalDividido[1].split(" ")
			#Quitamos el primer elemento que hace referencia al id de la carretera			
			carretera_id.append(nombreCarretera)			
			carretera.pop(0)
			#Quitamos el \n del final
			carretera = carretera[:-2]
			#Pasamos a int el array
			carretera = list(map(int,carretera))
			#Agrupamos en parejas de dos el array para juntar en x,y las coordenadas
			n = 2
			carretera = [ carretera[i:i+n] for i in range(0, len(carretera), n) ]
			array_carreteras.append(carretera)
			max_x = carretera[0][0]
			min_x = carretera[0][0]
			max_y = carretera[0][1]
			min_y = carretera[0][1]
			for indice in range(len(carretera)):
				if(carretera[indice][0] > max_x):
					max_x = carretera[indice][0]
				if(carretera[indice][0] < min_x):
					min_x = carretera[indice][0]
				if(carretera[indice][1] > max_y):
					max_y = carretera[indice][1]
				if(carretera[indice][1] < min_y):
					min_y = carretera[indice][1]

			#print ("------------------------")
			#print (min_x,max_x,min_y,max_y)
			#print (carretera)
			#print ("------------------------")
			array_carreterasleftRightBottomTop.append([min_x,max_x,min_y,max_y])
			


def esta_dentro_carretera(x,y,poly):
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


def compruebaCercania(numCarretera,x,y):

	estaCerca = False
	#array_carreteras_maximo_minimo el [0] es el max y el [1] es el min

	if((array_carreterasleftRightBottomTop[numCarretera][0] <= x and array_carreterasleftRightBottomTop[numCarretera][1] >= x and \
		array_carreterasleftRightBottomTop[numCarretera][2] <= y and array_carreterasleftRightBottomTop[numCarretera][3] >= y)):

		estaCerca = True

	return estaCerca

def detecta_en_que_carretera(x,y):

	carreteraEncontrada = False
	contadorCarreteras = 0
	while(not carreteraEncontrada and contadorCarreteras<len(array_carreteras)):
		#TODO: Optimizacion. Comparar si la diferencia es muy grande respecto las coordenadas y si lo es, pasar a la siguiente		
		estaCerca = compruebaCercania (contadorCarreteras,x,y)
		if(estaCerca):
			carreteraEncontrada = esta_dentro_carretera(x,y,array_carreteras[contadorCarreteras])

		contadorCarreteras += 1

	valorReturn = contadorCarreteras
	if(not carreteraEncontrada):
		valorReturn = -1

	#else:
	#	print('Punto x,y:', x, y, 'no encontrada la carretera a la que corresponde')

	return valorReturn


def apunta_trafico_instante(instante):

	instante = instante.split(" ")
	#La estructura del fichero es x1 y1 color1 x2 y2 color2 ... xn yn colorn\n
	i = 0			

	arrayTraficoPorCarretera = [0] * len(array_carreteras)

	#print (array_carreteras_maximo_minimo)

	while i < len(instante):
		numCarretera = detecta_en_que_carretera(int(float(instante[i])),int(float(instante[i+1])))
		i+=3
		if(numCarretera!=-1):
			arrayTraficoPorCarretera[numCarretera]+=1
	#print(arrayTraficoPorCarretera)

	for i in range(len(array_carreteras)):
		print(carretera_id[i],":",arrayTraficoPorCarretera[i])
	
	print("Trafico total detectado:",sum(arrayTraficoPorCarretera))

def actualiza_hora():
	global segundos
	global minutos
	global hora
	segundos = segundos + 10
	if(segundos==60):
		minutos = minutos + 1
		if(minutos==60):
			hora = hora + 1
			if(hora==24):
				hora = 0

def apunta_trafico_dia(dia_traza):
	with open(dia_traza,"r") as trazaTotal:
		contador = 0
		for instante in trazaTotal:
			contador = contador + 1
			#if(contador == 3000):
			apunta_trafico_instante(instante)
			break
			actualiza_hora()

if __name__ == "__main__":

	dia_traza = "city_information/diaModificadoVilanova"
	carga_carreteras()
	#print(array_carreteras)
	apunta_trafico_dia(dia_traza)

