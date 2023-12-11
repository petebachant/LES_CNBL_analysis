"""Plot farm flow profiles
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

case_id = 'H300-C8-G1'


y_pos = 15247.5
y_id = int(y_pos//21.74)

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

#interpolate in y direction
f_u_x = sp.interp1d([y_id*21.74, (y_id+1)*21.74], u[:,y_id:y_id+2,:100], axis=1)
u_xz = f_u_x(y_pos)

#define colormap
cmap = plt.get_cmap('viridis', 8)

for j in range(8):

    u_min = np.zeros(10)
    #loop over different x positions
    for i in range(10):

        x_pos = 17.9685e3+(j*10*198)+i*198
        #interpolate in y direction
        f_u = sp.interp1d(31.25*np.arange(1600), u_xz, axis=0)
        u_slice = f_u(x_pos)

        #plot u velocity
        #plt.plot(u_slice, 1000*z[:100], c=cmap(i))
        #plt.savefig('plots/wake_profiles.png')

        f_u = sp.interp1d(1000*z[:100], u_slice, axis=0)
        u_min[i] = f_u(119)

    plt.plot(np.arange(10), u_min, c=cmap(j))
    plt.savefig('plots/wake_recovery.png')

aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
print(np.mean(np.abs(aux['yaw'])))