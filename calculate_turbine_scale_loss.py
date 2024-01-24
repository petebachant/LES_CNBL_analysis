"""Calculate turbine-scale power
loss for wind farm LES
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp
import scipy.optimize as opt

case_id = 'H500-C0-G0'
u_star0 = 0.277

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

##############################################
# 1. Calculate U_F0
##############################################

#open precursor file
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_first_order.h5', 'r')
u = f['u']
v = f['v']

#horziontally average
u = np.mean(u[:,:,:100], axis=(0,1))
v = np.mean(v[:,:,:100], axis=(0,1))

#interpolate
interp_u = sp.interp1d(1000*z[:100], 
    u, bounds_error=False, fill_value='extrapolate')
interp_v = sp.interp1d(1000*z[:100], 
    v, bounds_error=False, fill_value='extrapolate')

#calculate wind direction at turbine height
u_hubh = interp_u(119)
v_hubh = interp_v(119)
angle_hubh = np.arctan(v_hubh/u_hubh)

#number of vertical levels for intergration
n_z = 100
u_farm_layer = interp_u(np.linspace(0,2.5*119,n_z))
v_farm_layer = interp_v(np.linspace(0,2.5*119,n_z))
u_f0 = np.mean(u_farm_layer)*np.cos(angle_hubh) + np.mean(v_farm_layer)*np.sin(angle_hubh)

plt.plot(u_farm_layer, np.linspace(0,2.5*119,n_z))
plt.plot(v_farm_layer, np.linspace(0,2.5*119,n_z))
plt.ylim([0,2.5*119])
plt.axvline(u_f0)
plt.savefig('plots/vertical_velocity_profiles.png')
plt.close()



#check convergence of u_f0 calculation with vertical levels
while False:
    n_z_values = np.linspace(10,500,10)
    u_f0_convergence = np.zeros(10)
    for i, n_z in enumerate(n_z_values):
        print(n_z)
        n_z = int(n_z)
        u_farm_layer = interp_u(np.linspace(0,2.5*119,n_z))
        v_farm_layer = interp_v(np.linspace(0,2.5*119,n_z))
        u_f0_convergence[i] = np.mean(u_farm_layer)*np.cos(angle_hubh) + np.mean(v_farm_layer)*np.sin(angle_hubh)
    plt.plot(n_z_values, u_f0_convergence)
    plt.ylim([0,10])
    plt.savefig('plots/u_f0_convergence.png')
    plt.close()

##############################################
# 2. Calculate U_F
##############################################

aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
#calculate average yaw angle
#yaw in degrees
yaw = aux['yaw']
time = aux['time']
yaw_mean = np.mean(yaw[time[:]>75600,:],axis=0)

#calculate turbine force
force = aux['force']
plt.plot(time[:], np.mean(force[:,:],axis=1))
#forces in the direction of averge yaw angle
force_hubh = force*np.cos((yaw-yaw_mean)*np.pi/180)
plt.plot(time[:], np.mean(force_hubh[:,:],axis=1))
#average turbine force over last 1.5hrs of simulation
force_ave = np.mean(force_hubh[time[:]>75600,:])
plt.plot([75600,81000],[force_ave,force_ave])
plt.savefig('plots/turbine_force.png')
plt.close()

#define x, y, z coordinates
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)

#open velocity file
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_main_first_order.h5', 'r')
u = f['u']
v = f['v']

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

#check convergence of u_f calculation with horizontal discretisation
while False:
    n_xy_values = np.linspace(10,500,10)
    u_f_convergence = np.zeros(10)
    for i, n_xy in enumerate(n_z_values):

        print(n_xy)
        n_x = int(n_xy)
        n_y = int(n_xy)

        x_farm = np.linspace(17.4735e3,33.3135e3,n_x)
        y_farm = np.linspace(10.050e3,19.950e3,n_y)
        z_farm = np.linspace(0,2.5*119,n_z)
        xg, yg, zg = np.meshgrid(x_farm, y_farm, z_farm)

        pos = np.zeros((n_x*n_y*n_z,3))
        pos[:,0] = xg.flatten()
        pos[:,1] = yg.flatten()
        pos[:,2] = zg.flatten()

        u = np.mean(interp_u(pos))
        v = np.mean(interp_v(pos))

        yaw_mean_rad = np.pi*np.mean(yaw_mean)/180
        u_f_convergence[i] = u*np.cos(yaw_mean_rad)+v*np.sin(yaw_mean_rad)

    plt.plot(n_xy_values, u_f_convergence)
    plt.ylim([0,10])
    plt.savefig('plots/u_f_convergence.png')

#################################
# 3. Calculate M and zeta
#################################
beta = u_f/u_f0
print(beta**3)

M = force_ave/(5**2 * 198**2 * u_star0**2) + beta**2
zeta = (M-1)/(1-beta)

#################################
# 4. Calculate C_{p,Nishino}
#################################

array_density = np.pi/(4*5*5)
ctstar = 0.88*1.107
cf0 = u_star0**2/(0.5*u_f0**2)

def ndfm(beta):
    lhs = ctstar*(array_density/cf0)*beta**2 + beta**2

    rhs = 1 + zeta*(1-beta)
    
    return lhs - rhs

beta = opt.bisect(ndfm,1,0.3)
print(beta**3)