import matplotlib.pyplot as plt

def parser(input_file, target_atom):
    with open(input_file, "r") as f:
        lines = f.readlines()

    diff_list, euclidean_dist_list = [], []

    config_count = 0
    i = 0  # Initialize i outside the loop

    while i < len(lines):
        line = lines[i]
        if "Direct configuration=" in line:
            config_count += 1
            if config_count > 1:
                atom_symbols = lines[i - 2].split()
                atom_counts = list(map(int, lines[i].split()))
                specific_count = atom_counts[atom_symbols.index(target_atom)]
                upper_bound = sum(atom_counts[:(atom_symbols.index(target_atom) + 1)])
                lower_bound = upper_bound - specific_count + 1
                atom_total = sum(atom_counts)

                positions = [list(map(float, lines[j].split())) for j in range(i + 1, i + 1 + atom_total)]
                specific_positions = positions[lower_bound - 1:upper_bound]
                for i in range(len(specific_positions)):
                    for j in range(i + 1, len(specific_positions)):
                        diff = [specific_positions[j][k] - specific_positions[i][k] for k in range(3)]
                        diff_list.append(diff)

        i += 1  # Increment i

    euclidean_dist_list = [sum(d**2 for d in diff)**0.5 for diff in diff_list]

    plt.hist(euclidean_dist_list, bins=50, edgecolor="black")
    plt.title('Difference Histogram')
    plt.xlabel('Differences')
    plt.ylabel('Frequency')
    plt.show()

parser("./150fs/XDATCAR_first2", "C")
