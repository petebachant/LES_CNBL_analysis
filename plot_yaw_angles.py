"""Plot the distribution of yaw angles
for different wind farms
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

plt.style.use("plots/style.mplstyle")

case_id = 'H1000-C5-G4'

aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
yaw = aux['yaw']
time = aux['time']
yaw = np.mean(yaw[time[:]>75600,:],axis=0)

fig, ax = plt.subplots(figsize=[6,4], dpi=300)
plt.hist(yaw.flatten(), bins=10, density=True)
plt.xlabel('Turbine yaw (deg)')
plt.ylabel('Density')
plt.axvline(-2.87, c='r')
plt.axvline(2.87, c='r')
plt.tight_layout()
plt.savefig(f'plots/{case_id}/turbine_yaw_histogram.png')