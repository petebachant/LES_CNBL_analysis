import matplotlib.pyplot as plt
import numpy as np
import h5py
import matplotlib as mpl

#path variable to change
path = '/mnt/c/Users/trin3517/Documents/PhD/Year 4/Research plots and presentations/LES_data/'


plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803

fig, ax = plt.subplots(ncols=3, figsize=[textwidth,textwidth/(3*golden_ratio)],
        dpi=300)

#define x, y coordinates
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)

#open LES data for H500-C5-G4
f = h5py.File(f'{path}H500-C5-G4/stat_main_first_order.h5', 'r')

#open velocity data
u = f['u']

ax[0].pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u[450:1150,340:1050,23].T,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
ax[0].set_xlim([15,35])
ax[0].set_ylim([7.5,22.5])
ax[0].set_aspect('equal')
ax[0].set_ylabel(r'$y$ (km)')
ax[0].set_xlabel(r'$x$ (km)')
ax[0].set_title(r'(A) Standard', loc='left')

#open LES data for H500-C5-G4_double_spacing
f = h5py.File(f'{path}H500-C5-G4_double_spacing/stat_main_first_order.h5', 'r')

#open velocity data
u = f['u']

pcm = ax[2].pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u[450:1150,340:1050,23].T,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
ax[2].set_xlim([15,35])
ax[2].set_ylim([7.5,22.5])
ax[2].set_aspect('equal')
ax[2].set_xlabel(r'$x$ (km)')
ax[2].set_title(r'(C) Double spacing', loc='left')

#open LES data for H500-C5-G4_half_farm
f = h5py.File(f'{path}H500-C5-G4_half_farm/stat_main_first_order.h5', 'r')

#open velocity data
u = f['u']

ax[1].pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u[450:1150,340:1050,23].T,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
ax[1].set_xlim([15,35])
ax[1].set_ylim([7.5,22.5])
ax[1].set_aspect('equal')
ax[1].set_xlabel(r'$x$ (km)')
ax[1].set_title(r'(B) Half length', loc='left')

cbar = fig.colorbar(pcm, ax=ax)
cbar.set_label(r'$u$ (ms$^{-1}$)')

#plt.tight_layout()

plt.savefig('KirbyFig16.png', bbox_inches='tight')
plt.savefig('fig16.pdf', bbox_inches='tight')
