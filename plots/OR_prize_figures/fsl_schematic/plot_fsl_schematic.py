import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import matplotlib as mpl
import h5py

#path variable to change!
path = '/mnt/c/Users/trin3517/Documents/PhD/Year 4/Research plots and presentations/LES_data/'

plt.style.use("../style.mplstyle")

tab10 = mpl.colormaps['tab10']

cm = 1/2.54
textwidth = 15
golden_ratio = 1.61803
fig, ax = plt.subplots(figsize=[textwidth*cm,textwidth*cm/(1.5*golden_ratio)], dpi=300)

cp_ratio = np.zeros(50)
effective_array_density = np.linspace(2,25,50)

#power coefficient should be overpredicted due to
#the effect of the Gaussian filter length
#here we calculate the overpredicted power coefficient 
#of an actuator disc with ct_prime = 1.9417 according to
#Shapiro et. al. 2019

#calculate shapiro correction factor
#Gaussian filter length is yz direction is 32.61m
ct_prime = 1.9417
delta_r = 32.61
turbine_radius = 99
#using equation 26 of Shapiro et. al. 2019
M_shapiro = delta_r/turbine_radius
M_shapiro = M_shapiro / np.sqrt(3*np.pi)
M_shapiro = M_shapiro * ct_prime / 4
M_shapiro = M_shapiro + 1
M_shapiro = M_shapiro**(-1)

ctstar = 0.88/M_shapiro**2
zeta = 38.1

for i in range(50):

    def ndfm(beta):
        lhs = ctstar*effective_array_density[i]*beta**2 + beta**2

        rhs = 1 + zeta*(1-beta)

        return lhs - rhs

    beta = opt.bisect(ndfm,1,0.3)
    cp_ratio[i] = beta**3

plt.plot([2, 25], [1, 1], c='k')
plt.plot(effective_array_density, cp_ratio, zorder=0)
plt.scatter(10, 0.575, marker='x', c='r', zorder=1)
plt.scatter(10, 0.46, marker='x', c='r', zorder=1)
ax.annotate("", xy=(10, 0.575), xytext=(10,1), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(10, 0.46), xytext=(10,0.575), arrowprops=dict(arrowstyle="->"))
ax.text(12.5, 1, r"Isolated turbine", ha='center', va='bottom')
ax.annotate("", xy=(10.3, 0.58), xytext=(14.5, 0.7), arrowprops=dict(arrowstyle="->", color='r'))
ax.annotate("", xy=(10.3, 0.44), xytext=(14.5, 0.2), arrowprops=dict(arrowstyle="->", color='r'))

ax.text(9.75, 0.85, r'Farm-scale'+'\n'+r'efficiency $\eta_{FS}$',
         ha='right', va='center', ma='left')
ax.text(9.75, 0.56, r'Turbine-scale'+'\n'+r'efficiency $\eta_{TS}$',
         ha='right', va='top', ma='left')
ax.text(20, 0.4, r'$P_{Nishino}$', ha='left', va='bottom', ma='left', c=tab10(0))
ax.text(16.4, 0.85, r'Optimal', ha='center', va='bottom')

left, bottom, width, height = [0.5, 0.5, 0.2, 0.2]
ax2 = fig.add_axes([left, bottom, width, height])
f = h5py.File(f'{path}H500-C5-G4/stat_main_first_order.h5', 'r')
u = f['u']
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)
ax2.set_xlim([25.5,28.5])
ax2.set_ylim([13,16])
ax2.pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u[450:1150,340:1050,23].T,
                    shading='nearest', vmin=2, vmax=8.5, rasterized=True)
ax2.set_aspect('equal')
ax2.set_yticks([])
ax2.set_xticks([])

#x position of turbine no.0
x_pos_turb = 18e3
#y position of turbine no.0
y_pos_turb = 10.2975e3

#add white lines to denote turbine position
for i in range(10):

    for j in range(16):

        x = x_pos_turb + j*198*5
        if j%2 == 0:
            y = y_pos_turb + i*198*5
        else:
            y = y_pos_turb + i*198*5 + 198*2.5
        ax2.plot([x/1000, x/1000], [(y-99)/1000, (y+99)/1000], c='w')

left, bottom, width, height = [0.5, 0.14, 0.2, 0.2]
ax3 = fig.add_axes([left, bottom, width, height])
f = h5py.File(f'{path}H500-C5-G4_aligned/stat_main_first_order.h5', 'r')
u = f['u']
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)
ax3.set_xlim([25.5,28.5])
ax3.set_ylim([13,16])
ax3.pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u[450:1150,340:1050,23].T,
                    shading='nearest', vmin=2, vmax=8.5, rasterized=True)
ax3.set_aspect('equal')
ax3.set_yticks([])
ax3.set_xticks([])

#x position of turbine no.0
x_pos_turb = 18e3
#y position of turbine no.0
y_pos_turb = 10.545e3

#add white lines to denote turbine position
for i in range(10):

    for j in range(16):

        x = x_pos_turb + j*198*5
        y = y_pos_turb + i*198*5
        ax3.plot([x/1000, x/1000], [(y-99)/1000, (y+99)/1000], c='w')

ax.set_ylim([0, 1.1])
ax.set_ylabel(r'Farm efficiency $P/P_{\infty}$')
ax.set_xlabel(r'Effective farm density $\lambda/C_{f0}$')

plt.savefig('KirbyFig1.png', bbox_inches='tight')
plt.savefig('fig1.pdf', bbox_inches='tight')
