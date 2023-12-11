"""Plot farm flow profiles
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

f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_main_first_order.h5', 'r')
u = f['u']

#check farm area
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)
xx, yy = np.meshgrid(x, y)

#interpolate in z direction
f_u_z = sp.interp1d(1000*z[23:25], u[:,:,23:25])
u_xy = f_u_z(119)
    
#plot farm flow field
plt.figure(1)
plt.pcolormesh(xx, yy, u_xy.T,shading='nearest')
plt.colorbar()
plt.plot([23.415e3, 26.3835e3, 26.3825e3, 23.415e3, 23.415e3],
    [14.505e3, 14.505e3, 15.99e3, 15.99e3, 14.505e3], c='r')
plt.ylim([10e3,20e3])
plt.xlim([17.5e3,35e3])
plt.savefig('plots/farm_area.png')
plt.close(1)

#plot zoomed in profile
plt.figure(2)
plt.pcolormesh(xx, yy, u_xy.T,shading='nearest', vmin=2, vmax=10)
plt.colorbar()
plt.ylim([14.505e3,15.99e3])
plt.xlim([23.4135e3,26.3835e3])
plt.savefig('plots/farm_area_zoom.png')
plt.close(2)

#plot zoomed in profile
plt.figure(3)
plt.pcolormesh(xx, yy, u_xy.T,shading='nearest', vmin=2, vmax=10)
plt.colorbar()
for i in range(10):
    plt.plot([23.908e3+i*198, 23.908e3+i*198], [14.7525e3, 15.7425e3], c='r')
plt.ylim([14.505e3,15.99e3])
plt.xlim([23.4135e3,26.3835e3])
plt.savefig('plots/farm_area_zoom1.png')
plt.close(3)

#plot wake profiles
cmap = plt.get_cmap('viridis', 10)
#interpolate in x direction
f_u_y = sp.interp1d(31.25*np.arange(1600), u_xy, axis=0)

for i in range(10):
    x_pos = 23.908e3+i*198
    #spanwise average u velocity
    f_u_y_ave = sp.interp1d(21.74*np.arange(1380), f_u_y(x_pos))
    u_y_ave = f_u_y_ave(np.linspace(14.7525e3,15.7425e3, 500))
    plt.plot(u_y_ave, np.linspace(-2.5*198, 2.5*198, 500), c=cmap(i))

plt.axhline(99.5)
plt.axhline(-99.5)
plt.savefig('plots/wake_profiles.png')



