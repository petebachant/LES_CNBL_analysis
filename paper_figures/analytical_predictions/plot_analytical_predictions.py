import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=2, figsize=[textwidth,textwidth/(2*golden_ratio)], dpi=300)

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)


#farm-scale loss factors
fsl = np.zeros(40)
#total loss i.e. P_farm/P_Betz
fsl_predictions = np.zeros(40)

for i in range(40):
    fsl[i] = loss_factors[i][4]
    fsl_predictions[i] = loss_factors[i][5]

tab20 = mpl.colormaps['tab20']

index_mask = [5, 15, 25]
ax[0].bar(np.arange(3)-0.1, 1-fsl[index_mask], width=0.2, label=r'LES results', color=tab20(2))
ax[0].bar(np.arange(3)+0.1, 1-fsl_predictions[index_mask], width=0.2, label=r'Analytical predictions', color=tab20(3))
ax[0].set_xticks([0,1,2])
ax[0].set_xticklabels([r'H1000-C5-G4', r'H500-C5-G4', r'H300-C5-G4'])
ax[0].set_ylabel(r'$\eta_{farm-scale}$')
ax[0].set_ylim([0,1.1])
ax[0].set_title(r'(A)', loc='left')
ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)

#exclude cases H300-C0-G0 and H150-C0-G0
index_mask = [i != 20 and i < 30 for i in range(40)]

percentage_error = 100*(fsl[index_mask] - fsl_predictions[index_mask])/(1-fsl[index_mask])
print("Mean aboslute percentage error (%) ",np.mean(np.abs(percentage_error)))

ax[1].boxplot(percentage_error)
ax[1].set_xticks([])
ax[1].set_yticks([-15,-10,-5,0,5,10])
ax[1].set_xlim([0.8, 1.5])
ax[1].set_ylabel(r'Percentage error (\%)')
ax[1].text(1.2, 7.5, r'Overprediction', ha='left', va='center')
ax[1].text(1.2,-12.5, r'Underprediction', ha='left', va='center')
ax[1].set_title(r'(B) MAPE 5.67\%', loc='left')

plt.tight_layout()
plt.savefig('KirbyFig18.png', bbox_inches='tight')
plt.savefig('fig18.pdf', bbox_inches='tight')
