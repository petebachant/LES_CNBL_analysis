"""Calculate farm-layer height H_F
for precursor simulations
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

case_id = f'H500-C5-G4_st'

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

#plot u and v profile from precursor simulation
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_first_order.h5', 'r')
u = f['u']
u_profile = np.mean(u[:,:,:120],axis=(0,1))
v = f['v']
v_profile = np.mean(v[:,:,:120],axis=(0,1))

speed = np.sqrt(u_profile**2+v_profile**2)
#angle in degrees!
angle = np.arctan(v_profile/u_profile)

#interpolate speed and velocity
f_speed = sp.interp1d(1000*z[:120], speed, fill_value="extrapolate")
f_angle = sp.interp1d(1000*z[:120], angle, fill_value="extrapolate")
hubh_angle = f_angle(119)

#turbine hub height
h = 119
#turbine diameter
d = 198
print(d,h)

nz = 1000000
z = np.linspace(-d/2,d/2,nz)

#rotor section width
width = 2*np.sqrt((d**2)/4 - z**2)
u = f_speed(h+z)*np.cos(f_angle(h+z)-hubh_angle)

#calculate U_T0
area = np.sum(width*(d/nz))
disc_vel = np.sum(u*width*(d/nz))/area
print(disc_vel, f_speed(119))

z = np.linspace(0,297.5,10000)
speed_interp = f_speed(z)*np.cos(f_angle(z)-hubh_angle)
plt.plot(speed_interp, z)
plt.axhline(119)
plt.axvline(9.24)
plt.savefig('plots/u_profile.png')
print(np.mean(speed_interp))

disc_vel = np.sum(u**2*width*(d/nz))/area
disc_vel = np.sqrt(disc_vel)
print(disc_vel)


