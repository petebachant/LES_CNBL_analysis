import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
cm = 1/2.54
fig, ax = plt.subplots(ncols=3, figsize=[12*cm,0.33*12*cm/(0.75*golden_ratio)], dpi=300, layout='constrained')

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#array to store momentum availability factors
M = np.zeros(44)
#array to store farm wind speed reduction factors
beta = np.zeros(44)
case_id = []

for i in range(44):
    M[i] = loss_factors[i][8]
    beta[i] = loss_factors[i][9]
    case_id.append(loss_factors[i][0])

x = np.linspace(0,0.32,10)

ax[0].scatter(1-beta[40], M[40]-1, c='r', marker='x', zorder=1)
ax[0].scatter(1-beta[5], M[5]-1, c='r', marker='o', zorder=1)
print(case_id[5])
print(case_id[40])
ax[0].plot(x, 40.617218*x, c='grey', linestyle='--', zorder=0)
ax[0].text(0.15, 4.5, r'$\zeta=40.6$', c='grey')

ax[0].set_ylabel(r'$M_{LES}-1$ [-]')
ax[0].set_xlabel(r'$1-\beta_{LES}$ [-]')
ax[0].set_xlim([0, 0.32])
ax[0].set_ylim([0, 12])
ax[0].set_title(r'(a) H1000-C5-G4', loc='left')
ax[0].set_box_aspect(1/golden_ratio)

ax[1].scatter(1-beta[43], M[43]-1, c='r', marker='P', zorder=1, label=r'Double spacing')
ax[1].scatter(1-beta[41], M[41]-1, c='r', marker='x', zorder=1, label=r'Aligned layout')
ax[1].scatter(1-beta[15], M[15]-1, c='r', marker='o', zorder=1, label=r'Staggered layout')
print(case_id[15])
print(case_id[41])
ax[1].plot(x, 38.052374*x, c='grey', linestyle='--', zorder=0)
ax[1].text(0.16, 4.5, r'$\zeta=38.1$', c='grey')

ax[1].set_xlabel(r'$1-\beta_{LES}$ [-]')
ax[1].set_xlim([0, 0.32])
ax[1].set_ylim([0, 12])
ax[1].set_title(r'(b) H500-C5-G4', loc='left')
ax[1].set_box_aspect(1/golden_ratio)

ax[2].scatter(1-beta[25], M[25]-1, c='r', marker='o', zorder=1)
print(case_id[25])
ax[2].scatter(1-beta[42], M[42]-1, c='r', marker='x', zorder=1)
print(case_id[42])
ax[2].plot(x, 30.201715*x, c='grey', linestyle='--', zorder=0)
ax[2].text(0.17, 3.6, r'$\zeta=30.2$', c='grey')

ax[2].set_xlabel(r'$1-\beta_{LES}$ [-]')
ax[2].set_xlim([0, 0.32])
ax[2].set_ylim([0, 12])
ax[2].set_title(r'(c) H300-C5-G4', loc='left')
ax[2].set_box_aspect(1/golden_ratio)

fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)

plt.savefig('KirbyFig9.png', bbox_inches='tight')
plt.savefig('fig9.pdf', bbox_inches='tight')
