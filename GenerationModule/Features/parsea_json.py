import json
from pprint import pprint
import sys

with open(sys.argv[1]) as f:
    data = json.load(f)


rutas = data['routes'][0]['geometry']['coordinates']

dirname = os.path.dirname(sys.argv[2])
if not os.path.exists(dirname):
    os.makedirs(dirname)

with open(sys.argv[2], 'a') as traza:
    traza.write(rutas)

