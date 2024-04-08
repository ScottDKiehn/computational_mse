import matplotlib.pyplot as plt
import numpy as np

def parser(input, atom):
    with open(input, "r") as r:
        lines = r.readlines()
        euclidean_dist_list = []

        atom_symbols = []
        atom_counts = []
        specific_positions = []

        for i, line in enumerate(lines):
            if i == 5:
                atom_symbols = line.split()
            elif i == 6:
                atom_counts = list(map(int, line.split()))

        specific_count = atom_counts[atom_symbols.index(atom)]
        upper_bound = sum(atom_counts[:(atom_counts.index(specific_count)+1)])
        lower_bound = upper_bound - specific_count + 1
        atom_total = sum(atom_counts)

        x_scale = 7.994037
        y_scale = 9.271353
        z_scale = 27.081524
        #x_scale = 1
        #y_scale = 1
        #z_scale = 1

        for i, line in enumerate(lines):
            if "Direct configuration" in line:
                positions = [list(map(float, lines[j].split())) for j in range(i + 1, i + 1 + atom_total)]

                scaled_positions = [[x * x_scale, y * y_scale, z * z_scale] for x, y, z in positions]
                specific_positions = scaled_positions[lower_bound-1:upper_bound]

                for i in range(len(specific_positions)):
                    for j in range(i+1, len(specific_positions)):
                        diff = [specific_positions[j][k] - specific_positions[i][k] for k in range(3)]
                        euclidean_dist = sum(d**2 for d in diff) ** 0.5
                        euclidean_dist_list.append(euclidean_dist)

    plt.hist(euclidean_dist_list, bins=200, edgecolor="black")
    plt.xticks(np.arange(0, int(max(euclidean_dist_list)+3), step=1))
    plt.title('Distance Histogram')
    plt.xlabel('Distances (Ang)')
    plt.ylabel('Frequency')
    plt.show()

parser("./150fs/XDATCAR", "C")


#use cutoff as d_0: around 2 from visual inspection, and use plumed with the vairbales that professor lee gave you