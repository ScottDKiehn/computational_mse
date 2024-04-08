import matplotlib.pyplot as plt
import numpy as np

def switching(rij, d0, r0, n, m):
    top = (1 - (rij - d0) / r0) ** n
    bottom = (1 - (rij - d0) / r0) ** m
    return top / bottom

def dist(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def parser(input, atom):
    with open(input, "r") as f:
        lines = f.readlines()

        #CHANGE THESE PARAMETERS BASED ON SCALING LINES 3,4,5 IN XDATCAR. ONLY SUPPORTS CUBIC SYSTEMS
        x_scale, y_scale, z_scale = 7.994037, 9.271353, 27.081524
        
        iteration_counter = 0
        radial_distances_iteration, z_distances_iteration = {}, {}

        ethane_positions = {}
        ethane_radial_distances = {}
        ethane_z_distances = {}

        for i, line in enumerate(lines):
            if i == 5:
                atom_symbols = line.split()
            elif i == 6:
                atom_counts = list(map(int, line.split()))
                specific_count = atom_counts[atom_symbols.index(atom)]
                upper_bound = sum(atom_counts[:(atom_counts.index(specific_count) + 1)])
                lower_bound = upper_bound - specific_count + 1
            elif line.startswith("Direct configuration"):
                iteration_counter += 1
                main = {f'{atom}_{j + 1}': [] for j in range(atom_counts[atom_symbols.index(atom)])}
                pos = main.copy()
                positions = [list(map(float, lines[j].split())) for j in range(i + 1, i + sum(atom_counts))]
                scaled_positions = list([x_scale * x, y_scale * y, z_scale * z] for x, y, z in positions)
                specific_positions = list(scaled_positions)[lower_bound - 1:upper_bound]

                for k, positions in enumerate(specific_positions):
                    pos[f'{atom}_{k + 1}'] = positions


                distances = {key: [] for key in pos}
                for key1, value1 in pos.items():
                    for key2, value2 in pos.items():
                        if key1 != key2:  
                            d = dist(value1, value2)
                            distances[key1].append(d)

                sij = {key: [] for key in distances}  
                for key, value in distances.items():
                    sij[key].append([switching(d, d0=1.5, r0=1, n=6, m=12) for d in value])


                sij_cond = {key: [v for sublist in values for v in sublist if v > 0.3] for key, values in sij.items()}
                

                ethane_lists = []
                processed_atoms = set()
                for key, value in sij_cond.items():
                    if key not in processed_atoms and value:
                        ethane = [key]
                        processed_atoms.add(key)
                        for other_key, other_value in sij_cond.items():
                            if key != other_key and other_key not in processed_atoms and other_value == value:
                                ethane.append(other_key)
                                processed_atoms.add(other_key)
                        ethane_lists.append(tuple(ethane))


                for ethane in ethane_lists:
                    if ethane not in radial_distances_iteration:
                        radial_distances_iteration[ethane] = []
                    if ethane not in z_distances_iteration:
                        z_distances_iteration[ethane] = []


                for ethane in ethane_lists:
                    ethane_positions[ethane] = np.mean([pos[key] for key in ethane], axis=0)

                    #CHANGE START AND END LINES FOR RUTHENIUM POSITION VALUES
                    #i REFERENCES INDEX OF LINE CONTAINING STRING "DIRECT CONFIGURATION"
                    #sum(atom_counts[:2]) REFERENCES SUM OF C AND H LINES

                    #EX: IN A 6 C, 26 H, AND 48 Ru SYSTEM,  
                    #ruthenium_positions_start = i + 1 + sum(atom_counts[:2] = 7 + 1 + (6+26) = 40 = INDEX OF LINE CONTAINING FIRST RU POSITION
                    #MEANING FIRST Ru POSITION IS LINE 41 OF XDATCAR
                    #ruthenium_positions_end = ruthenium_positions_start + 48Ru Atoms = 40 + 48 = 88 = INDEX OF LINE CONTAINING LAST RU POSITION
                    #THE AVERAGE OF ALL THESE POSITIONS WILL BE TAKEN WITH ruthenium_positions = np.mean(ruthenium_positions, axis=0) AND WILL SERVE AS THE POINT WHERE THE RUTHENIUM SLAB IS DEFINED

                    ruthenium_positions_start = i + 1  + sum(atom_counts[:2])
                    ruthenium_positions_end = ruthenium_positions_start + 12 # + HOWEVER MANY INDEXES YOU WANT YOUR RUTHENIUM POSITIONS TO END IN
                    ruthenium_positions = [list(map(float, lines[j].split())) for j in range(ruthenium_positions_start, ruthenium_positions_end)]

                    ruthenium_positions = np.mean(ruthenium_positions, axis=0)

                    ethane_radial_distances[ethane] = [dist(ethane_positions[ethane], ruthenium_pos) for ruthenium_pos in ruthenium_positions]
                    ethane_z_distances[ethane] = [ethane_positions[ethane][2] - ruthenium_positions[2]]


                average_radial_distances, average_z_distances = {}, {}
                for key, value in ethane_radial_distances.items():
                    average_radial_distances[key] = np.average(value)
                for key, value in ethane_z_distances.items():
                    average_z_distances[key] = np.average(value)

                for key, value in average_radial_distances.items():
                    radial_distances_iteration[key].append(value)
                for key, value in average_z_distances.items():
                    z_distances_iteration[key].append(value)


    x_axis = np.arange(1, iteration_counter + 1, 1)
    for key, values in radial_distances_iteration.items():
        if not all(np.isnan(val) for val in values):
            plt.plot(x_axis, values, label=str(key))

    plt.xlabel('Iteration')
    plt.ylabel('Distance (Ang)')
    plt.legend(title='Ethane')
    plt.title(f'Radial Distance Between Ethane and Ruthenium Slab')
    plt.show()

    for key, values in z_distances_iteration.items():
        if not all(np.isnan(val) for val in values):
            plt.plot(x_axis, values, label=str(key))

    plt.xlabel('Iteration')
    plt.ylabel('Distance (Ang)')
    plt.legend(title='Ethane')
    plt.title(f'Z Distance Between Ethane and Ruthenium Slab')
    plt.show()

#parser(INPUPT FILE, "C" FOR ETHANE)
parser("XDATCAR_first500", "C")
