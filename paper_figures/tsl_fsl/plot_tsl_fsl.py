import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=2, figsize=[textwidth,textwidth/(2*golden_ratio)], dpi=300)

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#turbine-scale loss factors
tsl = np.zeros(40)
#farm-scale loss factors
fsl = np.zeros(40)
#total loss i.e. P_farm/P_Betz
total_loss = np.zeros(40)

for i in range(40):
    tsl[i] = loss_factors[i][3]
    fsl[i] = loss_factors[i][4]
    total_loss[i] = (1-tsl[i])*(1-fsl[i])

#exclude cases H300-C0-G0 and H150-C0-G0
index_mask = [i != 20 and i != 30 for i in range(40)]

#plot farm efficiency against wake efficiency
ax[0].scatter(1-tsl[index_mask], total_loss[index_mask], c='b', marker='x')

ax[0].set_ylim([0, 0.6])
ax[0].set_xlim([0, 1.2])

ax[0].set_ylabel(r'$C_p/C_{p,Betz}$')
ax[0].set_xlabel(r'$1-\Pi_T$')
ax[0].set_title(r'(A)', loc='left')

#plot farm efficiency against non-local efficiency
ax[1].scatter(1-fsl[index_mask], total_loss[index_mask], c='b', marker='x')

#fit linear regression to data
regr = linear_model.LinearRegression()
regr.fit(1-fsl[index_mask].reshape(-1, 1), total_loss[index_mask].reshape(-1, 1))

#calculate r2 score
y_predict = regr.predict(1-fsl[index_mask].reshape(-1, 1))
r_squared = r2_score(total_loss[index_mask], y_predict)
ax[1].text(0.05, 0.5, rf'$R^2={round(r_squared,3)}$', ha='left', va='center')
ax[1].set_ylim([0, 0.6])
ax[1].set_xlim([0, 0.6])
ax[1].set_title(r'(B)', loc='left')

#plot linear regression
x = np.linspace(0.25,0.5)
y = regr.predict(x.reshape(-1, 1))
ax[1].plot(x,y)

ax[1].set_xlabel(r'$1-\Pi_F$')

plt.tight_layout()
plt.savefig('KirbyFig13.png', bbox_inches='tight')
plt.savefig('fig13.pdf', bbox_inches='tight')
