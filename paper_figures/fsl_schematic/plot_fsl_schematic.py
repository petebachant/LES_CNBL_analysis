import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import matplotlib as mpl

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(figsize=[textwidth,textwidth/(golden_ratio)], dpi=300)

cp_nishino = np.zeros(50)
effective_array_density = np.linspace(5,20,50)

ctstar = 0.88
zeta = 25

for i in range(50):

    def ndfm(beta):
        lhs = ctstar*effective_array_density[i]*beta**2 + beta**2

        rhs = 1 + zeta*(1-beta)

        return lhs - rhs

    beta = opt.bisect(ndfm,1,0.3)
    cp_nishino[i] = 0.592*beta**3

plt.plot([5, 20], [0.592, 0.592], c='k')
plt.plot(effective_array_density, cp_nishino, zorder=0)
plt.scatter([9.97, 11.76], [0.225, 0.27], marker='x', c='r', zorder=1)


left, bottom, width, height = [0.475, 0.15, 0.2, 0.2]
ax2 = fig.add_axes([left, bottom, width, height])
u_wind_hubh50 = np.load('u_wind_hubh50.npy')
n_x, n_y = np.shape(u_wind_hubh50)
x = 24.5*np.arange(0, n_x)/100
y = 24.5*np.arange(0, n_y)/100
x, y = np.meshgrid(x, y)
pcm = ax2.pcolormesh(x, y, np.transpose(u_wind_hubh50)/10.10348311, vmin=0.1, vmax=0.4, rasterized=True)
ax2.set_aspect('equal')
ax2.set_yticks([])
ax2.set_xticks([])

left, bottom, width, height = [0.585, 0.575, 0.2, 0.2]
ax3 = fig.add_axes([left, bottom, width, height])
u_wind_hubh6 = np.load('u_wind_hubh6.npy')
n_x, n_y = np.shape(u_wind_hubh6)
x = 24.5*np.arange(0, n_x)/100
y = 24.5*np.arange(0, n_y)/100
x, y = np.meshgrid(x, y)
pcm = ax3.pcolormesh(x, y, np.transpose(u_wind_hubh6)/10.10348311, vmin=0.1, vmax=0.4, rasterized=True)
ax3.set_aspect('equal')
ax3.set_yticks([])
ax3.set_xticks([])

ax.annotate("", xy=(11.9, 0.28), xytext=(14.5, 0.475), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(10.2, 0.215), xytext=(12.4, 0.1), arrowprops=dict(arrowstyle="->"))
ax.text(12, 0.6, r"Isolated turbine $C_{p,Betz}$ ($C_T'=1.9417$)", ha='center', va='bottom')
tab10 = mpl.colormaps['tab10']
ax.annotate("", xy=(9.97, 0.23), xytext=(9.97, 0.3), arrowprops=dict(arrowstyle="<->"), color=tab10(1))
ax.annotate("", xy=(9.97, 0.3), xytext=(9.97, 0.592), arrowprops=dict(arrowstyle="<->"), color=tab10(2))

ax.text(6.2, 0.475, r'Farm-scale'+'\n'+r'losses'+'\n'+r'$\Pi_F=1-\frac{C_{p,Nishino}}{C_{p,Betz}}$',
         ha='left', va='center', ma='left')
ax.text(6.2, 0.26, r'Turbine-scale'+'\n'+r'losses' +'\n'+r'$\Pi_T=1-\frac{C_{p}}{C_{p,Nishino}}$', 
        ha='left', va='center', ma='left')
ax.text(16, 0.24, r"$C_{p,Nishino}$ ($\zeta=25$, $\gamma=2.0$,"+'\n'+r"$C_T'=1.9417$)", ha='left', va='center', ma='right', c=tab10(0))

#plt.tight_layout()
ax.set_ylim([0, 0.65])
ax.set_xlabel(r'$\lambda/C_{f0}$')
ax.set_ylabel(r'$C_p$', rotation=0)
plt.savefig('KirbyFig10.png', bbox_inches='tight')
plt.savefig('fig10.pdf', bbox_inches='tight')
