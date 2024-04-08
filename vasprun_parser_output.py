from bs4 import BeautifulSoup
import sys
from sys import argv


def parse(filename, output):
  with open(output, "w") as l:
    sys.stdout = l
    with open(filename, 'r') as f:
      data = f.read()
      xml_tags = BeautifulSoup(data , "xml")
      structure_tags = xml_tags.find_all("structure")

    for structure in structure_tags:
      varray_tags = structure.find_all("varray")
      for v in varray_tags:
       if v.get("name") == "positions":
          print(v)

parse("vasprun_nblock_1.xml", output='x')