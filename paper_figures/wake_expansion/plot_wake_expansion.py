import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
cm = 1/2.54
fig, ax = plt.subplots(ncols=2, figsize=[12*cm,12*cm/(0.75*2*golden_ratio)], dpi=300, layout='constrained')

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#array to store wake efficiencies
eta_w = np.zeros(40)
#array to store non-local efficiencies
eta_nl = np.zeros(40)
#array to store farm efficiencies
eta_f = np.zeros(40)
#array to store wake expansion coefficients
k_star = np.zeros(40)

for i in range(40):
    eta_w[i] = loss_factors[i][1]
    eta_nl[i] = loss_factors[i][2]
    eta_f[i] = eta_w[i]*eta_nl[i]
    k_star[i] = loss_factors[i][6]

#exclude cases H300-C0-G0 and H150-C0-G0
index_mask = [i != 20 and i < 30 for i in range(40)]

#plot farm efficiency against wake efficiency
ax[0].scatter(k_star[index_mask], eta_f[index_mask], c='b', marker='x')

#fit linear regression to data
regr = linear_model.LinearRegression()
regr.fit(k_star[index_mask].reshape(-1, 1), eta_f[index_mask].reshape(-1, 1))

#calculate r2 score
y_predict = regr.predict(k_star[index_mask].reshape(-1, 1))
r_squared = r2_score(eta_f[index_mask], y_predict)
ax[0].text(0.01, 0.1, rf'$R^2={round(r_squared,3)}$', ha='left', va='center')
ax[0].set_ylim([0, 0.6])
ax[0].set_xlim([0, 0.125])

#plot linear regression
x = np.linspace(0.07, 0.105)
y = regr.predict(x.reshape(-1, 1))
ax[0].plot(x,y,c='k')

ax[0].set_ylabel(r'$\eta_f$ [-]')
ax[0].set_xlabel(r'$k^*$ [-]')
ax[0].set_title(r'(a)', loc='left')
ax[0].set_box_aspect(1/golden_ratio)

#plot farm efficiency against non-local efficiency
ax[1].scatter(k_star[index_mask], eta_w[index_mask], c='b', marker='x')

#fit linear regression to data
regr = linear_model.LinearRegression()
regr.fit(k_star[index_mask].reshape(-1, 1), eta_w[index_mask].reshape(-1, 1))

#calculate r2 score
y_predict = regr.predict(k_star[index_mask].reshape(-1, 1))
r_squared = r2_score(eta_w[index_mask], y_predict)
ax[1].text(0.01, 0.2, rf'$R^2={round(r_squared,3)}$', ha='left', va='center')
ax[1].text(0.12, 1, rf'Faster' +'\n'+ r'recovery', ha='right', va='center', ma='left')
ax[1].text(0.06, 1, rf'Slower' +'\n'+ r'recovery', ha='right', va='center', ma='left')
ax[1].set_ylim([0, 1.2])
ax[1].set_xlim([0, 0.125])

#plot linear regression
x = np.linspace(0.07, 0.105)
y = regr.predict(x.reshape(-1, 1))
ax[1].plot(x,y,c='k')

ax[1].set_ylabel(r'$\eta_w$ [-]')
ax[1].set_xlabel(r'$k^*$ [-]')
ax[1].set_title(r'(b)', loc='left')
ax[1].set_box_aspect(1/golden_ratio)

#plt.tight_layout()
plt.savefig('KirbyFig8.png', bbox_inches='tight')
plt.savefig('fig8.pdf', bbox_inches='tight')
