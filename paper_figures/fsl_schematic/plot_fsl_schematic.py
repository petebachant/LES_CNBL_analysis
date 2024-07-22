import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import matplotlib as mpl
import h5py

#path variable to change!
path = '/mnt/c/Users/trin3517/Documents/PhD/Year 4/Research plots and presentations/LES_data/'

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
cm = 1/2.54
fig, ax = plt.subplots(figsize=[12*cm,12*cm/(golden_ratio)], dpi=300)

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#turbine-scale loss factors
tsl = np.zeros(44)
#farm-scale loss factors
fsl = np.zeros(44)
#total loss i.e. P_farm/P_Betz
total_loss = np.zeros(44)

for i in range(44):
    tsl[i] = loss_factors[i][3]
    fsl[i] = loss_factors[i][4]
    total_loss[i] = (1-tsl[i])*(1-fsl[i])

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
plt.scatter(17.85, total_loss[15], marker='x', c='r', zorder=1)
plt.scatter(17.85, total_loss[41], marker='x', c='r', zorder=1)
plt.scatter(4.46, total_loss[43], marker='x', c='r', zorder=1)


left, bottom, width, height = [0.675, 0.5, 0.2, 0.2]
ax2 = fig.add_axes([left, bottom, width, height])
#f = h5py.File(f'{path}H500-C5-G4/stat_main_first_order.h5', 'r')
#u = f['u']
u = np.load('H500-C5-G4.npy')
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)
ax2.set_xlim([25,30])
ax2.set_ylim([12.5,17.5])
ax2.pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
#np.save('H500-C5-G4.npy', u[450:1150,340:1050,23].T)
ax2.set_aspect('equal')
ax2.set_yticks([])
ax2.set_xticks([])

left, bottom, width, height = [0.675, 0.14, 0.2, 0.2]
ax3 = fig.add_axes([left, bottom, width, height])
#f = h5py.File(f'{path}H500-C5-G4_aligned/stat_main_first_order.h5', 'r')
#u = f['u']
u = np.load('H500-C5-G4_aligned.npy')
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)
ax3.set_xlim([25,30])
ax3.set_ylim([12.5,17.5])
ax3.pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
#np.save('H500-C5-G4_aligned.npy', u[450:1150,340:1050,23].T)
ax3.set_aspect('equal')
ax3.set_yticks([])
ax3.set_xticks([])

left, bottom, width, height = [0.2, 0.2, 0.2, 0.2]
ax4 = fig.add_axes([left, bottom, width, height])
#f = h5py.File(f'{path}H500-C5-G4_double_spacing/stat_main_first_order.h5', 'r')
#u = f['u']
u = np.load('H500-C5-G4_double_spacing.npy')
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)
ax4.set_xlim([25,30])
ax4.set_ylim([12.5,17.5])
ax4.pcolormesh(x[450:1150]/1000, y[340:1050]/1000, u,
                    shading='nearest', vmin=2, vmax=10, rasterized=True)
#np.save('H500-C5-G4_double_spacing.npy', u[450:1150,340:1050,23].T)
ax4.set_aspect('equal')
ax4.set_yticks([])
ax4.set_xticks([])

ax.annotate("", xy=(18.1, 0.46), xytext=(19.9, 0.7), arrowprops=dict(arrowstyle="->", color='r'))
ax.annotate("", xy=(18.1, 0.325), xytext=(19.9, 0.2), arrowprops=dict(arrowstyle="->", color='r'))
ax.annotate("", xy=(4.5, 0.7), xytext=(6.5, 0.425), arrowprops=dict(arrowstyle="->", color='r'))
ax.text(12.5, 1, r"Isolated turbines", ha='center', va='bottom')
tab10 = mpl.colormaps['tab10']
ax.annotate("", xy=(17.5, 0.3175), xytext=(17.5, 0.44), arrowprops=dict(arrowstyle="->"), color=tab10(1), zorder=0)
ax.annotate("", xy=(17.5, 0.42), xytext=(17.5, 1), arrowprops=dict(arrowstyle="->"), color=tab10(2), zorder=0)

ax.text(11.75, 0.8, r'Farm-scale'+'\n'+r'losses'+'\n'+r'$FSL$',
         ha='left', va='top', ma='left')
ax.text(11.75, 0.42, r'Turbine-scale'+'\n'+r'losses'+'\n'+r'$TSL$', 
        ha='left', va='top', ma='left')
ax.text(4, 0.85, r"$C_{p,Nishino}/C_{p,Betz}$" + '\n' +r"($\zeta=38.1$)", ha='left', va='center', ma='left', c=tab10(0))

#plt.tight_layout()
ax.set_ylim([0, 1.1])
ax.set_xlabel(r'$\lambda/C_{f0}$ [-]')
ax.set_ylabel(r'$C_p/C_{p,Betz}$ [-]')
plt.savefig('KirbyFig11.png', bbox_inches='tight')
plt.savefig('fig11.pdf', bbox_inches='tight')
