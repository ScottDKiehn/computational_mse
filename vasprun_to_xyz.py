from bs4 import BeautifulSoup
import sys
from sys import argv
import os

def parser(filename, output):
  with open(output, "w") as l:
    sys.stdout = l
    with open(filename, "r") as f:
      data = f.read()
      xml_tags = BeautifulSoup(data, "xml")
      structure_tags = xml_tags.find_all("structure")

      for array in xml_tags.find_all("array"):
        if array.get("name") == "atoms":
          atom_data = [c.find("c").get_text(strip=True) for c in array.find_all("rc")]

      for structure in structure_tags:
        position_data_list = []
        for varray in structure.find_all("varray"):
          if varray.get("name") == "positions":
            for v in varray.find_all("v"):
              position_data = v.get_text().split()
              position_data_list.append(position_data)

        print(f"{len(atom_data)}\n")
        for i in range(len(atom_data)):
          x,y,z = map(float, position_data_list[i])
          print(f"{atom_data[i]} {10*x} {10*y} {10*z}")

if len(argv) != 3:
  os.system("echo " + "usage: python vasprun_to_xyz.py <filename.xml> <outputfilename.xyz>")   
else:
  os.system("echo " + "converting to xyz...")   
  filename, output = argv[1], argv[2]
  parser(filename, output)
