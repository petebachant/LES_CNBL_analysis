"""Calculate turbine-scale power
loss for wind farm LES
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

case_id = 'H1000-C5-G4'

aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
#calculate average yaw angle
#yaw in degrees
yaw = aux['yaw']
time = aux['time']
yaw_mean = np.mean(yaw[time[:]>75600,:],axis=0)

#calculate turbine force
force = aux['force']
#forces in the direction of averge yaw angle
force_hubh = force*np.cos((yaw-yaw_mean)*np.pi/180)
#average turbine force over last 1.5hrs of simulation
force_ave = np.mean(force_hubh[time[:]>75600,:])

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

#open shear stress file
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_main_second_order.h5', 'r')
uw = f['uw']
vw = f['vw']
#open sub-grid shear stress file
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_main_second_order_sgs.h5', 'r')
uw_sgs = f['uw_sgs']
vw_sgs = f['vw_sgs']

#create interpolating function for gridded data
print('Begin interpolation')
interp_uw = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    uw[544:1120,400:1050,:100], bounds_error=False, fill_value=None)
interp_uw_sgs = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    uw_sgs[544:1120,400:1050,:100], bounds_error=False, fill_value=None)
interp_vw = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    vw[544:1120,400:1050,:100], bounds_error=False, fill_value=None)
interp_vw_sgs = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    vw_sgs[544:1120,400:1050,:100], bounds_error=False, fill_value=None)
print('Interpolation finished')

#grid to extrapolate shear stress onto
n_x = 500
n_y = 500

uw = np.zeros(100)
uw_sgs = np.zeros(100)
vw = np.zeros(100)
vw_sgs = np.zeros(100)
for i in range(100):
    print(i)
    x_farm = np.linspace(17.4735e3,33.3135e3,n_x)
    y_farm = np.linspace(10.050e3,19.950e3,n_y)
    z_farm = 1000*z[i]
    xg, yg, zg = np.meshgrid(x_farm, y_farm, z_farm)
    pos = np.zeros((n_x*n_y,3))
    pos[:,0] = xg.flatten()
    pos[:,1] = yg.flatten()
    pos[:,2] = zg.flatten()

    uw[i] = np.mean(interp_uw(pos))
    uw_sgs[i] = np.mean(interp_uw_sgs(pos))
    vw[i] = np.mean(interp_vw(pos))
    vw_sgs[i] = np.mean(interp_vw_sgs(pos))

plt.plot(uw, 1000*z[:100])
plt.plot(uw_sgs, 1000*z[:100])
plt.plot(vw, 1000*z[:100])
plt.plot(vw_sgs, 1000*z[:100])
plt.axhline(218)
plt.axhline(20)
plt.savefig('plots/uw.png')
plt.close()
