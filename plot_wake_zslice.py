"""Plot wake recovery
in wind farm LES
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp
from scipy import stats
from scipy.optimize import curve_fit

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

#load auxiliary data
aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
yaw = aux['yaw']
time = aux['time']
yaw = np.mean(yaw[time[:]>75600,:],axis=0)

#load precursor data
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_first_order.h5', 'r')
u_precursor = f['u']
u_prec_profile = np.mean(u_precursor[:,:,:100],axis=(0,1))

#create interpolating function for gridded data
print('Begin interpolation')
interp_u = sp.RegularGridInterpolator((x[544:1120], y[450:1000], 1000*z[:100]), u[544:1120,450:1000,:100])
interp_v = sp.RegularGridInterpolator((x[544:1120], y[450:1000], 1000*z[:100]), v[544:1120,450:1000,:100])
print('Interpolation finished')

#x position of turbine no.0
x_pos_turb = 17.9685e3
#y position of turbine no.0
y_pos_turb = 10.2475e3 + 50

#function to fit to wake deficits
def fit_func(z,a,b,c):
    return a*stats.norm.pdf(z,c,b*198)

wake_distance = np.linspace(2,9,8)
speed_min = np.zeros((10,8,100))

#define colormap
cmap1 = plt.get_cmap('viridis', 8)
cmap2 = plt.get_cmap('viridis', 16)

k=10

#loop over x positions
for i, distance in enumerate(wake_distance):

    #loop over turbine column
    for j in range(10):

                #loop over vertical column
                for z_index in range(100):

                    x_pos = x_pos_turb + distance*198*np.cos(np.pi*yaw[j]/180) + 5*198*k
                    #staggered alternate rows
                    if k%2 == 0:
                        y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j]/180) + 5*198*j
                    else:
                        y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j]/180) + 5*198*j + 2.5*198
                    plt.figure(1)
                    plt.scatter(x_pos, y_pos, c='r', s=1)

                    pos = np.array([x_pos, y_pos, 1000*z[z_index]])
                    u_min = interp_u(pos)
                    v_min = interp_v(pos)

                    speed_min[j, i, z_index] = u_min*np.cos(np.pi*yaw[j]/180) + v_min*np.sin(np.pi*yaw[j]/180)

    wake_profile = np.mean(speed_min, axis=0)
    plt.figure(2)
    plt.plot((u_prec_profile-wake_profile[i,:]), 1000*z[:100], c=cmap1(i))
    plt.savefig('plots/wake_recovery.png')

    #fit Gaussian function to wake deficit across turbine disk
    popt, pcov = curve_fit(fit_func, 1000*z[4:44], u_prec_profile[4:44]-wake_profile[i,4:44])
    print(popt[1])
    plt.plot(fit_func(1000*z[4:44], *popt), 1000*z[4:44], c='k')
    plt.savefig('plots/wake_recovery.png')

    #plt.figure(3)
    #plt.scatter(distance, popt[1], c=cmap2(k))
    #plt.savefig('plots/wake_expansion.png')


plt.figure(1)
plt.savefig('plots/farm_area.png')