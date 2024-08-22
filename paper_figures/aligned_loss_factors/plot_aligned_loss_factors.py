import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
cm = 1/2.54
fig, ax = plt.subplots(figsize=[12*cm,12*cm/(2.5*golden_ratio)], dpi=300)

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#array to store wake efficiencies
eta_w = np.zeros(44)
#array to store non-local efficiencies
eta_nl = np.zeros(44)
#array to store farm efficiencies
eta_f = np.zeros(44)
#turbine-scale loss factors
tsl = np.zeros(44)
#farm-scale loss factors
fsl = np.zeros(44)
#total loss i.e. P_farm/P_Betz
total_loss = np.zeros(44)

for i in range(44):
    eta_w[i] = loss_factors[i][1]
    eta_nl[i] = loss_factors[i][2]
    eta_f[i] = eta_w[i]*eta_nl[i]
    tsl[i] = loss_factors[i][3]
    fsl[i] = loss_factors[i][4]
    total_loss[i] = (1-tsl[i])*(1-fsl[i])

index_mask = [5, 40, 15, 41, 25, 42]

tab20 = mpl.colormaps['tab20']

ax.bar(np.arange(6), 1-tsl[index_mask], width=0.2, label=r'$\eta_{TS}$', color=tab20(0))
ax.bar(np.arange(6)-0.2, total_loss[index_mask], width=0.2, label=r'$C_p/C_{p,Betz}$', color='k')
ax.bar(np.arange(6)+0.2, 1-fsl[index_mask], width=0.2, label=r'$\eta_{FS}$', color=tab20(2))
ax.set_ylim([0,1.6])
ax.axvline(1.5, c='grey')
ax.axvline(3.5, c='grey')
ax.set_xticks(np.arange(6), [r'S', r'A', r'S', r'A', r'S', r'A'], rotation=0)
ax.text(0.5, 1.55, r'H1000-'+'\n'+r'C5-G4', ha='center', va='top', ma='center')
ax.text(2.5, 1.55, r'H500-'+'\n'+r'C5-G4', ha='center', va='top', ma='center')
ax.text(4.5, 1.55, r'H300-'+'\n'+r'C5-G4', ha='center', va='top', ma='center')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)
#ax.plot([-0.5, 1.5], [0.450, 0.450], c='grey', linestyle='--', zorder=0)
#ax.plot([1.5, 3.5], [0.427, 0.427], c='grey', linestyle='--', zorder=0)
#ax.plot([3.5, 5.5], [0.369, 0.369], c='grey', linestyle='--', zorder=0)
ax.set_xlim([-0.5,5.5])
ax.set_box_aspect(1/golden_ratio)
ax.grid(which='major', axis='y', color='#DDDDDD', linewidth=0.8)
ax.grid(which='minor', axis='y', color='#DDDDDD', linewidth=0.5)
ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)
ax.set_axisbelow(True)

#plt.tight_layout()
plt.savefig('KirbyFig14.png', bbox_inches='tight')
plt.savefig('fig14.pdf', bbox_inches='tight')
