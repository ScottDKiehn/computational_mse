from bs4 import BeautifulSoup
import sys

def parse(filename):
    with open(filename, 'r') as f:
        data = f.read()
        xml_tags = BeautifulSoup(data, "xml")
        calculation_tags = xml_tags.find_all("calculation")
        array_tags = xml_tags.find_all("array")

        for calculation in calculation_tags:
          varray_tags = calculation.find_all("varray")
          for varray in varray_tags:
            if varray.get("name") == "positions":
              for v in varray.find_all("v"):
                position_data = " ".join(v.get_text().split())
                #print(position_data)

          for array in array_tags:
            if array.get("name") == "atoms":
                odd_count = 0
                count = 1
                for c in array.find_all("c"):
                  odd_count += 1
                  count += 1
                  if odd_count % 2 == 1: 
                    atom = (f"{c.get_text(strip=True)}{int(count/2)}")
          print(atom, position_data)



parse("vasprun_nblock_1.xml")
