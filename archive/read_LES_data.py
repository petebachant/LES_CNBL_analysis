import h5py
import matplotlib.pyplot as plt
import numpy as np

f = h5py.File('/mnt/d/LES_data/H1000-C5-G4/aux_files.h5', 'r')

force = f['force']
time = f['time']

plt.plot(time[:], force[:,100])
plt.savefig('plots/turbine_force.png')
