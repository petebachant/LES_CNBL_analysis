import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score

plt.style.use("../style.mplstyle")

cm = 1/2.54
textwidth = 15
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=2, nrows=2, figsize=[textwidth*cm,textwidth*cm/(golden_ratio)], dpi=300)

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#array to store wake efficiencies
eta_w = np.zeros(40)
#array to store non-local efficiencies
eta_nl = np.zeros(40)
#array to store farm efficiencies
eta_f = np.zeros(40)
#turbine-scale loss factors
tsl = np.zeros(40)
#farm-scale loss factors
fsl = np.zeros(40)
#total loss i.e. P_farm/P_Betz
total_loss = np.zeros(40)

for i in range(40):
    eta_w[i] = loss_factors[i][1]
    eta_nl[i] = loss_factors[i][2]
    eta_f[i] = eta_w[i]*eta_nl[i]
    tsl[i] = loss_factors[i][3]
    fsl[i] = loss_factors[i][4]
    total_loss[i] = (1-tsl[i])*(1-fsl[i])

#exclude cases H300-C0-G0 and H150-C0-G0
index_mask = [i != 20 and i != 30 for i in range(40)]

ax[0,0].set_title(r'a)', loc='left')
ax[0,0].set_ylabel(r'$P/P_{\infty}$')
ax[0,0].set_xlabel(r'Wake efficiency $P/P_{1}$')
ax[0,0].scatter(eta_w[index_mask], total_loss[index_mask], c='b', marker='x')
ax[0,0].set_ylim([0, 0.6])
ax[0,0].set_xlim([0, 1.2])

#fit linear regression to data
regr = linear_model.LinearRegression()
regr.fit(eta_w[index_mask].reshape(-1, 1), total_loss[index_mask].reshape(-1, 1))
#calculate r2 score
y_predict = regr.predict(eta_w[index_mask].reshape(-1, 1))
r_squared = r2_score(total_loss[index_mask], y_predict)
ax[0,0].text(0.05, 0.1, rf'$R^2={round(r_squared,3)}$', ha='left', va='center')
#plot linear regression
x = np.linspace(0.4,1.05)
y = regr.predict(x.reshape(-1, 1))
ax[0,0].plot(x,y)

ax[0,1].set_title(r'b)', loc='left')
ax[0,1].set_xlabel(r'Blockage efficiency $P_1/P_{\infty}$')
ax[0,1].scatter(eta_nl[index_mask], total_loss[index_mask], c='b', marker='x')
ax[0,1].set_ylim([0, 0.6])
ax[0,1].set_xlim([0, 1.2])

#fit linear regression to data
regr = linear_model.LinearRegression()
regr.fit(eta_nl[index_mask].reshape(-1, 1), total_loss[index_mask].reshape(-1, 1))
#calculate r2 score
y_predict = regr.predict(eta_nl[index_mask].reshape(-1, 1))
r_squared = r2_score(total_loss[index_mask], y_predict)
ax[0,1].text(0.05, 0.1, rf'$R^2={round(r_squared,3)}$', ha='left', va='center')
#plot linear regression
x = np.linspace(0.2,1.05)
y = regr.predict(x.reshape(-1, 1))
ax[0,1].plot(x,y)

ax[1,0].set_title(r'c)', loc='left')
ax[1,0].set_ylabel(r'$P/P_{\infty}$')
ax[1,0].set_xlabel(r'Turbine-scale efficiency $\eta_{ts}$')
ax[1,0].scatter(1-tsl[index_mask], total_loss[index_mask], c='b', marker='x')
ax[1,0].set_ylim([0, 0.6])
ax[1,0].set_xlim([0, 1.2])


ax[1,1].set_title(r'd)', loc='left')
ax[1,1].set_xlabel(r'Farm-scale efficiency $\eta_{fs}$')
ax[1,1].scatter(1-fsl[index_mask], total_loss[index_mask], c='b', marker='x')
ax[1,1].set_ylim([0, 0.6])
ax[1,1].set_xlim([0, 0.6])

#fit linear regression to data
regr = linear_model.LinearRegression()
regr.fit(1-fsl[index_mask].reshape(-1, 1), total_loss[index_mask].reshape(-1, 1))
#calculate r2 score
y_predict = regr.predict(1-fsl[index_mask].reshape(-1, 1))
r_squared = r2_score(total_loss[index_mask], y_predict)
ax[1,1].text(0.05, 0.1, rf'$R^2={round(r_squared,3)}$', ha='left', va='center')
#plot linear regression
x = np.linspace(0.25,0.5)
y = regr.predict(x.reshape(-1, 1))
ax[1,1].plot(x,y)

plt.tight_layout()

plt.savefig('KirbyFig2.png', bbox_inches='tight')
plt.savefig('fig2.pdf', bbox_inches='tight')
