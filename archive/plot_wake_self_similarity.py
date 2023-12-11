"""Plot self similar wakes
in wind farm LES
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

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
plt.figure(1)
xx, yy = np.meshgrid(x, y)
plt.figure(1)
plt.pcolormesh(xx[450:1000,544:1120], yy[450:1000,544:1120], u[544:1120,450:1000,23].T,shading='nearest')
plt.colorbar()
plt.ylim([10e3,20e3])
plt.xlim([17.5e3,35e3])
plt.savefig('plots/farm_area.png')
plt.close()

#create interpolating function for gridded data
print('Begin interpolation')
interp_u = sp.RegularGridInterpolator((x[544:1120], y[450:1000], 1000*z[:100]), u[544:1120,450:1000,:100])
interp_v = sp.RegularGridInterpolator((x[544:1120], y[450:1000], 1000*z[:100]), v[544:1120,450:1000,:100])
print('Interpolation finished')

#coordinates for interpolation and averaging
x_interp = np.linspace(17.9685e3, 33.8085e3, 1000)
y_interp = np.linspace(10.05e3, 19.95e3, 1000)

xg_interp, yg_interp = np.meshgrid(x_interp, y_interp, indexing='ij')
#array to store coordinates to evaluate
pos = np.zeros((1000000, 3))
pos[:, 0] = xg_interp.flatten()
pos[:, 1] = yg_interp.flatten()

#array to store results
u_profile = np.zeros(100)
v_profile = np.zeros(100)


#calculate farm averaged values
for z_index in range(100):

    print(z_index)
    pos[:, 2] = 1000*z[z_index]
    u_profile[z_index] = np.mean(interp_u(pos))
    v_profile[z_index] = np.mean(interp_v(pos))

#load precursor data
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_first_order.h5', 'r')
u_precursor = f['u']
u_prec_profile = np.mean(u_precursor[:,:,:100],axis=(0,1))

plt.plot(u_prec_profile - u_profile, 1000*z[:100])
plt.savefig('plots/wake_self_similarity.png')