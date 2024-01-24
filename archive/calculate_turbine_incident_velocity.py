"""Calculate the velocity
incident on every turbine and compare
with U_F
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

case_id = 'H300-C8-G1'

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


aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
#calculate average yaw angle
#yaw in degrees
yaw = aux['yaw']
time = aux['time']
yaw_mean = np.mean(yaw[time[:]>75600,:],axis=0)
yaw = np.mean(yaw[time[:]>75600,:],axis=0)

#open velocity file
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_main_first_order.h5', 'r')
u = f['u']
v = f['v']

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

#grid to extrapolate shear stress onto
n_x = 500
n_y = 500
n_z = 100
x_farm = np.linspace(17.4735e3,33.3135e3,n_x)
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

print(u_f)


#x position of turbine no.0
x_pos_turb = 17.9685e3
#y position of turbine no.0
y_pos_turb = 10.2475e3 + 50

k=0
j=0

upstream_distance = np.linspace(0,-3,30)
upstream_velocity = np.zeros((16,10,30))

#loop over turbine row
for k in range(16):

    #loop over turbine column
    for j in range(10):

        #loop over x positions
        for i, distance in enumerate(upstream_distance):

            x_pos = x_pos_turb + distance*198*np.cos(np.pi*yaw[j+k*10]/180) + 5*198*k
            #staggered alternate rows
            if k%2 == 0:
                y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j+k*10]/180) + 5*198*j
            else:
                y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j+k*10]/180) + 5*198*j + 2.5*198

            pos = np.array([x_pos, y_pos, 119])
            u_upstream = interp_u(pos)
            v_upstream = interp_v(pos)

            upstream_velocity[k,j,i] = u_upstream*np.cos(np.pi*yaw[j+k*10]/180) + v_upstream*np.sin(np.pi*yaw[j+k*10]/180)

plt.plot(upstream_distance, np.mean(upstream_velocity,axis=(0,1)))
plt.axhline(u_f)
plt.savefig('plots/upstream_velocity.png')