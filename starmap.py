import csv
import time
import json
import random
import numpy as np
import pyplanets
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def create_coords(amount):
    xyz=np.array(np.random.random((amount,3)))

    with open('sector_1.csv', mode='w', newline='') as file:
        planet_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        planet_writer.writerow(['x', 'y', 'z'])
        for item in xyz:
            planet_writer.writerow(item)

    return xyz


def generate_planets(planets=[]):
    galaxy = pyplanets.Galaxy()
    planets = planets + galaxy.planets

    while len(planets) <= 20000:
        galaxy.nextgalaxy()
        galaxy.makeSystems()
        planets = planets + galaxy.planets

    return planets


def remove_dup(a):
   i = 0
   while i < len(a):
      j = i + 1
      while j < len(a):
         if a[i] == a[j]:
            del a[j]
         else:
            j += 1
      i += 1


planets = generate_planets()
xyz = create_coords(len(planets))

remove_dup(planets)

weighted_types = ['rocky'] * 30 + ['desert'] * 20 + ['volcanic'] * 20 + ['gaseous'] * 15 + ['terra'] * 10 + ['metal'] * 5

for i, item in enumerate(xyz):
    type = random.choice(weighted_types)
    data = {
        "name": planets[i],
        "description": "A planet in The Dissent Atlas",
        "image": "https://dissent.world/planet_images/{}.png".format(i),
        "attributes": [
            {
                "trait_type": "planet",
                "value": type
            },
            {
                "trait_type": "location",
                "value": "{}, {}, {}".format(item[0], item[1], item[2])
            },
            {
                "trait_type": "galactic serial number",
                "value": 8423 + i
            }

        ]
    }

    with open('planet_metadata/planet_{}.json'.format(i + 1), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
