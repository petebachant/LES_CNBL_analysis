import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sp
import matplotlib as mpl


plt.style.use("../style.mplstyle")

tab10 = mpl.colormaps['tab10']

cm = 1/2.54
textwidth = 15
golden_ratio = 1.61803
fig, ax = plt.subplots(figsize=[textwidth*cm,textwidth*cm/(1.5*golden_ratio)], dpi=300)

#wind farm parameters
#momentum `extractability' factor
zeta=[0,5,10,15,20,25]
#bottom friction exponent
gamma=2

#arrays to store result
cp_finite = np.zeros((50,6))
effective_area_ratio = np.zeros(50)
cp_nishino = np.zeros((50,6))

#load LES data
training_data = np.genfromtxt('LES_training_data.csv', delimiter=',')
#remove header
training_data = np.delete(training_data, 0, 0)
training_data = np.delete(training_data, 0, 1)

#note correction factor N^2 already applied!
ct_star = training_data[:,3]
beta = training_data[:,5]
#note correction factor N^3 already applied!
cp = training_data[:,7]
cp_corrected = np.zeros((50))
beta_corrected = np.zeros((50))

################################
#1. Correct LES wind speed
################################

for run_no in range(50):

        #calculate effective area ratio
        C_f0 = 0.28641758**2/(0.5*10.10348311**2)
        A = np.pi/4
        S = training_data[run_no,0]*training_data[run_no,1]
        area_ratio = A/S
        effective_area_ratio[run_no] = area_ratio/C_f0

        #calculate beta_fine_theory
        def NDFM(beta):
            """ Non-dimensional farm momentum
            equation (see Nishino 2020)
            """
	    #use ct_star to predict beta_fine_theory
            return ct_star[run_no]*effective_area_ratio[run_no]*beta**2 + beta**gamma - 1

        beta_fine_theory = sp.bisect(NDFM,0,1)

        #calculate beta_coarse_theory
        def NDFM(beta):
            """ Non-dimensional farm momentum
            equation (see Nishino 2020)
            """
	    #use ct_star to predict beta_fine_theory
            return (ct_star[run_no]/ 0.8037111)*effective_area_ratio[run_no]*beta**2 + beta**gamma - 1

        beta_coarse_theory = sp.bisect(NDFM,0,1)

        #correct Cp values recorded by LES
        cp_corrected[run_no] = cp[run_no]*(beta_fine_theory/beta_coarse_theory)**3
        #correct beta value recorded by LES
        beta_corrected[run_no] = beta[run_no]*(beta_fine_theory/beta_coarse_theory)


#repeat for different zeta values
for i in range(6):

    #############################################
    # 2. Calculate Cp from LES data for a finite
    # wind farm
    #############################################

    #calculate adjusted Cp and effective area ratio
    #for each wind farm LES
    for run_no in range(50):
        U_F = beta_corrected[run_no]*10.10348311
        U_F0 = 10.10348311

        #coefficients of quadratic formula to solve
        a = 1/U_F**2
        b = zeta[i]/U_F0
        c = -zeta[i] - 1

        U_Fprime = (-b + np.sqrt(b**2 - 4*a*c))/(2*a)
    
        cp_finite[run_no,i] = cp_corrected[run_no]*(U_Fprime/U_F)**3

    #############################################
    # 3. Predict Cp using two-scale momentum
    # theory
    #############################################

    #predict Cp for each wind farm LES
    for run_no in range(50):

        def NDFM(beta):
            """ Non-dimensional farm momentum
            equation (see Nishino 2020)
            """
	    #use ct_star to predict beta
	    #analytical model gives ct_star = 0.75
            ct_star = 0.75
            return ct_star*effective_area_ratio[run_no]*beta**2 + beta**gamma - 1 -zeta[i]*(1-beta)

        beta_theory = sp.bisect(NDFM,0,1)
        cp_nishino[run_no,i] = 0.75**1.5 * beta_theory**3 * 1.33**-0.5

ax.scatter(effective_area_ratio, cp_finite[:,5]/0.562, c='r', marker='x')
ax.scatter(effective_area_ratio, cp_finite[:,1]/0.562, c='r', marker='x')

cp_ratio = np.zeros(50)
effective_array_density = np.linspace(2,25,50)

ctstar = 0.75

for count, zeta in enumerate([25, 5]):

    for i in range(50):

        def ndfm(beta):
            lhs = ctstar*effective_array_density[i]*beta**2 + beta**2

            rhs = 1 + zeta*(1-beta)

            return lhs - rhs

        beta = sp.bisect(ndfm,1,0.3)
        cp_ratio[i] = beta**3

    ax.plot(effective_array_density, cp_ratio, c=tab10(0))

ax.set_ylim([0, 1.1])
ax.set_ylabel(r'Farm efficiency $P/P_{\infty}$')
ax.set_xlabel(r'Effective farm density $\lambda/C_{f0}$')
ax.text(4, 0.8, r'$\zeta=25$', ha='left', va='bottom')
ax.text(4, 0.4, r'$\zeta=5$', ha='right', va='top')

ax.plot([2, 25], [1, 1], c='k')
ax.text(12.5, 1, r"Isolated turbine", ha='center', va='bottom')

plt.savefig('KirbyFig1.png', bbox_inches='tight')
plt.savefig('fig1.pdf', bbox_inches='tight')

fig, ax = plt.subplots(figsize=[textwidth*cm,textwidth*cm/(1.5*golden_ratio)], dpi=300)

ax.scatter(effective_area_ratio[49], cp_finite[49,5]/0.562, c='r', marker='x')

for count, zeta in enumerate([25]):

    for i in range(50):

        def ndfm(beta):
            lhs = ctstar*effective_array_density[i]*beta**2 + beta**2

            rhs = 1 + zeta*(1-beta)

            return lhs - rhs

        beta = sp.bisect(ndfm,1,0.3)
        cp_ratio[i] = beta**3

    ax.plot(effective_array_density, cp_ratio, c=tab10(0))

ax.annotate("", xy=(10, 0.53), xytext=(10,1), arrowprops=dict(arrowstyle="->"))
ax.annotate("", xy=(10, 0.41), xytext=(10,0.54), arrowprops=dict(arrowstyle="->"))

ax.text(9.4, 0.85, r'$\eta_{FS}$', ha='right', va='center')
t = ax.text(9.4, 0.47, r'$\eta_{TS}$', ha='right', va='center')
t.set_bbox(dict(facecolor='white', linewidth=0))

ax.set_ylim([0, 1.1])
ax.set_ylabel(r'Farm efficiency $P/P_{\infty}$')
ax.set_xlabel(r'Effective farm density $\lambda/C_{f0}$')
ax.text(4, 0.8, r'$\zeta=25$', ha='left', va='bottom')

ax.plot([2, 25], [1, 1], c='k')
ax.text(12.5, 1, r"Isolated turbine", ha='center', va='bottom')

plt.savefig('KirbyFig1a.png', bbox_inches='tight')
plt.savefig('fig1a.pdf', bbox_inches='tight')
