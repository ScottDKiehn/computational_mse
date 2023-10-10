from bs4 import BeautifulSoup
import numpy as np
from sys import argv
import matplotlib.pyplot as plt
import sys
import math

def spacing(filename):
  with open("output.txt", 'w') as l:
    sys.stdout = l

    
    with open(filename, "r") as f:
      data = f.read()
      xml_data = BeautifulSoup(data, "xml")
      iteration_tags = xml_data.find_all("iteration") #searches for "iteration" in xml file

      #itialization
      iteration_count = 1
      n9_positions = []
      n10_positions = []
      n_differences = []
      n_differences_modified = []
      n_distances_true = []

      for iteration in iteration_tags:
        iteration_count += 1

        
        atom_tags = iteration.find_all("atom") #searches for "atom" in each iteration
        for atom in atom_tags: #each atom has its respective data, gathers name and position data in the following lines:
          name = atom.get("name")
          atom_children = list(atom.children)
          position_data = atom_children[1].text
          position_data_list_ang = [(float(val))/1.89 for val in position_data.split()] #converts position to unit angrstoms


          if name.startswith("N9"): #conditional to get postiions of nitrogen atom 9 and nitrogen atom 10
            n9_positions.append(position_data_list_ang)
          if name.startswith("N10"):
            n10_positions.append(position_data_list_ang)

        #tried converting things to numpy arrays to make things easier
        n9_array, n10_array = np.array(n9_positions), np.array(n10_positions)
        n_difference = n9_array-n10_array
        n_differences.append(n_difference)


        #lattice parameters (constant)
        lx = 5.45
        ly = 4.72
        lz = 12.14

        n_difference_modified = [(n_difference[0] % lx), (n_difference[1] % ly), (n_difference[2] % lz)] #MODIFED: INCLUDES PERIODIC BOUNDARY CONDITIONS
        n_distance_true = [math.sqrt(sum(val**2 for val in n_difference_modified))] #finds euclidean distance using pythagorean method
        n_differences_modified.append(n_difference_modified)
        n_distances_true.append(n_distance_true)

        print(f"Frame: {iteration_count}")
        print(f"N9 Positions: {n9_positions}")
        print(f"N10 Positions: {n10_positions}")
        print(f"N-N Distance: {n_difference}")
        print(f"True Euclidean Distance: {n_distance_true}")

      x_axis = np.linspace(0, iteration_count, len(n9_positions))
      y_axis = n_distances_true

      plt.plot(x_axis, y_axis)
      plt.xlabel("Frame Count (fs)")
      plt.ylabel("N-N Distance")
      plt.show()
      plt.savefig('output.png', format='png', dpi=300, bbox_inches='tight', facecolor='white', edgecolor='black')

spacing("ssages_out_0_run_0_cleaned_frame1.xml") #note this is only frame 1, normally there's many thousands

