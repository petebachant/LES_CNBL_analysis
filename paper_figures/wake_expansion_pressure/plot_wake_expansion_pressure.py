import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(figsize=[0.5*textwidth,0.5*textwidth/(golden_ratio)], dpi=300)

#load csv file of farm loss factors
loss_factors = np.genfromtxt('../loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#array to store wake expansion coefficients
kstar = np.zeros(40)
#array to store farm pressure gradients
pressure_farm = np.zeros(40)

for i in range(40):
    kstar[i] = loss_factors[i][6]
    pressure_farm[i] = loss_factors[i][11]

#exclude cases H300-C0-G0 and H150-C0-G0
index_mask = [i != 20 and i < 30 for i in range(40)]
plt.scatter(pressure_farm[index_mask], kstar[index_mask], c='b', marker='x')

#fit linear regression to data
regr = linear_model.LinearRegression()
regr.fit(pressure_farm[index_mask].reshape(-1, 1), kstar[index_mask].reshape(-1, 1))

#calculate r2 score
y_predict = regr.predict(pressure_farm[index_mask].reshape(-1, 1))
r_squared = r2_score(kstar[index_mask], y_predict)
plt.text(2.5,0.02, rf'$R^2={round(r_squared,3)}$', ha='left', va='center')

#plot linear regression
x = np.linspace(4,29)
y = regr.predict(x.reshape(-1, 1))
plt.plot(x,y)

plt.xlim([0, 30])
plt.ylim([0, 0.12])

plt.tight_layout()
plt.ylabel(r'$k^*$', rotation=0)
plt.xlabel(r'$\Delta p_f / \rho_0$ (m$^2$s$^{-2}$)')
plt.savefig('KirbyFigA3.png', bbox_inches='tight')
plt.savefig('figA3.pdf', bbox_inches='tight')
