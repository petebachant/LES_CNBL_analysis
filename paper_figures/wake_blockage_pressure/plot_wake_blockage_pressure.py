import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import h5py

#path variable to change
path = '/mnt/e/LES_data/'

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
cm = 1/2.54
fig, ax = plt.subplots(nrows=2, figsize=[12*cm,12*cm/(golden_ratio)], dpi=300, layout='constrained')

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
ax[0].set_title(r'(a) H300-C2-G1', loc='left')
ax[0].text(1,1.45, r'$\eta_w=0.501$'+'\n'+r'$\eta_{nl}=0.857$', ha='left', va='top')
#ax[0].text(1,1, r'$\eta_{nl}=P_1/P_{\infty}=0.857$', ha='left', va='center')
ax[0].set_ylabel(r'$z$ [km]')
ax[0].set_box_aspect(1/(2*golden_ratio))
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
ax[1].set_title(r'(b) H300-C8-G1', loc='left')
ax[1].text(1,1.45, r'$\eta_w=1.00$'+'\n'+r'$\eta_{nl}=0.437$', ma='left', ha='left', va='top')
#ax[1].text(1,1, r'$\eta_{nl}=P_1/P_{\infty}=0.437$', ha='left', va='center')
ax[1].set_ylabel(r'$z$ [km]')
ax[1].set_xlabel(r'$x$ [km]')
ax[1].set_box_aspect(1/(2*golden_ratio))
#plot turbine locations
for i in range(16):
    ax[1].plot([18+i*5*0.198, 18+i*5*0.198], [21/1000, 217/1000], c='k')

#plt.tight_layout()

cbar = fig.colorbar(pcm, ax=ax)
cbar.set_label(r'$(\langle \overline p \rangle_f - \langle \overline p_{in} \rangle_f)/\rho_0$ [m$^2$s$^{-2}$]')

plt.savefig('KirbyFig2.png', bbox_inches='tight')
plt.savefig('fig2.pdf', bbox_inches='tight')