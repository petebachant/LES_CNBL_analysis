import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sp

plt.style.use("../style.mplstyle")

cm = 1/2.54
textwidth = 15
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=2, nrows=1, figsize=[textwidth*cm,textwidth*cm/(1.4*golden_ratio)], dpi=300, layout='constrained')

u_wind_hubh50 = np.load('u_wind_hubh50.npy')
n_x, n_y = np.shape(u_wind_hubh50)
x = 24.5*np.arange(0, n_x)/100
y = 24.5*np.arange(0, n_y)/100
x, y = np.meshgrid(x, y)
pcm = ax[0].pcolormesh(x, y, np.transpose(u_wind_hubh50)/10.10348311, vmin=0.1, vmax=0.4, rasterized=True)
ax[0].set_ylabel(r'$y/D$')
ax[0].set_xlabel(r'$x/D$')
ax[0].set_title('a)', loc='left')

u_wind_hubh2 = np.load('u_wind_hubh2.npy')
n_x, n_y = np.shape(u_wind_hubh2)
x = 24.5*np.arange(0, n_x)/100
y = 24.5*np.arange(0, n_y)/100
x, y = np.meshgrid(x, y)
pcm = ax[1].pcolormesh(x, y, np.transpose(u_wind_hubh2)/10.10348311, vmin=0.1, vmax=0.4, rasterized=True)
ax[1].set_xlabel(r'$x/D$')
ax[1].set_title('b)', loc='left')

ax[0].set_aspect('equal')

ax[1].set_aspect('equal')

cbar = fig.colorbar(pcm, ax=ax.ravel().tolist(), shrink=0.95)
cbar.solids.set_rasterized(True)
cbar.set_label(r'$\overline{U}/U_{F0}$')

plt.savefig('KirbyFig3.png', bbox_inches='tight')
plt.savefig('fig3.pdf', bbox_inches='tight')
