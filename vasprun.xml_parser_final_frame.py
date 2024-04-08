from bs4 import BeautifulSoup
import sys
import os
from sys import argv

def parser(filename, output):
    with open(output, "w") as l:
        sys.stdout = l
        with open(filename, "r") as f:
            data = f.read()
            xml_tags = BeautifulSoup(data, "xml")

            atom_count = None
            positions = []

            for array in xml_tags.find_all("array"):
                if array.get("name") == "atoms":
                    atom_data = [c.find("c").get_text(strip=True) for c in array.find_all("rc")]

            structure_tags = xml_tags.find_all("structure")
            finalpos_tag = None  # Initialize to None
            for structure in structure_tags:
                if structure.get("name") == "finalpos":
                    finalpos_tag = structure
            if finalpos_tag:
                varray = finalpos_tag.find("varray", {"name": "positions"})
                if varray:
                    for v in varray.find_all("v"):
                        position_data = v.get_text().split()
                        positions.append(position_data)

            if atom_data:
                atom_count = len(atom_data)

            if atom_count and positions:
                print(f"{atom_count}\n")
                for i in range(atom_count):
                    x, y, z = map(float, positions[i])
                    print(f"{atom_data[i]} {10*x} {10*y} {10*z}")

#if len(argv) != 3:
  ##os.system("echo " + "usage: blah blah")
#else:
    #filename, output = argv[1], argv[2]
parser("vasprun_nblock_1.xml", "nblock1_finalframe.xyz")
