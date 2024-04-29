import matplotlib.pyplot as plt
import numpy as np
import h5py
import matplotlib as mpl

#path variable to change
path = '/mnt/e/LES_data/'

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
cm = 1/2.54
fig, ax = plt.subplots(ncols=2, nrows=2, figsize=[12*cm,12*cm/(golden_ratio)], dpi=300, layout='constrained')

#open LES data for H300-C2-G1
f = h5py.File(f'{path}H300-C2-G1/stat_main_first_order.h5', 'r')

#open velocity data
u = f['u']
v = f['v']

#define x, y coordinates
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)

ax[0,0].pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u[450:1150,340:1050,23].T,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
ax[0,0].set_xlim([15,35])
ax[0,0].set_ylim([7.5,22.5])
ax[0,0].set_aspect('equal')
ax[0,0].set_ylabel(r'$y$ [km]')
ax[0,0].set_title(r'(a) H300-C2-G1 $\eta_w=0.501$', loc='left')

ax[0,1].pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u[450:1150,340:1050,23].T,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
ax[0,1].set_xlim([27.405,29.385])
ax[0,1].set_ylim([14.505,15.99])
ax[0,0].plot([27.405, 29.385, 29.385, 27.405, 27.405], [14.505, 14.505, 15.99, 15.99, 14.505], c='r')
ax[0,1].plot([27.405, 29.385, 29.385, 27.405, 27.405], [14.505, 14.505, 15.99, 15.99, 14.505], c='r', linewidth=3.0)
ax[0,1].set_aspect('equal')
ax[0,1].set_title(r'(b) H300-C2-G1 $\eta_w=0.501$', loc='left')

#open LES data for H300-C8-G1
f = h5py.File(f'{path}H300-C8-G1/stat_main_first_order.h5', 'r')

#open velocity data
u = f['u']
v = f['v']

#define x, y coordinates
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)

ax[1,0].pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u[450:1150,340:1050,23].T,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
ax[1,0].set_xlim([15,35])
ax[1,0].set_ylim([7.5,22.5])
ax[1,0].set_ylabel(r'$y$ [km]')
ax[1,0].set_xlabel(r'$x$ [km]')
ax[1,0].set_aspect('equal')
ax[1,0].set_title(r'(c) H300-C8-G1 $\eta_w=1.00$', loc='left')

pcm = ax[1,1].pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u[450:1150,340:1050,23].T,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
ax[1,1].set_xlim([27.405,29.385])
ax[1,1].set_ylim([14.505,15.99])
ax[1,0].plot([27.405, 29.385, 29.385, 27.405, 27.405], [14.505, 14.505, 15.99, 15.99, 14.505], c='r')
ax[1,1].plot([27.405, 29.385, 29.385, 27.405, 27.405], [14.505, 14.505, 15.99, 15.99, 14.505], c='r', linewidth=3.0)
ax[1,1].set_xlabel(r'$x$ [km]')
ax[1,1].set_aspect('equal')
ax[1,1].set_title(r'(d) H300-C8-G1 $\eta_w=1.00$', loc='left')

cbar = fig.colorbar(pcm, ax=ax, pad=0.125)
cbar.set_label(r'$u$ [m s$^{-1}$]')

plt.savefig('KirbyFig5.png', bbox_inches='tight')
plt.savefig('fig5.pdf', bbox_inches='tight')
