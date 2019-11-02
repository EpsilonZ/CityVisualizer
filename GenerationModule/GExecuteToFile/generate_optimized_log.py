from pathlib import Path
import math
import sys
import datetime


#simulation time
hour = 6
minutes = 0
seconds = 0

#
length = 0
count = 0

schedules = []

lastPositionOfCitizens = []
citizensFinishedMap = {}

routesLengthPerCitizenMap = {}

citizenHourToGoMap = {}

def get_schedules():
	i = 0
	with open(sys.argv[2]) as schedulesFile:
		for citizenSchedule in schedulesFile:
			tmp=''.join(citizenSchedule)

			if(i==0):
				tmp = tmp[1:] #did this because on my tests first char was hidden and it resulted in a \ue...\ hidden char. Just delete it
				i = 1 

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


def routes_length_per_citizen(routeFile):
	i = 0
	for line in routeFile.readlines():
		routesLengthPerCitizenMap[str(i)] = len(line.rstrip().split(' ')) #we delete the \n
		i = i + 1
	#print(routesLengthPerCitizenMap)

def get_citizen_pos(line, positionIndex):
	#to get the positionIndex coord we have to jump n*2-2 spaces until we find it
	#print(line)
	spaces_to_jump = 0
	if(positionIndex == 0 or positionIndex == 1):
		spaces_to_jump = positionIndex
	else:
		spaces_to_jump = positionIndex * 2 - 2 
	coordX = 0.0
	coordY = 0.0
	i = 0
	coordsFound = False
	while ( i < len(line) and not coordsFound):
		if (line[i] == ' '):
			spaces_to_jump = spaces_to_jump - 1

		elif (spaces_to_jump == 0 or spaces_to_jump == -1):
			tmpcoord = ""
			space_found = False
			while (not space_found): 
				if(line[i] != ' '):
					tmpcoord += line[i]
					i = i + 1
				else:
					space_found = True
					spaces_to_jump = spaces_to_jump - 1

			if (spaces_to_jump == -1):
				coordX = float(tmpcoord)
			else:
				#we write coordY and we finish iterating as we found the coords we needed
				coordY = float(tmpcoord)
				coordsFound = True
		i = i + 1

	return coordX, coordY

def get_citizens_step(citizensIndexes):

	finisheds = 0
	route = []
	citizen = 0
	with open(sys.argv[1]) as routesFile:

		for line in routesFile:

				#if citizen is still waiting to leave 
				if (str(citizen) in citizenHourToGoMap):
					route.append(lastPositionOfCitizens[citizen])
				else:
					citizenIndexX = citizensIndexes[citizen]
					citizenIndexY = citizenIndexX + 1

					if(routesLengthPerCitizenMap[str(citizen)] <= citizenIndexX):
						route.append(lastPositionOfCitizens[citizen])
						citizensFinishedMap[str(citizen)] = 1
						finisheds = finisheds + 1

					else:

						lineSplitted = line.rstrip().split(' ')
						#print("indexX: ", citizenIndexX, "len line: ", len(lineSplitted))
						citizenPosX = lineSplitted[citizenIndexX]
						citizenPosY = lineSplitted[citizenIndexY]

						# we implement a search pos function to not do a split to the whole line. this way is optimized. only works for low indexes
						#citX, citY = get_citizen_pos(line, citizenIndexX)

						#print("citizenPosX/Y from split ", citizenPosX, citizenPosY)		
						#print("citizenPosX/Y from looking for it", citX, citY)

						route.append([citizenPosX,citizenPosY])			
						lastPositionOfCitizens[citizen] = [citizenPosX, citizenPosY]

				citizen = citizen + 1

	return route, finisheds

def init_array_with_length(lengthValue):
	
	return ([0] * lengthValue)

def isExecutionDone(countFinished):
	global length
	return countFinished==length

def increase_time(fileToWrite):
	global seconds
	global minutes
	global hour

	seconds+=10
	if(seconds==60):
		minutes+=1
		seconds=0
		if(minutes==60):
			hour+=1
			minutes=0
		if(hour == 0 or hour == 1 or hour == 2 or hour == 3 or hour == 4 ):
			hour+=24
	fileToWrite.write("\n")


def citizenHasRemainingSteps(citizenCount):

	return (not str(citizenCount) in citizensFinishedMap)
	
def main(fileToWrite):

	global lastPositionOfCitizens 
	global length

	get_schedules()
	finished = False

	length = len(routesLengthPerCitizenMap.keys())
	citizensIndexes = init_array_with_length(length)
	lastPositionOfCitizens = init_array_with_length(length)

	while(not finished):

		citizenCount = 0
		#get_citizens_init_time = datetime.datetime.now()
		citizensNextStep, contFinished = get_citizens_step(citizensIndexes)
		#get_citizens_end_time = datetime.datetime.now()

		#c = get_citizens_end_time - get_citizens_init_time

		#print("get citizens steps took ", c.seconds,'seconds', 'or ', c.microseconds,'ms')

		#print(contFinished)
		print("time: ", hour,":",minutes,":",seconds)


		for_init_timer = datetime.datetime.now()

		for citizenCoords in citizensNextStep:

			#iteration_init_timer = datetime.datetime.now()

			index = citizensIndexes[citizenCount]
			posX = float(citizenCoords[0])
			posY = float(citizenCoords[1])

			#print("posx:", posX, " posY:", posY)
			#print("schedX:", schedules[citizenCount][0][0], " schedY:", schedules[citizenCount][0][1])
			
			
			if(citizenHasRemainingSteps(citizenCount)):

				if(len(schedules[citizenCount])==0):
					citizensIndexes[citizenCount]+=2

				elif(posX==schedules[citizenCount][0][0] and posY==schedules[citizenCount][0][1] or \
					 abs(posX - float(schedules[citizenCount][0][0]) ) < 6 and abs(posY - float(schedules[citizenCount][0][1]) ) < 6 ):

					tmp=(schedules[citizenCount][0][2] + "").split(".")

					scheduleHourCitizen = int(tmp[0])
					schedulesMinuteCitizen = int(tmp[1])			

					if((hour>scheduleHourCitizen) or (hour==scheduleHourCitizen and minutes >= schedulesMinuteCitizen)):
						schedules[citizenCount].pop(0)
						citizensIndexes[citizenCount]+=2
						if (str(citizenCount) in citizenHourToGoMap):
							citizenHourToGoMap.pop(str(citizenCount))
					else:
						citizenHourToGoMap[str(citizenCount)] = 1

				else:
					citizensIndexes[citizenCount]+=2

			else:
				citizensFinishedMap[str(citizenCount)] = 1
			
			fileToWrite.write(str(posX) + " " + str(posY))

			citizenCount = citizenCount + 1

			if(citizenCount < length):			
				fileToWrite.write(" ")

			#iteration_end_timer = datetime.datetime.now()

			#diff = 	iteration_end_timer - iteration_init_timer
			#print('iteration took ', diff.seconds,'seconds', 'or ', diff.microseconds,'ms')

		#for_end_timer = datetime.datetime.now()
		#diff_for_timers = for_end_timer - for_init_timer
		#print('for took ', diff_for_timers.seconds,'seconds', 'or ', diff_for_timers.microseconds,'ms')

		#Status checks
		if(isExecutionDone(contFinished)):
			fileToWrite.close()
			finished=True
		else:
			increase_time(fileToWrite)
		
if __name__ == "__main__":

	routesFile = open(sys.argv[1],'r')
	fileToWrite = open(sys.argv[3], 'w')

	#we tag routes for our optimizations. instead of loading all file we load columns by columns to get each step of each citizen
	routes_length_per_citizen(routesFile)
	#we'll use the routes tagged so we close the original one
	routesFile.close()

	#we execute 
	main(fileToWrite)

	fileToWrite.close()
