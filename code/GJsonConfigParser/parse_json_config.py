import sys
import os
import argparse
import json
import subprocess

#list admitted values by the json configuration
json_values = ["name", "description", "numberOfCitizens", "gpsTracing", "traceName", "visualizationTracing", "osrmServerIP", "osrmServerPort", "destinationDirectory"]

def parse_file(filePath):

	valuesMap = {}
	with open(filePath,'r') as jsonConfigFile:
		valuesMap = json.load(jsonConfigFile)

	return valuesMap

def check_parameters_correctness(json_user_values):
	#true if everything is correct
	correct = True

	if(json_user_values["visualizationTracing"] == False and json_user_values["gpsTracing"] == False):
		print("Both visualization tracing and gps tracing can't be false. At least one of them have to be true in order to generate the whole city")
		correct = False

	return correct

#####################################
#OS COMMANDS TO EXECUTE PROGRAMS / CONFIGURE FILES / DIRECTORIES FOR USER

def create_working_directory(destinationDirectory):

	subprocess.call(["sudo", "mkdir", "-p", destinationDirectory])

def get_scheduled_routes(osrmIP, osrmPort, citizensNumber):

	print(osrmIP, osrmPort, citizensNumber)
	subprocess.call(["python3","GScheduledRoutesParallel/pythonVersion/peticion_rutas_reales.py", str(osrmIP), str(osrmPort), str(citizensNumber)])

def move_scheduled_routes_to_working_directory(workingDir):

	subprocess.call(["sudo", "cp", "horarios.txt", "/var/www/html/Data"])
	subprocess.call(["sudo", "cp", "rutas.txt", "/var/www/html/Data"])

def open_brower_translating_coords_for_user():

	cmd = "google-chrome localhost/GeneradorPruebas.html"
	print("I'll open browser with localhost/GeneradorPruebas.html URL")
	subprocess.call(cmd, shell=True)

def move_translated_files_to_workingDir(workingDir, downloadsFolderBrowser):

	subprocess.call(["sudo", "mv", downloadsFolderBrowser+"/rutas_simples_traducidas.txt", workingDir+"filtered_routes.txt"])
	subprocess.call(["sudo", "mv", downloadsFolderBrowser+"/horarios_traducidos.txt", workingDir+"filtered_schedules.txt"])

def smooth_visualization_tracing(workingDir):

	subprocess.call(["python3", "GSmootherPath/genera_intermedios.py", workingDir+"filtered_routes.txt", workingDir+"filtered_smoothed_routes.txt"])

def wait_user_response():

	userFeedback = input("Press any key when you've already downloaded the files from the browser")

def get_free_memory():

	free_mem_in_kb = 0

	with open('/proc/meminfo') as file:
		for line in file:
		    if 'MemFree' in line:
		        free_mem_in_kb = line.split()[1]
		        break

	return free_mem_in_kb

def get_needed_mem_for_visualization_execution(workingDir):

	cmd = "sudo du -b " + workingDir+"filtered_smoothed_routes.txt | awk '{print $1}'"
	ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	output, err = ps.communicate()
	return output
	
def executeToFile_high_performance(workingDir, nameForTrace):

	cmd = "python3 GExecuteToFile/genera_log.py " + workingDir+"filtered_smoothed_routes.txt " + workingDir+"/filtered_schedules.txt " + workingDir+nameForTrace
	subprocess.call(cmd, shell=True)	

def executeToFile_low_performance(workingDir, nameForTrace):

	subprocess.call(["python3 GExecuteToFile/generatete_optimized_log.py " +workingDir+"filtered_smoothed_routes.txt "+ workingDir+"filtered_schedules.txt "+ workingDir+nameForTrace], shell=True)	

def executeToFile_visualization_tracing(workingDir, nameForTrace):

	freeMemoryAvailable = int (get_free_memory()) / 1024
	ramNeededForHighPerformanceExecution = int (get_needed_mem_for_visualization_execution(workingDir)) / 2048 

	if(freeMemoryAvailable > ramNeededForHighPerformanceExecution):
		userDecision = input("I've seen that you can run the high performance execution which will require " + str(ramNeededForHighPerformanceExecution) + "MB. If you say no it will run the less \
							  compute intensive program but it'll take way longer. Press y/Y for high performance and n/N for the alternative." )
		if(userDecision=="y" or userDecision=="Y"):
			executeToFile_high_performance(workingDir, nameForTrace)
		else:
			executeToFile_low_performance(workingDir, nameForTrace)
	else:
		executeToFile_low_performance()

def heatMap_visualization(workingDir, traceName):

	cmd = "Features/filtra_colores " + workingDir+traceName + " " + workingDir+traceName+"-colores.txt"
	subprocess.call(cmd, shell=True)

def sizesPerLine_visualization(workingDir, traceName):

	cmd = "awk '{print length($0)}' " + workingDir+traceName+"-unificado >> " + workingDir+traceName+"-unificado-sizes.txt"
	subprocess.call(cmd, shell=True)
	
def unify_heatMap_with_routes_trace_for_boosting_visualization(workingDir, traceName):

	cmd = "python3 Features/unifica_registro_mapaCalor.py " + workingDir+traceName + " " + workingDir+traceName+"-colores.txt" + " " + workingDir+traceName+"-unificado"
	subprocess.call(cmd, shell=True)

#####################################

def main(filePath):

	json_user_values = parse_file(filePath)
	if(check_parameters_correctness(json_user_values)):
		#create_working_directory(json_user_values["destinationDirectory"])
		get_scheduled_routes(json_user_values["osrmServerIP"], json_user_values["osrmServerPort"], json_user_values["numberOfCitizens"])
		move_scheduled_routes_to_working_directory(json_user_values["destinationDirectory"])
		if (json_user_values["visualizationTracing"]):
			open_brower_translating_coords_for_user()
			wait_user_response()
			move_translated_files_to_workingDir(json_user_values["destinationDirectory"], json_user_values["downloadsBrowserFolder"])
			smooth_visualization_tracing(json_user_values["destinationDirectory"])
			executeToFile_visualization_tracing(json_user_values["destinationDirectory"], json_user_values["traceName"])
			heatMap_visualization(json_user_values["destinationDirectory"], json_user_values["traceName"])
			unify_heatMap_with_routes_trace_for_boosting_visualization(json_user_values["destinationDirectory"], json_user_values["traceName"])
			sizesPerLine_visualization(json_user_values["destinationDirectory"], json_user_values["traceName"])
		if (json_user_values["gpsTracing"]):
			process_raw_routes_file()
			smooth_gps_routes_file()
			executeToFile_gps_tracing()

		#ask if user wants to delete tmp files. tell them that maybe they want to analyze them
	
		#if visualization was enabled open browser with visualization tool

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="This program will parse your json configuration and generate your city acording to your specifications")
	parser.add_argument("--jsonConfig", help="JSON configuration of the scenario you'll create")
	args = parser.parse_args()
	if(args.jsonConfig):
		main(args.jsonConfig)
	else:
		parser.print_help()


