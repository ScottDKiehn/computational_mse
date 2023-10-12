from bs4 import BeautifulSoup
import numpy as np
import math
import matplotlib.pyplot as plt

def spacing(filename):
  with open(filename, "r") as f:
    data = f.read()
    xml_data = BeautifulSoup(data, "xml")
    iteration_tags = xml_data.find_all("iteration")

    iteration_count = 0
    n_differences, n_distances = [], []
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
          n_differences.append(n9_array-n10_array)

      lx, ly, lz = 5.54, 4.72, 12.14

      n_distance = math.sqrt(((n9_array - n10_array)[0] % lx)**2 + ((n9_array - n10_array)[1] % ly)**2 + ((n9_array - n10_array)[2] % lz)**2)
      n_distances.append(n_distance)

  x_axis = np.linspace(0, iteration_count, len(n_distances))
  plt.plot(x_axis, n_distances)
  plt.xlabel("Iteration (fs)")
  plt.ylabel("N-N Distance (ang)")
  plt.title("N-N Distance vs Time (WITH PCB)")
  plt.show()

spacing("ssages_out_0_run_0_cleaned_frame1and2.xml")
