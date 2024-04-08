from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import math
import re


# 1. find direct config line, 2. find the previous two lines and convert them to lists (they're already whitespace separated). 
# the line two lines before the direct configuration line is the atomlist: [C,H,Ru], and the one one line before is the atomcount: [6,26,48], 
# 2.find the index that corresponds to the function input, this index will be called atom_index. 
#ex: C -> 1, H -> 2, Ru -> 3. so if C is called from the atom argument via parser(input_file, "C"), then the atom_index would be 1.
# 3. match atom_index's value with the index of atomcount list. so if atom_index is 1, it would return the value of equivalent index in 
# atomcount list -> 6. this value would be stored in variable called up_index. so up_index = 6 in this case. 
# 4. define variable upper_bound that adds up_index to all the previous values in the atomcount list. if up_index corresponds to the first 
# index in atomcount, then it adds zero.  for example, if H were called, the would correspond to the up_index value 26 in atomcount, therefore
# upper_bound would be 26+6=32. the 6 comes from the previous value in atomcount.
# 5. define variable lower_bound that's the value of the previous value in atomcount + 1. so if H were called, upper_bound would be 32,
# therefore, lower_bound would be 7, as this is the 6 from the pervious element in the list plus 1.
# 6. sample the number of lines after the direct config line corresponding to the sum of atomcount, and store in atom_total: so in this case, store the next 80 lines
# (from 6+26+48 from atomcount), and store in a list called positions
# 7. fetch from the positions list, the position values that correspond with the upper_bound and lower_bound variables and add to a new list 
# called specific_positions. so if H were called, lines 7-32 out of 80 total lines would be added to specific positions.


def parser(input, atom):
  #with open(output, "w") as l:
    #sys.stdout = l
    with open(input, "r") as f:
      lines = f.readlines()

    config_count = 0

    for i, line in enumerate(lines):
      if "Direct configuration" in line:
          config_count += 1
          atom_symbols_line = lines[i - 2].split()
          atom_counts_line = list(map(int, lines[i - 1].split()))
          atom_index = atom_symbols_line.index(atom) + 1
          up_index = atom_counts_line[atom_index - 1]
          upper_bound = sum(atom_counts_line[:atom_index])
          lower_bound = upper_bound - up_index + 1
          atom_total = sum(atom_counts_line)
          positions = [list(map(float, lines[i + j + 1].split())) for j in range(min(atom_total - 1, len(lines) - i - 1))]
          specific_positions = positions[lower_bound - 1:upper_bound]
          
    euclidean_distance_list = []
    difference_list = []

    #3D CASE:
    for i in range(len(specific_positions)):
        for j in range(i+1, len(specific_positions)):
            diff = [specific_positions[j][k] - specific_positions[i][k] for k in range(3)]
            difference_list.append(diff)
    for diff in difference_list:
        euclidean_distance = sum(d ** 2 for d in diff) ** 0.5
        euclidean_distance_list.append(euclidean_distance)


    plt.hist(euclidean_distance_list, bins=50, edgecolor= "black")
    plt.title('Difference Histogram')
    plt.xlabel('Differences')
    plt.ylabel('Frequency')
    plt.show()


parser("./150fs/XDATCAR_firstline", "H")

      
    #1D CASE:
    #for i in range(len(array)):
      #for j in range(i+1, len(array)):
        #new_array.append(array[j]-array[i])

        #np.array(new_array) 

    #plt.hist(new_array, bins=num_bins, edgecolor= "black")
    #plt.title('Difference Histogram')
    #plt.xlabel('Differences')
    #plt.ylabel('Frequency')
    #plt.show()


#convert fractional coordinates to absolute
#encompass all 500 frames in histogram
#convert XDATCAR to Lammpsdump to use in MDanalysis to plot radial dis. and coordination number