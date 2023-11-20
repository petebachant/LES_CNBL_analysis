"""Check convergence of LES simulations
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

case_id = f'H300-C5-G4'

#load force and time from auxiliary file
f = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
thrust = f['force']
print(thrust.shape)
time = f['time']
plt.plot(time[:], np.mean(thrust, axis=1))
plt.axvline(75600)
plt.savefig('plots/turbine_force.png')

#change averaging period
thrust_ave = np.zeros(1800)

for i in range(1800):
    thrust_ave[i] = np.mean(thrust[range(-(i+2),-1),:])/np.mean(thrust[time[:]>75600,:])

plt.close()
plt.plot(thrust_ave)
plt.axvline(1080)
plt.savefig('plots/turbine_force_averaging_period_norm.png')