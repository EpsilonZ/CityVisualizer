from pathlib import Path
import math
import sys

totalRutas = []
longitud=0

with open(sys.argv[1]) as ficheroRutas:
	for lineaRuta in ficheroRutas:
		longitud+=1
		#print(longitud)
		tmp=''.join(lineaRuta)
		tmp=tmp.split(" ")
		tmp.pop()
		totalRutas.append(tmp)

	ficheroRutas.close()

totalRutas.pop()

longitud= len(totalRutas)

#print (longitud)

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

#print (totalRutas[longitud-1])
#print (totalRutas[longitud-2])

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

lineaAescribir=""

while(fin!=1):
	


	#print (elemento)

	#if(contAcabados==68006):
	#	for i in range (longitud):
	#		if(len(totalHorarios[i]) > 0):
	#			indice=indices[i]
	#			print("Persona:",i)
	#			print("Indice:",indice,". Longitud ruta:",len(totalRutas[i]))
	#			print(totalHorarios[i][0][0],totalHorarios[i][0][1])
	#			print(totalRutas[i][indice],totalRutas[i][indice+1])


	if(elemento==0):
		contAcabados=0
		#arrayAcabados=[]

	if(len(totalRutas[elemento]) > indices[elemento]):

		indice=indices[elemento]

		coordXAgente = totalRutas[elemento][indice]
		coordYAgente = totalRutas[elemento][indice+1]

		if(linea==0):
			#print ("LINEA0","ELEMENTO",elemento, "LINEA", linea)
			lineaAescribir+=(totalRutas[elemento][0] + " " + totalRutas[elemento][1])
			ficheroLogTotal.write((totalRutas[elemento][0] + " " + totalRutas[elemento][1]))
			#indices[elemento]+=2		
	
		elif(len(totalHorarios[elemento])==0):
			#print ("LEN HORARIOS 0","ELEMENTO",elemento, "LINEA", linea)
			lineaAescribir+=(coordXAgente + " " + coordYAgente)
			ficheroLogTotal.write((coordXAgente + " " + coordYAgente))
			indices[elemento]+=2

		elif(len(totalHorarios[elemento]) == 4):

			horaAux = (totalHorarios[elemento][0][2] + "").split(".")
			horaHorario = int(horaAux[0])
			minutosHorario = int(horaAux[1])


			if(hora>horaHorario or (horaHorario==hora and minutos>=minutosHorario) ):
				#print ("PUEDE SALIR PUNTO INICIAL 4 PUNTOS","ELEMENTO",elemento, "LINEA", linea)
				#print ("Longitud horarios antes de borrar este", len(totalHorarios[elemento]))
				#print (hora,minutos)
				#print (horaHorario,minutosHorario)
				ficheroLogTotal.write(coordXAgente + " " + coordYAgente)
				indices[elemento] += 2
				totalHorarios[elemento].pop(0)
			
			else:
				ficheroLogTotal.write(coordXAgente + " " + coordYAgente)
			
		elif(coordXAgente==totalHorarios[elemento][0][0] and coordYAgente==totalHorarios[elemento][0][1] or abs(float(coordXAgente) - float(totalHorarios[elemento][0][0]) ) < 6 and abs(float(coordYAgente) - float(totalHorarios[elemento][0][1]) ) < 6 ):

			horaAux=(totalHorarios[elemento][0][2] + "").split(".")

			horaHorario = int(horaAux[0])
			minutosHorario = int(horaAux[1])			

			if((hora>horaHorario) or (hora==horaHorario and minutos >= minutosHorario)):
				#print ("PUEDE SALIR DE SU PUNTO INTERES","ELEMENTO",elemento, "LINEA", linea)
				#print ("Longitud horarios antes de borrar este", len(totalHorarios[elemento]))
				#print (hora,minutos)
				#print (horaHorario,minutosHorario)
				lineaAescribir+=(coordXAgente + " " + coordYAgente)
				ficheroLogTotal.write(coordXAgente + " " + coordYAgente)
				totalHorarios[elemento].pop(0)
				indices[elemento]+=2
			else:
				#print ("TIENE QUE ESPERAR HORARIO","ELEMENTO",elemento, "LINEA", linea)
				lineaAescribir+=(coordXAgente + " " + coordYAgente)
				ficheroLogTotal.write((coordXAgente + " " + coordYAgente))

		else:
			#print(abs(float(coordXAgente) - float(totalHorarios[elemento][0][0]) ) < 6 )
			#print(abs(float(coordYAgente) - float(totalHorarios[elemento][0][1]) ) < 6 )
			#print(float(coordYAgente),float(totalHorarios[elemento][0][1]))
			#print ("AVANZA YA QUE NO ES PUNTO INTERES","ELEMENTO",elemento, "LINEA", linea)
			lineaAescribir+=(coordXAgente + " " + coordYAgente)
			ficheroLogTotal.write((coordXAgente + " " + coordYAgente))
			indices[elemento]+=2

	else:
		coordUltimaX = totalRutas[elemento][indices[elemento]-2]
		coordUltimaY = totalRutas[elemento][indices[elemento]-1]
		ficheroLogTotal.write(coordUltimaX + " " + coordUltimaY)
		#print ("RUTA ACABADA, APUNTA ULTIMO","ELEMENTO",elemento, "LINEA", linea)
		lineaAescribir+=(coordUltimaX + " " + coordUltimaY)
		contAcabados+=1
		#arrayAcabados.append(elemento)
		#print("acabado: " + str(elemento))

	elemento+=1

	#print(elemento)

	if(contAcabados==longitud and elemento==longitud):
		ficheroLogTotal.close()
		fin=1
	elif(elemento < longitud):
		ficheroLogTotal.write(" ")
	else:

		#print(lineaAescribir)
		lineaAescribir=""
		#minutos+=1
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

		#print("NUEVA ITERACION")
		elemento=0
		#if(contAcabados==68006):
		#	print (totalHorarios)
		#print(contAcabados)
		#print ("Hora",hora,":",minutos)
		#arrayAcabados.sort()
		#print(arrayAcabados)
		#if(linea==5):
		#	break
		linea+=1


		
								
			
			
			
	
