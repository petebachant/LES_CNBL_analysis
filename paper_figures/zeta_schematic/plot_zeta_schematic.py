import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(figsize=[0.5*textwidth,0.5*textwidth/(golden_ratio)], dpi=300)

x = np.linspace(0,0.3,50)
y = 30*x
plt.plot(x, y, linestyle='--', c='grey', zorder=0)

plt.scatter(0.2, 6, c='k', marker='x', zorder=1)

plt.text(0.25, 3, r'$\zeta=\frac{M-1}{1-\beta}$', ha='left', va='center')
plt.annotate("", xy=(0.204, 5.8), xytext=(0.248, 3.1), arrowprops=dict(arrowstyle="->"))

plt.xlim([0, None])
plt.ylim([0, None])
plt.ylabel(r'$M-1$')
plt.xlabel(r'$1-\beta$')

plt.savefig('KirbyFig11.png', bbox_inches='tight')
plt.savefig('fig11.pdf', bbox_inches='tight')
