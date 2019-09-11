import json
from pprint import pprint
import sys
import os

#print sys.argv

with open(sys.argv[2]) as f:
    data = json.load(f)


rutas = data['routes'][0]['geometry']['coordinates']


dirname = os.path.dirname("./"+sys.argv[1])
if not os.path.exists(dirname):
    os.makedirs(dirname)

with open(sys.argv[1], 'a') as traza:
    stringRutas = str(rutas)
    traza.write(stringRutas.replace(" ","")+"\n")

