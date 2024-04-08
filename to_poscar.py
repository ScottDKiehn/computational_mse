from bs4 import BeautifulSoup
import sys
from sys import argv 
import os

def parser(filename, output, lx,ly,lz, description):
  with open(output, "w") as l:
    sys.stdout = l
    with open(filename, "r") as f:
      data = f.read()
      xml_tags = BeautifulSoup(data, "xml")
      iteration_tags = xml_tags.find_all("iteration")

      if iteration_tags:
        iteration = iteration_tags[0]
        atom_tags = iteration.find_all("atom")
        print(description)
        print("        1")
        print(f"    {lx}  0.000000  0.000000")
        print(f"    0.000000  {ly}  0.000000")
        print(f"    0.000000  0.000000  {lz}")
        

        atom_list = [atom.get("name").rstrip('0123456789') for atom in atom_tags]

        atom_count = {}
        for atom in atom_list:
          if atom in atom_count:
            atom_count[atom] += 1
          else:
            atom_count[atom] = 1

        unique_atoms = [f"{atom}" for atom in list(dict.fromkeys(atom_list))]
        print("   "+"    ".join(unique_atoms))

        total_counts = [str(atom_count[atom]) for atom in unique_atoms]
        print("   "+"    ".join(total_counts))
        print("Direct configuration=   408")

        for atom in atom_tags:
          position_data = [float(val)/1.89 for val in list(atom.children)[1].text.split()]
          #fractional = [position_data[0]/lx, position_data[1]/ly, position_data[2]/lz]
          #print(" ".join(map(str, fractional)))
          #WITH PBC
          position_data_updated = ([(position_data[0] % float(lx))/lx, (position_data[1] % float(ly))/ly, (position_data[2] % float(lz))/lz])
          print(' '.join(map(str, position_data_updated)))

filename, output, lx,ly,lz, description = argv[1], argv[2], argv[3], argv[4], argv[5], argv[6]
if len(argv) != 7:
  os.system("echo " + "usage: python to_poscar.py <xyz file> <output name> <lx> <ly> <lz> <description> WILL ONLY DO FIRST FRAME")
else:
  os.system("echo " + "converting to POSCAR...")   
  parser(filename, output, lx,ly,lz, description)
