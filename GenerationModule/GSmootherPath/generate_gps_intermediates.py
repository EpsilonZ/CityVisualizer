import sys
import math


ficheroUnificado = open(sys.argv[2],"w")

with open(sys.argv[1]) as ficheroRutasTraducidas:
	for lineaRuta in ficheroRutasTraducidas:
		lineaRutaParseada=''.join(lineaRuta)
		lineaRutaParseada=lineaRutaParseada.rstrip().split(" ")
		i=0
		while (i<len(lineaRutaParseada)) :

			if(i<(len(lineaRutaParseada)-2)):

				puntoAX = float(lineaRutaParseada[i])
				puntoAY = float(lineaRutaParseada[i+1])

				puntoBX = float(lineaRutaParseada[i+2])
				puntoBY = float(lineaRutaParseada[i+3])

				diff_X = puntoBX - puntoAX
				diff_Y = puntoBY - puntoAY

				distancia = int(math.sqrt( (puntoBX-puntoAX)**2 + (puntoBY-puntoAY)**2 ))

				#print("distance:", distancia)

                                #if you set this num higher final file is gonna be bigger but routes will be way smoother
				#puntosIntermedios = int(distancia/10)
				puntosIntermedios = 10

				interval_X = diff_X / (puntosIntermedios + 1)
				interval_Y = diff_Y / (puntosIntermedios + 1)

				ficheroUnificado.write(str(puntoAX) + " " + str(puntoAY) + " ")

				k=1

				while (k<=puntosIntermedios):

					puntoInterX = puntoAX+interval_X*k	
					puntoInterY = puntoAY+interval_Y*k 

					ficheroUnificado.write(str(puntoInterX) + " " + str(puntoInterY) + " ")

					k+=1

			else:
				puntoAX = float(lineaRutaParseada[i])
				puntoAY = float(lineaRutaParseada[i+1])
				ficheroUnificado.write(str(puntoAX) + " " + str(puntoAY) + " ")

			i+=2

		ficheroUnificado.write("\n")



