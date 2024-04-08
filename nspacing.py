from bs4 import BeautifulSoup
import numpy as np
import math
import matplotlib.pyplot as plt
import sys
from sys import argv
import os

def spacing(filename, output, lx, ly, lz):
  with open(output, "w") as l:
    sys.stdout = l
    with open(filename, "r") as f:
      data = f.read()
      xml_data = BeautifulSoup(data, "xml")
      iteration_tags = xml_data.find_all("iteration")

      iteration_count = 0
      n_distances = []
      n9_position, n10_position = None, None

      for iteration in iteration_tags:
        iteration_count += 1
        atom_tags = iteration.find_all("atom")

        for atom in atom_tags:
          name = atom.get("name")
          position_data = [float(val)/1.89 for val in list(atom.children)[1].text.split()]

          if name.startswith("N9"):
            n9_position = position_data
          elif name.startswith("N10"):
            n10_position = position_data

          if n9_position and n10_position is not None:
            n9_array, n10_array = np.array(n9_position), np.array(n10_position)

        #lx, ly, lz = 5.54, 4.72, 12.14 <-- used for testing
        #n_distance = math.sqrt(((n9_array - n10_array)[0] % lx)**2 + ((n9_array - n10_array)[1] % ly)**2 + ((n9_array - n10_array)[2] % lz)**2)
    
        dx,dy,dz = n9_array[0] - n10_array[0],n9_array[1] - n10_array[1],n9_array[2] - n10_array[2]
        n_distance = math.sqrt((dx - (lx * round(dx/lx)))**2 + (dy - (ly * round(dy/ly)))**2 + (dz - (lx * round(dz/lz)))**2)
        n_distances.append(n_distance)

    x_axis = np.linspace(0, float(iteration_count*.483), len(n_distances))
    plt.plot(x_axis, n_distances)
    plt.xlabel("Time (fs)")
    plt.ylabel("N-N Distance (ang)")
    plt.title("N-N Distance vs Time (WITH PBC)")
    plt.savefig(output, format="png", dpi=300)

filename, output, lx, ly, lz = argv[1], argv[2], argv[3], argv[4], argv[5]

if len(argv) != 6:
  os.system("echo " + "usage: python nspacing.py <xyz file> <output name> <lx> <ly> <lz>")
else:
  spacing(filename, output, lx, ly, lz)
