"""Plot farm flow profiles
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

case_id = 'H300-C2-G1'

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
#interpolate in x direction
f_u_y = sp.interp1d(31.25*np.arange(1600), u_xy, axis=0)

while True:
    x_pos = input('Enter x position: ')
    
    #plot x position on farm flow field
    plt.figure(1)
    plt.pcolormesh(xx, yy, u_xy.T,shading='nearest')
    plt.colorbar()
    plt.axvline(float(x_pos), c='red')
    plt.ylim([10e3,20e3])
    plt.xlim([17.5e3,35e3])
    plt.savefig('plots/farm_area.png')
    plt.close(1)

    #spanwise average u velocity
    f_u_y_ave = sp.interp1d(21.74*np.arange(1380), f_u_y(x_pos))
    u_y_ave = np.mean(f_u_y_ave(np.linspace(10.1e3,19.9e3, 500)))

    plt.figure(2)
    #plot spanwise slice of hubh u velocity
    plt.plot(f_u_y(x_pos), 21.74*np.arange(1380))
    #plot spanwise-averaged u velocity
    plt.axvline(u_y_ave)
    plt.ylim([10e3,20e3])
    plt.savefig('plots/u_hubh.png')
    plt.close(2)

