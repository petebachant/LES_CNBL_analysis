"""Plot wake recovery
in wind farm LES
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp
from scipy import stats
from scipy.optimize import curve_fit

plt.style.use("plots/style.mplstyle")

case_id = 'H1000-C5-G4'

#vertical grid - use cell centered points  
with open('/mnt/d/LES_data/zmesh','r') as file:       
    Nz_full     = int(float(file.readline()))   
    N_line = Nz_full+1
    line = N_line*[0]
    cnt = 0
    for lines in file:
        line[cnt]=lines.split()
        cnt+=1       
    z = np.array([float(line[k][0]) for k in range(int(Nz_full))])[1::2]

#define x, y, z coordinates
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)

#create meshgrid
xg, yg ,zg = np.meshgrid(x, y, z, indexing='ij', sparse=True)

#load u data
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_main_first_order.h5', 'r')
u = f['u']
v = f['v']

#plot farm area and wake tracks
xx, yy = np.meshgrid(x, y)
fig, ax = plt.subplots(figsize=[6,4], dpi=300)
plt.pcolormesh(xx[450:1000,544:1120]/1000, yy[450:1000,544:1120]/1000, u[544:1120,450:1000,23].T,shading='nearest', vmin=2, vmax=10)
cbar = plt.colorbar()
cbar.set_label(r'$u$ (m/s)')
plt.ylim([10,20])
plt.xlim([17.5,35])
plt.xlabel(r'x (km)')
plt.xlabel(r'y (km)')
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig(f'plots/{case_id}/farm_area.png')

plt.plot([23.415, 26.3835, 26.3825, 23.415, 23.415],
    [14.505, 14.505, 15.99, 15.99, 14.505], c='r')
plt.savefig(f'plots/{case_id}/farm_area_box.png')

plt.ylim([14.505,15.99])
plt.xlim([23.415,26.3835])
plt.savefig(f'plots/{case_id}/farm_area_zoom.png')


