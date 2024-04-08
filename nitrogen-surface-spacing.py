from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math

def z_space(filename):

  with open(filename, "r") as f:
    data = f.read()
    xml_tags = BeautifulSoup(data, "xml")
    iteration_tags = xml_tags.find_all("iteration")

    iteration_count = 0
    nitrogen9_positions = []
    nitrogen10_positions = []
    surface_positions = []

    for iteration in iteration_tags:
      iteratation_count += 1


      atom_tags = iteration.find_all("atom")

      for atom in atom_tags:
        name = atom.get("name")
        atom_children = list(atom.children)
        position_data = atom_children[1].text
        position_data_list_bohr = position_data.split()
        position_data_list_ang = [(float(val)/1.89 for val in position_data_list_bohr)]

        if name.startswith("N9"):
          nitrogen9_positions.append(position_data_list_ang)
        elif name.startswith("N10"):
          nitrogen10_positions.append(position_data_list_ang)
        elif name.startswith("Ru") and (name.endswith("5") or name.endswith("6") or name.endswith("7") or name.endswith("8")):
          surface_positions.append(position_data_list_ang)


        avg_surface_pos = [(sum(a[i]) for a in surface_positions)/i for i in range(position_data_list_ang)]
        n9_distance = [n9 - avg for n9, avg in zip(nitrogen9_positions, avg_surface_pos)]
        n10_distance = [n10 - avg for n10, avg in zip(nitrogen10_positions, avg_surface_pos)]
  


  x_axis = np.linsapce(0, iteration_count, len(nitrogen10_positions))
  y1 = n9_distance
  y2 = n10_distance
  plt.plot(x_axis, y1, label = "N9 distance")
  plt.plot(x_axis, y2, label = "N10 distance")
  plt.legend()
  plt.show()



  


      

