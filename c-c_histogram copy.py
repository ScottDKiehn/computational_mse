import matplotlib.pyplot as plt

def parser(input, atom):
  with open(input, "r") as r:
    lines = r.readlines()

    diff_list, euclidean_dist_list = [],[]

    config_count = 0

    for i, line in enumerate(lines):
      if "Direct configuration=     1" in line:
        config_count += 1
        atom_symbols = lines[i-2].split()
        atom_counts = list(map(int, lines[i-1].split()))
        specific_count = atom_counts[atom_symbols.index(atom)]
        upper_bound = sum(atom_counts[:(atom_counts.index(specific_count)+1)])
        lower_bound = upper_bound - specific_count + 1
        atom_total = sum(atom_counts)
      
        positions = [list(map(float, lines[j].split())) for j in range(i + 1, i + 1 + atom_total)]
        specific_positions = positions[lower_bound-1:upper_bound]

    for i in range(len(specific_positions)):
      for j in range(i+1, len(specific_positions)):
        diff = [specific_positions[j][k]-specific_positions[i][k] for k in range(3)]
        diff_list.append(diff)
    for diff in diff_list:
      euclidean_dist = sum(d**2 for d in diff) **.5
      euclidean_dist_list.append(euclidean_dist)

    plt.hist(euclidean_dist_list, bins=50, edgecolor= "black")
    plt.title('Difference Histogram')
    plt.xlabel('Distances')
    plt.ylabel('Frequency')
    plt.show()




  

parser("./150fs/XDATCAR_first2", "C")