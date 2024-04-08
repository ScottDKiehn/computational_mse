import numpy as np
import matplotlib.pyplot as plt
from ase.io import read
import MDAnalysis as mda

def calculate_rdf(atom_selection1, atom_selection2, trajectory_path, r_max=10.0, dr=0.1):
    # Load the trajectory using MDAnalysis and explicitly specify the format
    u = mda.Universe(trajectory_path, topology_format="vasp-xdatcar")

    # Get the indices of atoms for the RDF calculation
    indices1 = [i for i, atom in enumerate(u.atoms) if atom.symbol == atom_selection1]
    indices2 = [i for i, atom in enumerate(u.atoms) if atom.symbol == atom_selection2]

    # Initialize RDF array
    rdf, edges = np.histogram([], bins=np.arange(0, r_max + dr, dr), density=True)

    # Loop over frames in the trajectory
    for ts in u.trajectory:
        positions1 = ts.positions[indices1]
        positions2 = ts.positions[indices2]

        box = ts.dimensions[:3]

        # Compute distances between atoms in the two selections
        distances = mda.lib.distances.distance_array(positions1, positions2, box=box)

        # Update RDF histogram
        rdf_frame, _ = np.histogram(distances.flatten(), bins=edges, density=True)
        rdf += rdf_frame

    # Average RDF over all frames
    rdf /= len(u.trajectory)

    # Normalize RDF
    norm = 4 * np.pi * rdf * dr

    return edges[:-1], norm

def plot_rdf(r, rdf, label=None):
    plt.plot(r, rdf, label=label)

if __name__ == "__main__":
    # Example usage
    atom_selection1 = "C"  # Atom type for selection 1
    atom_selection2 = "H"  # Atom type for selection 2
    trajectory_path = "./lammps/traj_150.0_u_small.lammpstrj"

    r, rdf = calculate_rdf(atom_selection1, atom_selection2, trajectory_path)

    plt.figure()
    plot_rdf(r, rdf, label=f'{atom_selection1} - {atom_selection2}')
    plt.xlabel("Distance (Angstrom)")
    plt.ylabel("RDF")
    plt.legend()
    plt.show()
