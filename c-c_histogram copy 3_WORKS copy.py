import matplotlib.pyplot as plt
import numpy as np

def parser(input, atom1, atom2):
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

        if atom1 == atom2:
            specific_count = atom_counts[atom_symbols.index(atom1)]
            upper_bound = sum(atom_counts[:(atom_counts.index(specific_count)+1)])
            lower_bound = upper_bound - specific_count + 1
            atom_total = sum(atom_counts)

            x_scale = 7.994037
            y_scale = 9.271353
            z_scale = 27.081524

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


        else:
            specific_count1 = atom_counts[atom_symbols.index(atom1)]
            specific_count2 = atom_counts[atom_symbols.index(atom2)]
            upper_bound1 = sum(atom_counts[:(atom_counts.index(specific_count1)+1)])
            upper_bound2 = sum(atom_counts[:(atom_counts.index(specific_count2)+1)])
            lower_bound1 = upper_bound1 - specific_count1 + 1
            lower_bound2 = upper_bound2 - specific_count2 + 1
            atom_total = sum(atom_counts)

            print(f"{specific_count1} atoms of {atom1} found")
            print(f"{specific_count2} atoms of {atom2} found")

            x_scale = 7.994037
            y_scale = 9.271353
            z_scale = 27.081524
 

            for i, line in enumerate(lines):
                if "Direct configuration" in line:
                    positions = [list(map(float, lines[j].split())) for j in range(i + 1, i + 1 + atom_total)]

                    scaled_positions = [[x * x_scale, y * y_scale, z * z_scale] for x, y, z in positions]
                    specific_positions1 = scaled_positions[lower_bound1-1:upper_bound1]
                    specific_positions2 = scaled_positions[lower_bound2-1:upper_bound2]

                    for j in range(min(len(specific_positions1), len(specific_positions2))):
                        for k in range(j, min(len(specific_positions1), len(specific_positions2))):
                            diff = [specific_positions2[k][l] - specific_positions1[j][l] for l in range(3)]
                            euclidean_dist = sum(d**2 for d in diff) ** 0.5
                            euclidean_dist_list.append(euclidean_dist)

        
        plt.hist(euclidean_dist_list, bins=100, edgecolor="black")
        plt.xticks(np.arange(0, int(max(euclidean_dist_list)+3), step=1))
        plt.title('Difference Histogram')
        plt.xlabel('Distances')
        plt.ylabel('Frequency')
        plt.show()

        #sij = (1-((rij-d0)/r0))**n/(1-((rij-d0)/r0))**m


parser("./150fs/XDATCAR", "C", "H")