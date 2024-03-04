import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score

plt.style.use("../style.mplstyle")

tab10 = mpl.colormaps['tab10']

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(nrows=2, figsize=[textwidth,textwidth/(golden_ratio)], dpi=300)

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#internal turbine thrust coefficient
ctstar = np.zeros(44)
#wind extractability factors
zeta = np.zeros(44)
case_id = []

for i in range(44):
    ctstar[i] = loss_factors[i][7]
    zeta[i] = loss_factors[i][10]
    case_id.append(loss_factors[i][0])

#exclude cases H300-C0-G0 and H150-C0-G0
index_mask = [i != 20 and i != 30 for i in range(44)]

x = np.arange(38)

#plot `internal' turbine thrust coefficient`
ax[0].scatter(0, ctstar[0], c='k')
ax[0].scatter(x[1:10], ctstar[index_mask][1:10], c=tab10(0*np.ones(9).astype(int), alpha=(10-np.arange(1,10)%10)/10), edgecolor='k')
ax[0].scatter(x[5], ctstar[40], c='k', marker='x')
ax[0].scatter(0, ctstar[0], c='k')
ax[0].scatter(x[10], ctstar[index_mask][10], c='k')
ax[0].scatter(x[11:20], ctstar[index_mask][11:20], c=tab10(1*np.ones(9).astype(int), alpha=(10-np.arange(1,10)%10)/10), edgecolor='k')
ax[0].scatter(x[15], ctstar[41], c='k', marker='x')
ax[0].scatter(x[20:29], ctstar[index_mask][20:29], c=tab10(2*np.ones(9).astype(int), alpha=(10-np.arange(1,10)%10)/10), edgecolor='k')
ax[0].scatter(x[24], ctstar[42], c='k', marker='x')
ax[0].scatter(x[29:38], ctstar[index_mask][29:38], c=tab10(3*np.ones(9).astype(int), alpha=(10-np.arange(1,10)%10)/10), edgecolor='k')

ax[0].scatter(-10, 1, marker='o', c='None', edgecolor='k', label=r'Staggered turbine layout')
ax[0].scatter(-10, 1, marker='x', c='k', label=r'Aligned turbine layout')
ax[0].legend(loc='lower right')


ax[0].set_xticks(range(38))
ax[0].set_xticklabels([])
ax[0].set_ylim([0, 1.1])
ax[0].set_xlim([-1, 38])
ax[0].set_title(r'(A)', loc='left')
ax[0].set_ylabel(r'$C_{T,LES}^*$', rotation=0, labelpad=20)

#plot wind `extractability' factor zeta`
ax[1].scatter(0, zeta[0], c='k')
ax[1].scatter(x[1:10], zeta[index_mask][1:10], c=tab10(0*np.ones(9).astype(int), alpha=(10-np.arange(1,10)%10)/10), edgecolor='k')
ax[1].scatter(x[5], zeta[40], c='k', marker='x')
ax[1].scatter(0, zeta[0], c='k')
ax[1].scatter(x[10], zeta[index_mask][10], c='k')
ax[1].scatter(x[11:20], zeta[index_mask][11:20], c=tab10(1*np.ones(9).astype(int), alpha=(10-np.arange(1,10)%10)/10), edgecolor='k')
ax[1].scatter(x[15], zeta[41], c='k', marker='x')
ax[1].scatter(x[20:29], zeta[index_mask][20:29], c=tab10(2*np.ones(9).astype(int), alpha=(10-np.arange(1,10)%10)/10), edgecolor='k')
ax[1].scatter(x[24], zeta[42], c='k', marker='x')
ax[1].scatter(x[29:38], zeta[index_mask][29:38], c=tab10(3*np.ones(9).astype(int), alpha=(10-np.arange(1,10)%10)/10), edgecolor='k')
ax[1].set_ylim([0, 50])
ax[1].set_xlim([-1, 38])

ax[1].set_xticks(range(38))
ax[1].set_xticklabels(case_id[:20]+case_id[21:30]+case_id[31:40],rotation=90)
ax[1].set_title(r'(B)', loc='left')
ax[1].set_ylabel(r'$\zeta_{LES}$', rotation=0, labelpad=20)

plt.tight_layout()
plt.savefig('KirbyFig11.png', bbox_inches='tight')
plt.savefig('fig11.pdf', bbox_inches='tight')
