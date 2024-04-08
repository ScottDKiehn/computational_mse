import MDAnalysis as mda
import numpy as np
import matplotlib.pyplot as plt
from MDAnalysis.analysis.rdf import InterRDF

trajectory_path = 'path/to/your/trajectory.lammpstrj'
topology_path = 'path/to/your/trajectory.lammpstrj'

u = mda.Universe(trajectory_path, topology_path)

selection_g1 = 'C'
selection_g2 = 'H'

ag1 = u.select_atoms(selection_g1)
ag2 = u.select_atoms(selection_g2)

nbins = 75
rdf_range = (0.0, 15.0)
exclusion_block = None

rdf = InterRDF(ag1, ag2, nbins=nbins, range=rdf_range, exclusion_block=exclusion_block)

rdf.run()

plt.plot(rdf.bins, rdf.rdf)
plt.xlabel('Distance (Angstrom)')
plt.ylabel('RDF')
plt.title('Radial Distribution Function (RDF) between C and H')
plt.show()

#Coordination Number:
#N_{ab}(R) = 4pi*integral_0^r rdf(r)*r^2dr
coordination_number = 4 * np.pi * np.trapz(rdf.rdf * rdf.bins**2, rdf.bins)

#rdf.rdf * rdf.bins**2 --> element-wise multiplication of the RDF values by the 
# square of the corresponding radial distances. This operation effectively scales 
# each RDF value by the square of the distance.