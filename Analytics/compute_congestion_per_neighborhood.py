import os
import sys

def get_neighborhood_boundingBox(i):

	boundingBox=[[]]

	if(i==0):
		boundingBox=[[1.7043,41.2208],[1.6976,41.2156],[1.70055,41.2127],[1.7079,41.2155]]

	elif(i==1):
		boundingBox=[[1.72418,41.23307],[1.72748,41.2332],[1.72795,41.2305],[1.72479,41.2304]]

	elif(i==2):
		boundingBox=[[1.7212,41.2204],[1.7394,41.2249],[1.7417,41.2192],[1.7243,41.2144]]

	elif(i==3):
		boundingBox=[[1.723,41.2225],[1.7245,41.2229],[1.7243,41.2203],[1.7257,41.2208]]

	elif(i==4):
		boundingBox=[[1.7249,41.2285],[1.7244,41.2301],[1.7297,41.2305],[1.7303,41.2285]]

	elif(i==5):
		boundingBox=[[1.72803,41.22741],[1.7195,41.2248],[1.7258,41.2207],[1.733,41.223]]

	elif(i==6):
		boundingBox=[[1.7037,41.2202],[1.7096,41.224],[1.7076,41.2259],[1.7025,41.2254],[1.6973,41.2284],[1.6913,41.2302],[1.6916,41.2259],[1.6934,41.2233],[1.6963,41.2206],[1.7005,41.2228]]

	elif(i==7):
		boundingBox=[[1.6961,41.222],[1.6933,41.2239],[1.6854,41.2207],[1.6916,41.2152],[1.6956,41.2169]]

	elif(i==8):
		boundingBox=[[1.7238,41.2213],[1.7337,41.2364],[1.7461,41.2222],[1.7242,41.2203]]

	elif(i==9):
		boundingBox=[[1.74,41.23077],[1.74045,41.22994],[1.74279,41.23094],[1.74235,41.23181]]

	elif(i==10):
		boundingBox=[[1.7034,41.2206],[1.7106,41.2247],[1.7165,41.2185],[1.7079,41.215]]

	elif(i==11):
		boundingBox=[[1.7167,41.2278],[1.7198,41.2246],[1.72803,41.22741],[1.72203,41.22998]]

	elif(i==12):
		boundingBox=[[1.7238,41.2212],[1.7255,41.2185],[1.7227,41.2174],[1.7163,41.219],[1.7252,41.2216]]

	elif(i==13):
		boundingBox=[[1.6818,41.2052],[1.6872,41.2064],[1.6876,41.2048],[1.6829,41.2028]]

	elif(i==14):
		boundingBox=[[1.7228,41.2174],[1.7146,41.2119],[1.7261,41.2134],[1.7231,41.217]]

	elif(i==15):
		boundingBox=[[1.7106,41.2245],[1.7163,41.2189],[1.7238,41.2213],[1.7149,41.2272]]

	elif(i==16):
		boundingBox=[[1.6758,41.2178],[1.6825,41.2212],[1.6849,41.2185],[1.6847,41.2163],[1.6797,41.2219]]

	elif(i==17):
		boundingBox=[[1.7252,41.2363],[1.7285,41.2366],[1.7297,41.2339],[1.7258,41.2333]]

	return boundingBox

def is_inside_polygon(x,y,poly):
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


def get_the_neighborhood_is_at(citizenStep, neighborhoodBoundingBoxes):

	found = False
	i = 0
	while(i<18 and not found):
		found = is_inside_polygon(float(citizenStep[0]),float(citizenStep[1]),neighborhoodBoundingBoxes[i])
		if(not found):
			i = i + 1
	if(not found):
		i = i - 1
	return i

def init_neighborhood_array():

	neighborhood_array = []
	for i in range(18):
		neighborhood_array.append(get_neighborhood_boundingBox(i))
	return neighborhood_array

def main(gpstrace):
	
	neighborhoodBoundingBoxes = init_neighborhood_array()
	neighborhoodScores = ([0] * 18)
	with open(gpstrace,'r') as gpsfile:
		for citizensRawStep in gpsfile:
			citizensStep = citizensRawStep.split(' ')
			citizensStep = citizensStep[:-2] #we delete the \n 
			n = 2
			citizensStep = [ citizensStep[i:i+n] for i in range(0, len(citizensStep), n) ]
			for citizenStep in citizensStep:
				neighborhoodIndex = get_the_neighborhood_is_at(citizenStep, neighborhoodBoundingBoxes)
				if(neighborhoodIndex != -1):
					neighborhoodScores[neighborhoodIndex] += 1
			
			print(neighborhoodScores)
			break

if __name__ == "__main__":
	main(sys.argv[1])
