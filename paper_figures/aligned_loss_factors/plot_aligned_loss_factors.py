import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=2, figsize=[textwidth,textwidth/(2.5*golden_ratio)], dpi=300)

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

ax[0].bar(np.arange(6), eta_w[index_mask], width=0.2, label=r'$\eta_w$', color=tab20(0))
ax[0].bar(np.arange(6)-0.2, eta_f[index_mask], width=0.2, label=r'$\eta_f$', color='k')
ax[0].bar(np.arange(6)+0.2, eta_nl[index_mask], width=0.2, label=r'$\eta_{nl}$', color=tab20(2))
ax[0].set_ylim([0,1.2])
ax[0].axvline(1.5, c='grey')
ax[0].axvline(3.5, c='grey')
ax[0].set_title(r'(A)', loc='left')
ax[0].set_xticks(np.arange(6), [r'Staggered', r'Aligned', r'Staggered', r'Aligned', r'Staggered', r'Aligned'], rotation=90)
ax[0].text(0.5, 1.15, r'H1000-C5-G4', ha='center', va='top')
ax[0].text(2.5, 1.15, r'H500-C5-G4', ha='center', va='top')
ax[0].text(4.5, 1.15, r'H300-C5-G4', ha='center', va='top')
ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.5), ncol=2)

ax[1].bar(np.arange(6), 1-tsl[index_mask], width=0.2, label=r'$\eta_{turbine-scale}$', color=tab20(0))
ax[1].bar(np.arange(6)-0.2, total_loss[index_mask], width=0.2, label=r'$C_p/C_{p,Betz}$', color='k')
ax[1].bar(np.arange(6)+0.2, 1-fsl[index_mask], width=0.2, label=r'$\eta_{farm-scale}$', color=tab20(2))
ax[1].set_ylim([0,1.2])
ax[1].axvline(1.5, c='grey')
ax[1].axvline(3.5, c='grey')
ax[1].set_title(r'(B)', loc='left')
ax[1].set_xticks(np.arange(6), [r'Staggered', r'Aligned', r'Staggered', r'Aligned', r'Staggered', r'Aligned'], rotation=90)
ax[1].text(0.5, 1.15, r'H1000-C5-G4', ha='center', va='top')
ax[1].text(2.5, 1.15, r'H500-C5-G4', ha='center', va='top')
ax[1].text(4.5, 1.15, r'H300-C5-G4', ha='center', va='top')
ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.5), ncol=2)
ax[1].plot([-0.5, 1.5], [0.450, 0.450], c='grey', linestyle='--', zorder=0)
ax[1].plot([1.5, 3.5], [0.427, 0.427], c='grey', linestyle='--', zorder=0)
ax[1].plot([3.5, 5.5], [0.369, 0.369], c='grey', linestyle='--', zorder=0)
ax[1].set_xlim([-0.5,5.5])

#plt.tight_layout()
plt.savefig('KirbyFig15.png', bbox_inches='tight')
plt.savefig('fig15.pdf', bbox_inches='tight')
