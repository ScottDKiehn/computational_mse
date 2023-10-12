from bs4 import BeautifulSoup
import sys
from sys import argv
import os

def xyz(filename, output, lx, ly, lz):
  with open(output,'w') as l:
    sys.stdout = l

    with open(filename, 'r') as f:
      data = f.read()
      xml_data = BeautifulSoup(data, "xml")
      iteration_tags = xml_data.find_all("iteration")
      iteration_count = 0

      for iteration in iteration_tags:
        iteration_count += 1
        
        atom_tags = iteration.find_all("atom")
        print(len(atom_tags))
        print("")

        for atom in atom_tags:
          name = atom.get("name")
          position_data = [float(val)/1.89 for val in list(atom.children)[1].text.split()]
          position_data_updated = [position_data[0] % float(lx), position_data[1] % float(ly), position_data[2] % float(lz)]
          print(name, ' '.join(map(str, position_data_updated)))


if len(argv) != 6:
  os.system("echo " + "Usage: to_xml.py <input.xml> <output.xyz> <lx> <ly> <lz>")
else:
  os.system("echo " + "Converting to XYZ")
  filename, output, lx, ly, lz = argv[1],argv[2],argv[3],argv[4],argv[5]
  xyz(filename, output, lx, ly, lz)
