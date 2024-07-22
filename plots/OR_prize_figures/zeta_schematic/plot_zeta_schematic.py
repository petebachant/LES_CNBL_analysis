import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sp

plt.style.use("../style.mplstyle")

cm = 1/2.54
textwidth = 15
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=[0.5*textwidth*cm,textwidth*cm/(2*1.1*golden_ratio)], dpi=300, layout='constrained')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_box_aspect(1/golden_ratio)
ax.set_ylabel(r'$M$', rotation = 0)
ax.set_xlabel(r'$1-\beta$')

x = np.linspace(0,0.3,100)
y = 15*x + 1

ax.plot(x, y, c='k')
ax.set_xlim([0, None])
ax.set_ylim([0, None])

plt.savefig('KirbyFig3.png', bbox_inches='tight')
plt.savefig('fig3.pdf', bbox_inches='tight')

fig, ax = plt.subplots(ncols=1, nrows=1, figsize=[0.5*textwidth*cm,textwidth*cm/(2*1.1*golden_ratio)], dpi=300, layout='constrained')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_box_aspect(1/golden_ratio)
ax.set_ylabel(r'$M$', rotation = 0)
ax.set_xlabel(r'$1-\beta$')

x = np.linspace(0,0.3,100)
y = 15*x + 1

ax.plot(x, y, c='k', alpha=0.5)
ax.set_xlim([0, None])
ax.set_ylim([0, None])

y = 25*x + 1
ax.plot(x, y, c='k')

plt.savefig('KirbyFig3b.png', bbox_inches='tight')
plt.savefig('fig3b.pdf', bbox_inches='tight')
