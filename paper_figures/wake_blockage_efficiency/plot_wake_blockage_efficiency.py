import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
cm = 1/2.54
fig, ax = plt.subplots(ncols=2, figsize=[12*cm,12*cm/(golden_ratio)], dpi=300, layout="constrained")

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#array to store wake efficiencies
eta_w = np.zeros(40)
#array to store non-local efficiencies
eta_nl = np.zeros(40)
#array to store farm efficiencies
eta_f = np.zeros(40)

for i in range(40):
    eta_w[i] = loss_factors[i][1]
    eta_nl[i] = loss_factors[i][2]
    eta_f[i] = eta_w[i]*eta_nl[i]

#exclude cases H300-C0-G0 and H150-C0-G0
index_mask = [i != 20 and i != 30 for i in range(40)]

#plot farm efficiency against wake efficiency
ax[0].scatter(eta_w[index_mask], eta_f[index_mask], c='b', marker='x')

#fit linear regression to data
regr = linear_model.LinearRegression()
regr.fit(eta_w[index_mask].reshape(-1, 1), eta_f[index_mask].reshape(-1, 1))

#calculate r2 score
y_predict = regr.predict(eta_w[index_mask].reshape(-1, 1))
r_squared = r2_score(eta_f[index_mask], y_predict)
ax[0].text(0.1, 0.1, rf'$R^2={round(r_squared,3)}$', ha='left', va='center')
ax[0].set_ylim([0, 0.6])
ax[0].set_xlim([0, 1.4])
ax[0].set_title(r'a)', loc='left')

#plot linear regression
x = np.linspace(0.4, 1.3)
y = regr.predict(x.reshape(-1, 1))
ax[0].plot(x,y)

ax[0].set_ylabel(r'$\eta_f=P_{farm}/P_{\infty}$')
ax[0].set_xlabel(r'$\eta_w=P_{farm}/P_{1}$')
ax[0].set_box_aspect(1/golden_ratio)

#plot farm efficiency against non-local efficiency
ax[1].scatter(eta_nl[index_mask], eta_f[index_mask], c='b', marker='x')

#fit linear regression to data
regr = linear_model.LinearRegression()
regr.fit(eta_nl[index_mask].reshape(-1, 1), eta_f[index_mask].reshape(-1, 1))

#calculate r2 score
y_predict = regr.predict(eta_nl[index_mask].reshape(-1, 1))
r_squared = r2_score(eta_f[index_mask], y_predict)
ax[1].text(0.1, 0.1, rf'$R^2={round(r_squared,3)}$', ha='left', va='center')
ax[1].set_ylim([0, 0.6])
ax[1].set_xlim([0, 1.2])
ax[1].set_title(r'b)', loc='left')

#plot linear regression
x = np.linspace(0.2,1)
y = regr.predict(x.reshape(-1, 1))
ax[1].plot(x,y)

ax[1].set_xlabel(r'$\eta_{nl}=P_{1}/P_{\infty}$')
ax[1].set_box_aspect(1/golden_ratio)

#plt.tight_layout()
plt.savefig('KirbyFig3.png', bbox_inches='tight')
plt.savefig('fig3.pdf', bbox_inches='tight')
