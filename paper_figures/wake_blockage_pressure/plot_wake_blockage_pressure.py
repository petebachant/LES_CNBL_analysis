import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import h5py

#path variable to change
path = '/mnt/e/LES_data/'

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(nrows=2, figsize=[textwidth,textwidth/(golden_ratio)], dpi=300)

#open LES data for H300-C2-G1
f = h5py.File(f'{path}H300-C2-G1/stat_main_first_order.h5', 'r')
#open pressure data
pressure = f['p']

#define x, y, z coordinates
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)
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

#extract pressure across the farm width
x_index_mask = [x[i]<40e3 for i in range(1600)]
y_index_mask = [y[i]>15e3-4.95e3 and y[i]<15e3+4.95e3 for i in range(1380)]
pressure_farm = pressure[:,y_index_mask,:300]
pressure_farm = pressure_farm[x_index_mask,:,:]

#average pressure in y direction across the farm width
pressure_farm_average = np.mean(pressure_farm, axis=1)
pressure_perturbation = pressure_farm_average-pressure_farm_average[0,:]
ax[0].pcolormesh(x[x_index_mask]/1000, z[:300], pressure_perturbation.T, shading='nearest',
                    cmap=mpl.colormaps['RdBu'], vmin=-15, vmax=15, rasterized=True)
ax[0].set_title(r'(A) H300-C2-G1', loc='left')
ax[0].text(1,1.25, r'$\eta_w=P_{farm}/P_1=50\%$', ha='left', va='center')
ax[0].text(1,1, r'$\eta_{nl}=P_1/P_{\infty}=86\%$', ha='left', va='center')
ax[0].set_ylabel(r'$z$ (km)')
#plot turbine locations
for i in range(16):
    ax[0].plot([18+i*5*0.198, 18+i*5*0.198], [21/1000, 217/1000], c='k')

#open LES data for H300-C2-G1
f = h5py.File(f'{path}H300-C8-G1/stat_main_first_order.h5', 'r')
#open pressure data
pressure = f['p']

#extract pressure across the farm width
pressure_farm = pressure[:,y_index_mask,:300]
pressure_farm = pressure_farm[x_index_mask,:,:]

#average pressure in y direction across the farm width
pressure_farm_average = np.mean(pressure_farm, axis=1)
pressure_perturbation = pressure_farm_average-pressure_farm_average[0,:]
pcm = ax[1].pcolormesh(x[x_index_mask]/1000, z[:300], pressure_perturbation.T, shading='nearest',
                    cmap=mpl.colormaps['RdBu'], vmin=-20, vmax=20, rasterized=True)
ax[1].set_title(r'(B) H300-C8-G1', loc='left')
ax[1].text(1,1.25, r'$\eta_w=P_{farm}/P_1=100\%$', ha='left', va='center')
ax[1].text(1,1, r'$\eta_{nl}=P_1/P_{\infty}=44\%$', ha='left', va='center')
ax[1].set_ylabel(r'$z$ (km)')
ax[1].set_xlabel(r'$x$ (km)')
#plot turbine locations
for i in range(16):
    ax[1].plot([18+i*5*0.198, 18+i*5*0.198], [21/1000, 217/1000], c='k')

plt.tight_layout()

cbar = fig.colorbar(pcm, ax=ax)
cbar.set_label(r'$(\langle \overline p \rangle_f - \langle \overline p_{in} \rangle_f)/\rho_0$ (m$^2$s$^{-2}$)')

plt.savefig('KirbyFig2.png', bbox_inches='tight')
plt.savefig('fig2.pdf', bbox_inches='tight')