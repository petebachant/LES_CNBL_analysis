import matplotlib.pyplot as plt
import numpy as np
import h5py
import matplotlib as mpl

#path variable to change
path = '/mnt/c/Users/trin3517/Documents/PhD/Year 4/Research plots and presentations/LES_data/'


plt.style.use("../style.mplstyle")

textwidth = 7
cm = 1/2.54
golden_ratio = 1.61803

fig, ax = plt.subplots(ncols=2, figsize=[12*cm,12*cm/(0.75*2*golden_ratio)],
        dpi=300)

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#array to store wake efficiencies
eta_w = np.zeros(45)
#array to store non-local efficiencies
eta_nl = np.zeros(45)
#array to store farm efficiencies
eta_f = np.zeros(45)
#turbine-scale loss factors
tsl = np.zeros(45)
#farm-scale loss factors
fsl = np.zeros(45)
#total loss i.e. P_farm/P_Betz
total_loss = np.zeros(45)
case_id = []

for i in range(45):
    eta_w[i] = loss_factors[i][1]
    eta_nl[i] = loss_factors[i][2]
    eta_f[i] = eta_w[i]*eta_nl[i]
    tsl[i] = loss_factors[i][3]
    fsl[i] = loss_factors[i][4]
    total_loss[i] = (1-tsl[i])*(1-fsl[i])
    case_id.append(loss_factors[i][0])

index_mask = [15, 44, 43]

tab20 = mpl.colormaps['tab20']

ax[0].bar(np.arange(3), eta_w[index_mask], width=0.2, label=r'$\eta_w$', color=tab20(0))
ax[0].bar(np.arange(3)-0.2, eta_f[index_mask], width=0.2, label=r'$\eta_f$', color='k')
ax[0].bar(np.arange(3)+0.2, eta_nl[index_mask], width=0.2, label=r'$\eta_{nl}$', color=tab20(2))
ax[0].set_ylim([0,1.2])
ax[0].set_title(r'a)', loc='left')
ax[0].set_xticks(np.arange(3), [r'Standard', r'Half length', r'Double'+'\n'+'spacing'], rotation=90)
ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.65), ncol=2)
ax[0].set_box_aspect(1/golden_ratio)

ax[1].bar(np.arange(3), 1-tsl[index_mask], width=0.2, label=r'$\eta_{TS}$', color=tab20(0))
ax[1].bar(np.arange(3)-0.2, total_loss[index_mask], width=0.2, label=r'$C_p/C_{p,Betz}$', color='k')
ax[1].bar(np.arange(3)+0.2, 1-fsl[index_mask], width=0.2, label=r'$\eta_{FS}$', color=tab20(2))
ax[1].text(0, 1.049, r'1.049', ha='center', va='bottom')
ax[1].text(1, 1.038, r'1.038', ha='center', va='bottom')
ax[1].text(2, 0.975, r'0.975', ha='center', va='bottom')
ax[1].set_ylim([0,1.2])
ax[1].set_title(r'b)', loc='left')
ax[1].set_xticks(np.arange(3), [r'Standard', r'Half length', r'Double'+'\n'+r'spacing'],rotation=90)
ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.65), ncol=2)
ax[1].set_box_aspect(1/golden_ratio)

#plt.tight_layout()

plt.savefig('KirbyFig16.png', bbox_inches='tight')
plt.savefig('fig16.pdf', bbox_inches='tight')
