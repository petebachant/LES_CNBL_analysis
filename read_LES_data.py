import h5py
import matplotlib.pyplot as plt
import numpy as np

f = h5py.File('/mnt/c/Users/trin3517/Documents/PhD/Year 4/Research plots and presentations/LES_data/H500-C5-G4/stat_main_first_order.h5', 'r')

cmap = plt.get_cmap('seismic')
p = f['p']
p = np.mean(p[:,460:920,:300], axis=1) - np.mean(p[0,460:920,:300], axis=0)

x = np.arange(0,50000,31.25)
z = np.arange(2.5,1500,5)
plt.figure(figsize=[8,1])
plt.pcolormesh(x, z, p.T, cmap=cmap, shading='nearest', vmin=-18, vmax=18)
plt.savefig('p_slice_H500-C5-G4.png')
