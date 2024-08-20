import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from sklearn import linear_model
from sklearn.metrics import r2_score

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
cm = 1/2.54
fig, ax = plt.subplots(ncols=2, figsize=[12*cm,12*cm/(0.75*2*golden_ratio)], dpi=300)

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

#exclude cases H300-C0-G0 and H150-C0-G0
index_mask = [i != 20 and i < 30 for i in range(40)]

percentage_error = 100*(fsl[index_mask] - fsl_predictions[index_mask])/(1-fsl[index_mask])
print("Mean aboslute percentage error (%) ",np.mean(np.abs(percentage_error)))

ax[0].boxplot(percentage_error)
ax[0].set_xticks([])
ax[0].set_yticks([-15,-10,-5,0,5,10])
ax[0].set_xlim([0.85, 1.55])
ax[0].set_ylabel(r'Percentage error [\%]')
ax[0].text(1.05, 7.5, r'Overprediction', ha='left', va='center')
ax[0].text(1.05,-12.5, r'Underprediction', ha='left', va='center')
ax[0].set_title(r'(a) MAPE 5.68\%', loc='left')
ax[0].set_box_aspect(1/golden_ratio)

ax[1].plot([0, 1], [0, 1], 'grey', zorder=0)
ax[1].scatter(fsl[index_mask], fsl_predictions[index_mask], c='b', marker='x', zorder=1)
ax[1].set_xlim([0.5, 0.75])
ax[1].set_ylim([0.5, 0.75])
ax[1].set_box_aspect(1/golden_ratio)
ax[1].set_title(r'(b)', loc='left')
ax[1].set_ylabel(r'$\eta_{FS}$ (Prediction)')
ax[1].set_xlabel(r'$\eta_{FS}$ (LES)')

#fit linear regression to data
regr = linear_model.LinearRegression()
regr.fit(fsl[index_mask].reshape(-1, 1), fsl_predictions[index_mask].reshape(-1, 1))

#calculate r2 score
y_predict = regr.predict(fsl[index_mask].reshape(-1, 1))
r_squared = r2_score(fsl_predictions[index_mask], y_predict)
ax[1].text(0.51, 0.74, rf'$R^2={round(r_squared,3)}$', ha='left', va='top')

plt.subplots_adjust(wspace=0.35)
plt.savefig('KirbyFig17.png', bbox_inches='tight')
plt.savefig('fig17.pdf', bbox_inches='tight')
