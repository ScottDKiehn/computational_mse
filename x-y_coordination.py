import matplotlib.pyplot as plt
import numpy as np

def switching(rij, d0, r0, n, m):
    top = (1 - ((rij - d0) / r0)**n)
    bottom = (1 - ((rij - d0) / r0)**m)
    sij = top / bottom
    return sij

def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def parser(input, atom1, atom2):
    with open(input, "r") as l:
        lines = l.readlines()
        iteration_counter = 0
        
        #CHANGE THESE PARAMETERS BASED ON SCALING LINES 3,4,5 IN XDATCAR. ONLY SUPPORTS CUBIC SYSTEMS
        x_scale = 7.994037
        y_scale = 9.271353
        z_scale = 27.081524


        for i, line in enumerate(lines):
            if i == 5:
                atom_symbols = line.split()
            elif i == 6:
                atom_counts = list(map(int, line.split()))
                atom_pos_dict = {f'{atom1}_{j+1}': 0 for j in range(int(atom_counts[atom_symbols.index(atom1)]))}
                atom_diff_dict = {f'{atom1}_{j+1}': [] for j in range(int(atom_counts[atom_symbols.index(atom1)]))}
                atom_dist_dict = {f'{atom1}_{j+1}': [] for j in range(int(atom_counts[atom_symbols.index(atom1)]))}
                atom_sij_dict = {f'{atom1}_{j+1}': [] for j in range(int(atom_counts[atom_symbols.index(atom1)]))}
                atom_sij_condition_dict = {f'{atom1}_{j+1}': [] for j in range(int(atom_counts[atom_symbols.index(atom1)]))}
                sum_sij_iteration_dict = {f'{atom1}_{j+1}': [] for j in range(int(atom_counts[atom_symbols.index(atom1)]))}
                specific_position_count1, specific_position_count2 = int(atom_counts[atom_symbols.index(atom1)]), int(atom_counts[atom_symbols.index(atom2)])
                upper_bound1 = sum(atom_counts[:(atom_counts.index(specific_position_count1)+1)])
                lower_bound1 = upper_bound1 - specific_position_count1 + 1
                upper_bound2 = sum(atom_counts[:(atom_counts.index(specific_position_count2)+1)])
                lower_bound2 = upper_bound2 - specific_position_count2 + 1

            if line.startswith("Direct configuration"):
                positions = [list(map(float, lines[j].split())) for j in range(i+1, i+sum(atom_counts))]
                scaled_positions = list([x_scale*x, y_scale*y, z_scale*z] for x, y, z in positions)
                specific_positions_data_atom1 = list(scaled_positions)[lower_bound1-1:upper_bound1]
                specific_positions_data_atom2 = list(scaled_positions)[lower_bound2-1:upper_bound2]

                iteration_counter += 1

                for k, positions in enumerate(specific_positions_data_atom1):
                    atom_pos_dict[f'{atom1}_{k+1}'] = positions


                for k, positions_atom2 in enumerate(specific_positions_data_atom2):
                    for j, position_atom1 in atom_pos_dict.items():
                        dist = euclidean_distance(positions_atom2, position_atom1)


                        #REFINE SWTICHING FUNCTION PARAMETERS HERE:
                        #d_0 = CUTOFF (OR BOND) DISTANCE (IN ANG) FOUND FROM X_Y_HISTOGRAM.PY
                        #r_0 = DISTANCE (IN ANG) WITH WHICH BOND IS CONSIDERED SIGNIFICANT. INCREASE TO MAKE LESS SENSITIVE
                        #n AND m SHOULD REMAIN 6 AND 12 RESPSECTIVELY
                        coord = switching(dist, d0=1.5, r0=.5, n=6, m=12)
                        atom_dist_dict[j].append(dist)
                        atom_sij_dict[j].append(coord)



                for key, values in atom_sij_dict.items():
                    filtered_values = [value for value in values if value > 0.99]
                    atom_sij_condition_dict[key] = filtered_values

                sum_dict = {key: [sum(values)] for key, values in atom_sij_dict.items()}
                #print(sum_dict)
                for key, value in sum_dict.items():
                    sum_sij_iteration_dict[key].append(value[0])

                #print(atom_dist_dict)
                #print(atom_sij_dict)
                #print(atom_sij_condition_dict)
                atom_dist_dict.clear()
                atom_sij_dict.clear()
                atom_sij_condition_dict.clear()
                atom_dist_dict = {f'{atom1}_{j+1}': [] for j in range(int(atom_counts[atom_symbols.index(atom1)]))}
                atom_sij_dict = {f'{atom1}_{j+1}': [] for j in range(int(atom_counts[atom_symbols.index(atom1)]))}
                atom_sij_condition_dict = {f'{atom1}_{j+1}': [] for j in range(int(atom_counts[atom_symbols.index(atom1)]))}

        #print(sum_sij_iteration_dict)
                
        x_axis = np.arange(1, iteration_counter +1, 1)

       
    for key, values in sum_sij_iteration_dict.items():
        plt.plot(x_axis, values, label=key)

    plt.xlabel('Iteration')
    plt.ylabel('Sum of sij values')
    plt.legend(title='Atoms')
    plt.title(f'Coordination Number as a Function of Iteration Between {atom1} and {atom2}')
    plt.show()
        



parser("XDATCAR_system2", "C", "H")
