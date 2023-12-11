"""Plot the distribution of yaw angles
for different wind farms
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp


case_id = 'H300-C2-G1'

aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
yaw = aux['yaw']
time = aux['time']
yaw = np.mean(yaw[time[:]>75600,:],axis=0)

plt.hist(yaw.flatten(), bins=10, density=True)
plt.xlabel('Turbine yaw (deg)')
plt.ylabel('Density')
plt.axvline(-2.87, c='r')
plt.axvline(2.87, c='r')
plt.savefig('plots/turbine_yaw_histogram.png')