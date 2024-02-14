import matplotlib.pyplot as plt
import numpy as np
import h5py
import matplotlib as mpl
import scipy.interpolate as sp
from scipy import stats
from scipy.optimize import curve_fit

#path variable to change
path = '/mnt/e/LES_data/'

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=2, nrows=2, figsize=[textwidth,textwidth/(golden_ratio)], dpi=300)

#vertical grid - use cell centered points  
with open(f'{path}zmesh','r') as file:       
    Nz_full     = int(float(file.readline()))   
    N_line = Nz_full+1
    line = N_line*[0]
    cnt = 0
    for lines in file:
        line[cnt]=lines.split()
        cnt+=1       
    z = np.array([float(line[k][0]) for k in range(int(Nz_full))])[1::2]

#load precursor data
f = h5py.File(f'{path}H300-C2-G1/stat_precursor_first_order.h5', 'r')
u_precursor = f['u']
u_prec_profile = np.mean(u_precursor[:,:,:100],axis=(0,1))
interp_u_prec = sp.interp1d(1000*z[:100], u_prec_profile)
#hub height precursor u velocity
u_prec_hubh = interp_u_prec(119)

#open LES data for H300-C2-G1
f = h5py.File(f'{path}H300-C2-G1/stat_main_first_order.h5', 'r')

#open velocity data
u = f['u']
v = f['v']
#load auxiliary data
aux = h5py.File(f'{path}H300-C2-G1/aux_files.h5', 'r')
yaw = aux['yaw']
time = aux['time']
yaw = np.mean(yaw[time[:]>75600,:],axis=0)

#define x, y coordinates
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)

ax[0,0].pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u[450:1150,340:1050,23].T,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
ax[0,0].set_xlim([15,35])
ax[0,0].set_ylim([7.5,22.5])
ax[0,0].set_aspect('equal')
ax[0,0].set_ylabel(r'$y$ (km)')
ax[0,0].set_title(r'(A) H300-C2-G1 $\eta_w=50\%$', loc='left')

ax[0,0].plot([27.702, 28.692, 28.692, 27.702, 27.702], [10.05, 10.05, 19.95, 19.95, 10.05], c='r')
ax[0,1].set_title(r'(B) H300-C2-G1 $\eta_w=50\%$', loc='left')

#create interpolating function for gridded data
print('Begin interpolation')
interp_u = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), u[544:1120,400:1050,:100])
interp_v = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), v[544:1120,400:1050,:100])
print('Interpolation finished')

#x position of turbine no.0
x_pos_turb = 18e3
#y position of turbine no.0
y_pos_turb = 10.2975e3

#function to fit to wake deficits
def fit_func(z,a,b,c):
    return a*stats.norm.pdf(z,c,b*198)

#arrays to store results
wake_distance = np.linspace(2,9,8)
wake_span = np.linspace(-2*198, 2*198, 80)
wake_yslice = np.zeros((10,8,80))

cmap1 = plt.get_cmap('viridis', 8)
#turbine row number
k = 10

#loop over x positions
for i, distance in enumerate(wake_distance):

    #loop over turbine column
    for j in range(10):

        #loop across spanwise position
        for y_index in range(80):

            x_pos = x_pos_turb + distance*198*np.cos(np.pi*yaw[j+k*10]/180) + 5*198*k - \
                wake_span[y_index]*np.sin(np.pi*yaw[j+k*10]/180)
            #staggered alternate rows
            if k%2 == 0:
                y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j+k*10]/180) + 5*198*j + \
                wake_span[y_index]*np.cos(np.pi*yaw[j+k*10]/180)
            else:
                y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j+k*10]/180) + 5*198*j + 2.5*198 +\
                wake_span[y_index]*np.cos(np.pi*yaw[j+k*10]/180)

            pos = np.array([x_pos, y_pos, 119])
            u_min = interp_u(pos)
            v_min = interp_v(pos)

            wake_yslice[j, i, y_index] = u_min*np.cos(np.pi*yaw[j+k*10]/180) + v_min*np.sin(np.pi*yaw[j+k*10]/180)

    mean_wake_profile = np.mean(wake_yslice,axis=0)
    ax[0,1].plot((u_prec_hubh-mean_wake_profile[i,:])/u_prec_hubh, wake_span/198, c=cmap1(i))

ax[0,1].set_xlim([0,0.8])
ax[0,1].set_ylim([-1,1])
ax[0,1].set_ylabel(r'$y/D$')

#load precursor data
f = h5py.File(f'{path}H300-C8-G1/stat_precursor_first_order.h5', 'r')
u_precursor = f['u']
u_prec_profile = np.mean(u_precursor[:,:,:100],axis=(0,1))
interp_u_prec = sp.interp1d(1000*z[:100], u_prec_profile)
#hub height precursor u velocity
u_prec_hubh = interp_u_prec(119)

#open LES data for H300-C2-G1
f = h5py.File(f'{path}H300-C8-G1/stat_main_first_order.h5', 'r')

#open velocity data
u = f['u']
v = f['v']
#load auxiliary data
aux = h5py.File(f'{path}H300-C8-G1/aux_files.h5', 'r')
yaw = aux['yaw']
time = aux['time']
yaw = np.mean(yaw[time[:]>75600,:],axis=0)

pcm = ax[1,0].pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u[450:1150,340:1050,23].T,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
ax[1,0].set_xlim([15,35])
ax[1,0].set_ylim([7.5,22.5])
ax[1,0].set_ylabel(r'$y$ (km)')
ax[1,0].set_xlabel(r'$x$ (km)')
ax[1,0].set_aspect('equal')
ax[1,0].set_title(r'(C) H300-C8-G1 $\eta_w=100\%$', loc='left')

ax[1,0].plot([27.702, 28.692, 28.692, 27.702, 27.702], [10.05, 10.05, 19.95, 19.95, 10.05], c='r')
ax[1,1].set_title(r'(D) H300-C8-G1 $\eta_w=100\%$', loc='left')

#create interpolating function for gridded data
print('Begin interpolation')
interp_u = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), u[544:1120,400:1050,:100])
interp_v = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), v[544:1120,400:1050,:100])
print('Interpolation finished')

#arrays to store results
wake_distance = np.linspace(2,9,8)
wake_span = np.linspace(-2*198, 2*198, 80)
wake_yslice = np.zeros((10,8,80))

cmap1 = plt.get_cmap('viridis', 8)
#turbine row number
k = 10

#loop over x positions
for i, distance in enumerate(wake_distance):

    #loop over turbine column
    for j in range(10):

        #loop across spanwise position
        for y_index in range(80):

            x_pos = x_pos_turb + distance*198*np.cos(np.pi*yaw[j+k*10]/180) + 5*198*k - \
                wake_span[y_index]*np.sin(np.pi*yaw[j+k*10]/180)
            #staggered alternate rows
            if k%2 == 0:
                y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j+k*10]/180) + 5*198*j + \
                wake_span[y_index]*np.cos(np.pi*yaw[j+k*10]/180)
            else:
                y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j+k*10]/180) + 5*198*j + 2.5*198 +\
                wake_span[y_index]*np.cos(np.pi*yaw[j+k*10]/180)

            pos = np.array([x_pos, y_pos, 119])
            u_min = interp_u(pos)
            v_min = interp_v(pos)

            wake_yslice[j, i, y_index] = u_min*np.cos(np.pi*yaw[j+k*10]/180) + v_min*np.sin(np.pi*yaw[j+k*10]/180)

    mean_wake_profile = np.mean(wake_yslice,axis=0)
    plot = ax[1,1].plot((u_prec_hubh-mean_wake_profile[i,:])/u_prec_hubh, wake_span/198, c=cmap1(i))

ax[1,1].set_xlim([0,0.8])
ax[1,1].set_ylim([-1,1])
ax[1,1].set_xlabel(r'$\frac{u_{\infty}-U}{u_{\infty,hubh}}$')
ax[1,1].set_ylabel(r'$y/D$')

plt.subplots_adjust(wspace=0.4, hspace=0.3)

cbar = fig.colorbar(pcm, ax=ax[:,0])
cbar.set_label(r'$u$ (ms$^{-1}$)')

sm = plt.cm.ScalarMappable(cmap=cmap1, norm=plt.Normalize(vmin=2, vmax=9))
cbar2 = fig.colorbar(sm, ax=ax[:,1], ticks=np.linspace(2.5,8.5,8))
cbar2.set_ticklabels(np.linspace(2,9,8))
cbar2.set_label(r'$x/D$')

plt.savefig('KirbyFig6.png', bbox_inches='tight')
plt.savefig('fig6.pdf', bbox_inches='tight')
