import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(figsize=[0.5*textwidth,0.5*textwidth/(golden_ratio)], dpi=300)

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#array to store momentum availability factors
M = np.zeros(40)
#array to store farm wind speed reduction factors
beta = np.zeros(40)

for i in range(40):
    M[i] = loss_factors[i][8]
    beta[i] = loss_factors[i][9]

plt.scatter(1-beta[19], M[19]-1, c='r', marker='o', zorder=1)
plt.scatter(1-beta[29], M[29]-1, c='r', marker='o', zorder=1)

x = np.linspace(0, 30, 100)
zeta = (M[19]-1)/(1-beta[19])
plt.plot(x, zeta*x, c='grey', linestyle='--', zorder=0)
zeta = (M[29]-1)/(1-beta[29])
plt.plot(x, zeta*x, c='grey', linestyle='--', zorder=0)

plt.text(0.225, 10, r'H500-C8-G8', ha='right', va='bottom')
plt.text(0.275, 8.5, r'H300-C8-G8', ha='left', va='top')
plt.text(0.25, 4, r'$\zeta_{LES}=\frac{M_{LES}-1}{1-\beta_{LES}}$')
ax.annotate("", xy=(0.18, 6.3), xytext=(0.25, 4.25), arrowprops=dict(arrowstyle="->"))

plt.ylabel(r'$M_{LES}-1$')
plt.xlabel(r'$1-\beta_{LES}$')

plt.xlim([0, 0.4])
plt.ylim([0, 12])

plt.savefig('KirbyFig11.png', bbox_inches='tight')
plt.savefig('fig11.pdf', bbox_inches='tight')
