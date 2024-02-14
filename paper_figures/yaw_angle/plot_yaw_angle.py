import matplotlib.pyplot as plt
import numpy as np
import h5py
import matplotlib as mpl

#path variable to change
path = '/mnt/e/LES_data/'

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=2, figsize=[textwidth,textwidth/(2*golden_ratio)], dpi=300)

#open LES data for H300-C2-G1
f = h5py.File(f'{path}H300-C2-G1/stat_main_first_order.h5', 'r')

#open velocity data
u = f['u']
v = f['v']

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

#define x, y coordinates
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)

#plot up to 40km in x direction
x_index_mask = [x[i]<40e3 for i in range(1600)]

#calculate wind direction
wind_angle = np.arctan(v[x_index_mask,:,23]/u[x_index_mask,:,23])
#convert to degrees
wind_angle_deg = 180*wind_angle/np.pi

ax[0].pcolormesh(x[x_index_mask]/1000, y/1000, wind_angle_deg.T, shading='nearest', 
                    cmap=mpl.colormaps['RdBu'], vmin=-10, vmax=10, rasterized=True)

ax[0].set_ylabel(r'$y$ (km)')
ax[0].set_xlabel(r'$x$ (km)')
ax[0].set_title(r'(A) H300-C2-G1', loc='left')
ax[0].text(1,25, r'$\eta_w=P_{farm}/P_1=50\%$', ha='left', va='center')

#open LES data for H300-C2-G1
f = h5py.File(f'{path}H300-C8-G1/stat_main_first_order.h5', 'r')

#open velocity data
u = f['u']
v = f['v']

#calculate wind direction
wind_angle = np.arctan(v[x_index_mask,:,23]/u[x_index_mask,:,23])
#convert to degrees
wind_angle_deg = 180*wind_angle/np.pi

pcm = ax[1].pcolormesh(x[x_index_mask]/1000, y/1000, wind_angle_deg.T, shading='nearest', 
                    cmap=mpl.colormaps['RdBu'], vmin=-10, vmax=10, rasterized=True)
ax[1].set_xlabel(r'$x$ (km)')
ax[1].set_title(r'(B) H300-C8-G1', loc='left')
ax[1].text(1,25, r'$\eta_w=P_{farm}/P_1=100\%$', ha='left', va='center')

plt.tight_layout()

cbar = fig.colorbar(pcm, ax=ax)
cbar.set_label(r'$\gamma$ (deg.)')

plt.savefig('KirbyFig4.png', bbox_inches='tight')
plt.savefig('fig4.pdf', bbox_inches='tight')
