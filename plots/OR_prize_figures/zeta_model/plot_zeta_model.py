import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sp

plt.style.use("../style.mplstyle")

cm = 1/2.54
textwidth = 15
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=[0.5*textwidth*cm,textwidth*cm/(2*1.1*golden_ratio)], dpi=300, layout='constrained')

for cf0 in [0.001, 0.002, 0.004, 0.01]:
    fsr = np.linspace(5,100,100)
    zeta = 1.18 + 2.18/(cf0*fsr)
    plt.plot(fsr,zeta, c='k')

ax.set_ylim([0, 30])
ax.set_ylabel(r'$\zeta$', rotation=0)
ax.set_xlabel(r'Farm size ratio $L/h_0$')

ax.text(35, 7, r'$C_{f0}=0.01$', ha='right', va='top')
ax.text(50, 12, r'$0.004$', ha='left', va='bottom')
ax.text(65, 18, r'$0.002$', ha='left', va='bottom')
ax.text(100, 29.5, r'$0.001$', ha='right', va='top')

plt.savefig('KirbyFig3.png', bbox_inches='tight')
