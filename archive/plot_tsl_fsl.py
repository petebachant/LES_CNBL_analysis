import matplotlib.pyplot as plt
import numpy as np

plt.style.use("plots/style.mplstyle")

fig, ax = plt.subplots(figsize=[6,4], dpi=300)

eta_f = np.array([0.51, 0.5, 0.44, 0.43])
eta_wake = np.array([0.59, 0.71, 1.0, 0.5])
eta_nl = np.array([0.87, 0.7, 0.44, 0.86])

eta_f_adjusted = np.array([0.469, 0.450, 0.384, 0.375])
tsl = np.array([1.0406, 1.0523, 1.0575, 1.0627])
fsl = np.array([0.451, 0.428, 0.363, 0.353])

ax.bar(np.arange(4)-0.2, eta_f, width=0.2, label=r'$\eta_f$', color='k')
ax.bar(np.arange(4), eta_wake, width=0.2, label=r'$\eta_w$')
ax.bar(np.arange(4)+0.2, eta_nl, width=0.2, label=r'$\eta_{nl}$')
plt.xticks(np.arange(4), [r'H1000-C5-G4', r'H500-C5-G4', r'H300-C8-G1', r'H300-C2-G1'], fontsize=14)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncols=3)
plt.ylim([0,1.15])
plt.xlim([-0.5,3.5])
plt.tight_layout()
plt.savefig('plots/wake_blockage_loss.png')
plt.close()


fig, ax = plt.subplots(figsize=[6,4], dpi=300)
ax.bar(np.arange(4)-0.2, eta_f_adjusted, width=0.2, label=r'$\eta_f$', color='k')
ax.bar(np.arange(4), tsl, width=0.2, label=r'$1-\Pi_T$')
ax.bar(np.arange(4)+0.2, fsl, width=0.2, label=r'$1-\Pi_F$')
plt.xticks(np.arange(4), [r'H1000-C5-G4', r'H500-C5-G4', r'H300-C8-G1', r'H300-C2-G1'], fontsize=14)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncols=3)
plt.ylim([0,1.15])
plt.xlim([-0.5,3.5])
plt.tight_layout()
plt.savefig('plots/tsl_fsl.png')
plt.close()