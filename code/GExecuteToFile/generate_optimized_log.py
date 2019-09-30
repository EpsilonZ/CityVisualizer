from pathlib import Path
import math
import sys


#simulation time
hour = 6
minutes = 0
seconds = 0

#
length = 0
count = 0

schedules = []

fileToWriteExecution = open(fileToWritePath,'w')

citizensFinished = {}

def get_schedules(schedulesFilePath):

	with open(schedulesFilePath) as schedulesFile:
		for citizenSchedule in schedulesFile:
			tmp=''.join(citizenSchedule)
			tmp=tmp.split(" ")
			arraySchedule=[]
			cont=0
			while(cont<len(tmp)):
				arraytmp=[]
				arraytmp.append(tmp[cont])
				arraytmp.append(tmp[cont+1])
				arraytmp.append(tmp[cont+2])
				cont+=3
				arraySchedule.append(arraytmp)
			arraySchedule[len(arraySchedule)-1][2] = arraySchedule[len(arraySchedule)-1][2][:-2] # we delete the \n 
			schedules.append(arraySchedule)
		schedulesFile.close()


def get_line(i):

	route = []
	citizen = 0
	with open(sys.argv[1]) as routesFile:
		for line in lines:
			try:
				lineSplitted = line.split(' ')
				citizenX = i * 2
				citizenY = citizenX + 1
				route.append([lineSplitted[citizenPosX],lineSplitted[citizenPosY]])
				citizen += 1
			except:
				citizensFinished[str(citizen)] = get_line(i-1)[citizen]
	return route

def init_indexes_citizens_array(totalCitizens):
	
	return [0] * totalCitizens


def areWeStillProcessingSameTimeCitizens(citizenCount):
	
	return citizenCount < length

def isExecutionDone(countFinished, citizenCount):

	return countFinished==length and citizenCount==length

def increase_time():

	seconds+=10
	if(seconds==60):
		minutes+=1
		seconds=0
		if(minutes==60):
			hour+=1
			minutes=0
		if(hour == 0 or hour == 1 or hour == 2 or hour == 3 or hour == 4 ):
			hour+=24
	fileToWriteExecution.write("\n")

	citizenCount=0
	linea+=1


if citizenHasRemainingSteps(citizenCount, citizenIndexes):

	return (str(citizenCount) in citizensFinished)



def main(routesFilePath, schedulesFilePath, fileToWritePath):

	get_schedules(schedulesFilePath)
	finished = False
	citizensIndexes = init_indexes_citizens_array(len(route))
	try:
		i = 0
		while(not finished):
			numberOfCitizensThatFinishedRoute = 0
			citizenCount = 0
			citizensArrayFinished = []
			route = get_line(i)
			
			#Citizen check
			if(citizenCount==0):
				numberOfCitizensThatFinishedRoute = 0

			if(citizenHasRemainingSteps(citizenCount, route, citizenIndexes[citizenCount])):
				index= citizensIndexes[citizenCount]
				posX = route[citizenCount][indice]
				posY = route[citizenCount][indice+1]

				elif(len(schedules[citizenCount])==0):
					ficheroLogTotal.write((posX + " " + posY))
					citizensIndexes[citizenCount]+=2

				elif(posX==schedules[elemento][0][0] and posY==schedules[citizenCount][0][1] or \
				     abs(float(posX) - float(schedules[citizenCount][0][0]) ) < 6 and abs(float(posY) - float(totalHorarios[elemento][0][1]) ) < 6 ):

					tmp=(totalHorarios[elemento][0][2] + "").split(".")

					scheduleHourCitizen = int(tmp[0])
					schedulesMinuteCitizen = int(tmp[1])			

					if((hour>scheduleHourCitizen) or (hour==scheduleHourCitizen and minutes >= schedulesMinuteCitizen)):
						ficheroLogTotal.write(posX + " " + posY)
						schedules[citizenCount].pop(0)
						citizenIndexes[elemento]+=2
					else:
						ficheroLogTotal.write((posX + " " + posY))

				else:
					ficheroLogTotal.write((posX + " " + posY))
					citizenIndexes[elemento]+=2

			else:
				lastPosX = citizensFinished[str(citizenCount)][0]
				lastPosY = citizensFinished[str(citizenCount)][1]
				
				ficheroLogTotal.write(lastPosX + " " + lastPosY)
				numberOfCitizensThatFinishedRoute+=1

			citizenCount = citizenCount + 1

			#Status checks
			if(isExecutionDone(contFinished, citizenCount)):
				ficheroLogTotal.close()
				finished=True
			elif(areWeStillProcessingSameTimeCitizens()):			
				fileToWriteExecution.write(" ")
			else:
				#just increase time
				increase_time(citizenCount)

			i = i + 1

print(get_line(0))
print(get_line(1))
