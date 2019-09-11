import sys
import os


mapaCalor = open(sys.argv[2],"r")

ficheroUnificado = open(sys.argv[3],"w")

with open(sys.argv[1]) as ficheroRutas:
	for lineaRuta in ficheroRutas:
		
		lineaRutaParseada=''.join(lineaRuta)
		lineaRutaParseada=lineaRutaParseada.split(" ")
		lineaRutaParseada[len(lineaRutaParseada)-1] = lineaRutaParseada[len(lineaRutaParseada)-1][:-2]
		#lineaRutaParseada.pop() #al final se guarda un espacio y lo eliminamos

		lineaMapaCalor= mapaCalor.readline()
		lineaMapaCalor=''.join(lineaMapaCalor)
		lineaMapaCalor=lineaMapaCalor.split(" ")
		lineaMapaCalor.pop() # borro el espacio final con el caracter \n

		arrayUnificado = []

		contRuta=0
		contColor=0
		coordX=0
		coordY=0
		color=0

		#print(lineaRutaParseada[137694])
 
		while (contRuta<len(lineaRutaParseada)):
			coordX=lineaRutaParseada[contRuta]
			coordY=lineaRutaParseada[contRuta+1]
			color=lineaMapaCalor[contColor]

			ficheroUnificado.write(coordX + " " + coordY + " " + color)

			contRuta+=2
			contColor+=1
			
			if(contRuta<len(lineaRutaParseada)):
				ficheroUnificado.write(" ")

			#print (contRuta)
			#print (contColor)
			#print (len(lineaMapaCalor))


		ficheroUnificado.write("\n")
		


mapaCalor.close()

