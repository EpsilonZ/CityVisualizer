from pathlib import Path
import math
import sys

totalRutas = []
longitud=0

with open(sys.argv[1]) as ficheroRutas:
	for lineaRuta in ficheroRutas:
		longitud+=1
		tmp=''.join(lineaRuta)
		tmp=tmp.split(" ")
		tmp.pop()
		totalRutas.append(tmp)

	ficheroRutas.close()

totalRutas.pop()

longitud= len(totalRutas)


totalHorarios=[]

with open(sys.argv[2]) as ficheroHorarios:
	for lineaHorario in ficheroHorarios:
		tmp=''.join(lineaHorario)
		tmp=tmp.split(" ")
		arrayLinea=[]
		cont=0
		while(cont<len(tmp)):
			arraytmp=[]
			arraytmp.append(tmp[cont])
			arraytmp.append(tmp[cont+1])
			arraytmp.append(tmp[cont+2])
			cont+=3
			arrayLinea.append(arraytmp)
		arrayLinea[len(arrayLinea)-1][2] = arrayLinea[len(arrayLinea)-1][2][:-2] # borramos el caracter \n del fichero
		totalHorarios.append(arrayLinea)
	ficheroHorarios.close()


fin=0

nombre= sys.argv[3]

ficheroLogTotal = open(nombre,"w")

linea=0
elemento=0
contAcabados=0

arrayAcabados = []

indices=[]

for i in range(longitud):
	indices.append(0)


print("Voy a comenzar a generar el registro de ejecución")

hora=6
minutos=0
segundos=0


while(fin!=1):

	if(elemento==0):
		contAcabados=0

	if(len(totalRutas[elemento]) > indices[elemento]):

		indice=indices[elemento]

		coordXAgente = totalRutas[elemento][indice]
		coordYAgente = totalRutas[elemento][indice+1]

		if(linea==0):

			ficheroLogTotal.write((totalRutas[elemento][0] + " " + totalRutas[elemento][1]))

	
		elif(len(totalHorarios[elemento])==0):

			ficheroLogTotal.write((coordXAgente + " " + coordYAgente))
			indices[elemento]+=2

		elif(len(totalHorarios[elemento]) == 4):

			horaAux = (totalHorarios[elemento][0][2] + "").split(".")
			horaHorario = int(horaAux[0])
			minutosHorario = int(horaAux[1])


			if(hora>horaHorario or (horaHorario==hora and minutos>=minutosHorario) ):

				ficheroLogTotal.write(coordXAgente + " " + coordYAgente)
				indices[elemento] += 2
				totalHorarios[elemento].pop(0)
			
			else:
				ficheroLogTotal.write(coordXAgente + " " + coordYAgente)
			
		elif(coordXAgente==totalHorarios[elemento][0][0] and coordYAgente==totalHorarios[elemento][0][1] or \
		     abs(float(coordXAgente) - float(totalHorarios[elemento][0][0]) ) < 6 and abs(float(coordYAgente) - float(totalHorarios[elemento][0][1]) ) < 6 ):

			horaAux=(totalHorarios[elemento][0][2] + "").split(".")

			horaHorario = int(horaAux[0])
			minutosHorario = int(horaAux[1])			

			if((hora>horaHorario) or (hora==horaHorario and minutos >= minutosHorario)):

				ficheroLogTotal.write(coordXAgente + " " + coordYAgente)
				totalHorarios[elemento].pop(0)
				indices[elemento]+=2
			else:
				ficheroLogTotal.write((coordXAgente + " " + coordYAgente))

		else:

			ficheroLogTotal.write((coordXAgente + " " + coordYAgente))
			indices[elemento]+=2

	else:
		coordUltimaX = totalRutas[elemento][indices[elemento]-2]
		coordUltimaY = totalRutas[elemento][indices[elemento]-1]
		ficheroLogTotal.write(coordUltimaX + " " + coordUltimaY)
		contAcabados+=1

	elemento+=1

	if(contAcabados==longitud and elemento==longitud):
		ficheroLogTotal.close()
		fin=1
	elif(elemento < longitud):
		ficheroLogTotal.write(" ")
	else:
		segundos+=10
		if(segundos==60):
			minutos+=1
			segundos=0
			if(minutos==60):
				hora+=1
				minutos=0
			if(hora == 0 or hora == 1 or hora == 2 or hora == 3 or hora == 4 ):
				hora+=24
		ficheroLogTotal.write("\n")

		elemento=0
		linea+=1


		
								
			
			
			
	
