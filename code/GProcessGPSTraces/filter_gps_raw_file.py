import re
import sys
import os

def main(rawFile, fileToWrite):
	with open(rawFile) as routesRawFile:
		outputFile = open(fileToWrite,'w+')
		for rawRoute in routesRawFile:
			route = rawRoute.rstrip().split(',')
			valueToWrite = ""
			i = 0
			for rawValue in route:
				value = rawValue.replace("[","").replace("]","").replace(" ","").replace("'","")
				valueToWrite = value
				if(i < len(route) - 1):
					valueToWrite = valueToWrite + " "
				outputFile.write(valueToWrite)
				i = i + 1
			outputFile.write('\n')

		#delete last '\n' as it creates an empty blank line
		outputFile.seek(outputFile.tell() - 1, os.SEEK_SET)
		outputFile.write('')
		outputFile.close()

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])
