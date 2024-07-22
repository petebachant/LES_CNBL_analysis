import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sp

plt.style.use("../style.mplstyle")

cm = 1/2.54
textwidth = 15
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=[0.5*textwidth*cm,textwidth*cm/(2*1.1*golden_ratio)], dpi=300, layout='constrained')

ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect('equal')


ax.fill([-1,3.5,3.5,-1],[0,0,-0.2,-0.2], fill=False, hatch = '//')
ax.plot([0,2.5,2.5,0,0],[0,0,1,1,0], c='k')

plt.savefig('KirbyFig3.png', bbox_inches='tight')
plt.savefig('fig3.pdf', bbox_inches='tight')
