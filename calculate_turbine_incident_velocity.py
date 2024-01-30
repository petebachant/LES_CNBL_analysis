"""Calculate the velocity
incident on every turbine and compare
with U_F
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

case_id = 'H300-C5-G4'
#y position of turbine column
y_pos_turb = 10.2975e3 + 5*5*198

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
plt.ylabel(r'y (km)')
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig(f'plots/{case_id}/farm_area.png')

plt.plot([16.9785, 33.8085], [y_pos_turb/1000, y_pos_turb/1000], c='r')
plt.savefig(f'plots/{case_id}/farm_area.png')
plt.close()

#define x, y, z coordinates
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)

#create interpolating function for gridded data
print('Begin interpolation')
interp_u = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    u[544:1120,400:1050,:100], bounds_error=False, fill_value=None)
interp_v = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    v[544:1120,400:1050,:100], bounds_error=False, fill_value=None)
print('Interpolation finished')

#x positions for interpolation
x_positions = np.linspace(16.9785e3, 33.8085e3, 1000)
#create array of 3d position coordinates
interp_positions = np.zeros((1000,3))
#set x coordinates
interp_positions[:,0] = x_positions
#set y coordinates
interp_positions[:,1] = y_pos_turb*np.ones(1000)
#set z coordinates
interp_positions[:,2] = 119*np.ones(1000)
u_turbine_column = interp_u(interp_positions)

plt.plot(x_positions, u_turbine_column**3)
plt.savefig(f'plots/{case_id}/farm_x_slice.png')

#calculate U_F

aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
#calculate average yaw angle
#yaw in degrees
yaw = aux['yaw']
time = aux['time']
yaw_mean = np.mean(yaw[time[:]>75600,:],axis=0)

#grid to extrapolate shear stress onto
n_x = 500
n_y = 500
n_z = 100
x_farm = np.linspace(17.523e3,33.363e3,n_x)
y_farm = np.linspace(10.050e3,19.950e3,n_y)
z_farm = np.linspace(0,2.5*119,n_z)
xg, yg, zg = np.meshgrid(x_farm, y_farm, z_farm)
pos = np.zeros((n_x*n_y*n_z,3))
pos[:,0] = xg.flatten()
pos[:,1] = yg.flatten()
pos[:,2] = zg.flatten()

#calculate average u and v
u = np.mean(interp_u(pos))
v = np.mean(interp_v(pos))

yaw_mean_rad = np.pi*np.mean(yaw_mean)/180

u_f = u*np.cos(yaw_mean_rad)+v*np.sin(yaw_mean_rad)

plt.axhline(u_f**3)
plt.savefig(f'plots/{case_id}/farm_x_slice.png')