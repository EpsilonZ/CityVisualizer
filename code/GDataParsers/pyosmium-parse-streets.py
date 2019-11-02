"""
Compute the total length of highways in an osm file.
Shows how to extract the geometry of a way.
"""
import osmium as o
import sys
import urllib.request
import json

f = open("filtered_traces/limitesCarreterasVilanovaILaGeltru.txt","a")
array_carreteras = []

class LimitesCarreteras(o.SimpleHandler):
    def __init__(self):
        super(LimitesCarreteras, self).__init__()
        self.length = 0.0

    def way(self, w):
        if 'highway' in w.tags:
            try:
                nombre = w.tags.get('name', '') 
                #print(nombre)
                if(len(nombre)>0):
                    indice,existe = comprueba_si_existe(nombre)
                    nuevas_coordenadas = []
                    if(not existe):
                        nuevas_coordenadas.append(nombre)
                        nuevas_coordenadas.append("@@@") #separador entre nombre y coordenadas
                    for i in w.nodes:
                        if(existe):
                                array_carreteras[indice].append([i.location.lon,i.location.lat])
                        else:
                                nuevas_coordenadas.append([i.location.lon,i.location.lat])
                    if(not existe):
                        array_carreteras.append(nuevas_coordenadas)

                else:

                    url = 'http://open.mapquestapi.com/geocoding/v1/reverse?key=MXSRhLoc6m39HTn8NWdwU7D8R0MoeN53&location=' + str(w.nodes[0].location.lat) + ',' + \
                    str (w.nodes[0].location.lon) + '&includeRoadMetadata=true&includeNearestIntersection=true'
                    print(url)
                    response = urllib.request.urlopen(url)
                    data = response.read()      # a `bytes` object
                    encoding = response.info().get_content_charset('utf-8')
                    JSON_object = json.loads(data.decode(encoding))
                    nombre = JSON_object["results"][0]["locations"][0]["street"]
                    indice, existe = comprueba_si_existe(nombre)
                    #print(existe)
                    print(nombre)
                    nuevas_coordenadas = []
                    if(len(nombre)>0):
                        if(not existe):
                            nuevas_coordenadas.append(nombre)
                            nuevas_coordenadas.append("@@@")
                        for i in w.nodes:
                            if(existe):
                                array_carreteras[indice].append([i.location.lon,i.location.lat])
                            else:
                                nuevas_coordenadas.append([i.location.lon,i.location.lat])
                        if(not existe):
                            array_carreteras.append(nuevas_coordenadas)
                    else:
                        print('Este lugar no ha podido ser encontrado:', w.id)
                    #else:
                        #print('Nuevas coords added',array_carreteras[indice])
                #f.write(listaNodos)
                #print(listaNodos)
                self.length += o.geom.haversine_distance(w.nodes)
            except o.InvalidLocationError:
                # A location error might occur if the osm file is an extract
                # where nodes of ways near the boundary are missing.
                pass


def comprueba_si_existe(nombre):
	i = 0
	encontrado = False
	while i < len(array_carreteras) and not encontrado:
		if(array_carreteras[i][0]==nombre):
			encontrado = True
		else:
			i = i + 1

	return i,encontrado
			 

def main(osmfile):
    h = LimitesCarreteras()
    # As we need the geometry, the node locations need to be cached. Therefore
    # set 'locations' to true.
    h.apply_file(osmfile, locations=True)

    #print('Total way length: %.2f km' % (h.length/1000))

    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python %s <osmfile>" % sys.argv[0])
        sys.exit(-1)

    main(sys.argv[1])
    lineaFichero = ""
    for i in range(len(array_carreteras)):
        lineaFichero += str(array_carreteras[i][0]) + " " + str(array_carreteras[i][1]) + " "
        elemIndice = 2
        while (elemIndice < len(array_carreteras[i])):
            lineaFichero += str(array_carreteras[i][elemIndice][0]) + " " + str(array_carreteras[i][elemIndice][1]) + " "
            elemIndice = elemIndice + 1
        lineaFichero = lineaFichero[:-1]
        lineaFichero += "\n"
    lineaFichero = lineaFichero [:-1]
    print(lineaFichero)
    f.write(lineaFichero)
    f.close()
    exit()
