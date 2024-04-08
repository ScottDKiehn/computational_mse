#!/usr/bin/python
from bs4 import BeautifulSoup
from sys import argv
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

def n_spacing(filename):
  with open("output.txt", "w") as l:
    sys.stdout = l

    with open (filename, "r") as f:
      xml_data = f.read()
      xml_tags = BeautifulSoup(xml_data, "xml")
      iteration_tags = xml_tags.find_all("iteration")

      iteration_count = 0
      n_differences = []
      n_distances_unmodified = []
      n_distances_true = []

      for iteration in iteration_tags:
        atom_tags = iteration.find_all("atom")

        iteration_count += 1
        n9_positions = []
        n10_positions = []

        for atom in atom_tags:
          name = atom.get("name")
          atom_children = list(atom.children)
          position_data = atom_children[1].text
          position_data_list_bohr = position_data.split()
          position_data_list_ang = [(float(val))/1.89 for val in position_data_list_bohr]

          if name.startswith("N9"):
            n9_positions.append(position_data_list_ang)
          elif name.startswith("N10"):
            n10_positions.append(position_data_list_ang)

        #use numpy array. var = np.array(orignal list)
        n_difference = [[n9 - n10 for n9, n10 in tuple(zip(n9_pos, n10_pos))] for n9_pos, n10_pos in zip(n9_positions, n10_positions)]
        #n_difference = [n9 - n10 for n9,n10 in zip(n9_positions, n10_positions)]
        n_differences.append(n_difference)
        print(n_difference)
        dx = n_difference[0]
        dy = n_difference[1]
        dz = n_difference[2]
        lx = 5.45
        ly = 4.72
        lz = 12.14
        n_distances_unmodified = math.sqrt(dx**2 + dy**2 +dz**2)
        n_distances_unmodified.append(n_distances_unmodified)
        n_distance_true = math.sqrt((dx % lx)**2 + (dy % ly)**2 + (dz % lz)**2)
        n_distances_true.append(n_distance_true)

        print(f"Iteration count: {iteration_count}")
        print(f"N-N distance WITHOUT PCB {n_distances_unmodified}")
        print(f"N-N distance WITH PCB: {n_distance_true}")

      x_axis = np.linspace(0, iteration_count, len(n_distances_true))
      y_axis1 = n_distances_true
      y_axis2 = n_distances_unmodified
      plt.plot(x_axis,y_axis1, label = "WITH PBC")
      plt.plot(x_axis,y_axis2, label = "WITHOUT PBC")
      plt.xlabel("Iteration count (fs)")
      plt.ylabel("N-N distance")
      plt.legend()
      plt.show()




#main function

n_spacing("ssages_out_0_run_0_cleaned_frame1.xml")