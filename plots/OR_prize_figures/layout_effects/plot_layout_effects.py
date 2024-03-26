import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sp

plt.style.use("../style.mplstyle")

cm = 1/2.54
textwidth = 15
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=2, nrows=1, figsize=[textwidth*cm,textwidth*cm/(2*1.1*golden_ratio)], dpi=300, layout='constrained')

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

eta_ts = cp_finite/cp_nishino
eta_fs = cp_nishino/0.563205

ax[0].hist(eta_ts[:,1], density=True, bins=5, label=r'$\eta_{TS}$')
ax[0].hist(eta_fs[:,1], density=True, bins=5, label=r'$\eta_{FS}$')
ax[0].set_xlim([0,1.1])
ax[0].set_ylim([0,15])
ax[0].set_title(r'a) $\zeta=5$', loc='left')
ax[0].legend(loc='upper left', frameon=False)
ax[0].set_ylabel(r'Density')
ax[0].set_box_aspect(0.75/golden_ratio)

ax[1].hist(eta_ts[:,5], density=True, bins=5, label=r'$\eta_{TS}$')
ax[1].hist(eta_fs[:,5], density=True, bins=5, label=r'$\eta_{FS}$')
ax[1].set_xlim([0,1.1])
ax[1].set_ylim([0,15])
ax[1].set_title(r'b) $\zeta=25$', loc='left')
ax[1].legend(loc='upper left', frameon=False)
ax[1].set_box_aspect(0.75/golden_ratio)

#plt.tight_layout()

plt.savefig('KirbyFig3.png', bbox_inches='tight')
plt.savefig('fig3.pdf', bbox_inches='tight')
