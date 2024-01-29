"""Predict turbine-scale and
farm-scale loss factors usig equation A5
in https://doi.org/10.1017/jfm.2023.844

See https://doi.org/10.1017/jfm.2022.979 
for information and definitions of turbine
-scale and farm-scale loss factors
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp
import scipy.optimize as opt
import matplotlib.pyplot as plt

#dictionary for surface shear stress from precursor simulation
u_star0_dict = {'H1000-C5-G4': 0.275, 'H1000-C5-G4_aligned': 0.275,
                'H500-C5-G4': 0.277, 'H500-C5-G4_aligned': 0.277,
                'H500-C0-G0': 0.277, 'H300-C5-G4' : 0.281,
                'H300-C2-G1': 0.280, 'H300-C8-G1': 0.281}

#dictionary for shear stress ratios (i.e. shear stress at 2.5H_hub / bottom shear stress)
#In the LES simulations H_hub is 119m
#these values are extracted from figure 3 from https://arxiv.org/abs/2306.08633
shear_ratio_dict = {'H1000-C5-G4': 0.552, 'H1000-C5-G4_aligned': 0.552,
                'H500-C5-G4': 0.385, 'H500-C5-G4_aligned': 0.385,
                'H500-C0-G0': 0.385, 'H300-C5-G4' : 0.0972,
                'H300-C2-G1': 0.0972, 'H300-C8-G1': 0.0972}

#wind farm variables

#lambda - array density
array_density = np.pi/(4*5*5)
#L - wind farm length in streamwise direction
farm_length = 15.84e3
#h_f - farm-layer height (defined as 2.5H_hub where H_hub is turbine hub height)
h_f = 2.5*119
#ctstar 'internal' turbine thurst coefficient
#thrust coefficient should be overpredicted due to
#the effect of the Gaussian filter length
#here we calculate the overpredicted power coefficient 
#of an actuator disc with ct_prime = 1.9417 according to
#Shapiro et. al. 2019
#calculate shapiro correction factor
#Gaussian filter length is yz direction is 32.61m
delta_r = 32.61
turbine_radius = 99
ct_prime = 1.9417
#using equation 26 of Shapiro et. al. 2019
M_shapiro = delta_r/turbine_radius
M_shapiro = M_shapiro / np.sqrt(3*np.pi)
M_shapiro = M_shapiro * ct_prime / 4
M_shapiro = M_shapiro + 1
M_shapiro = M_shapiro**(-1)
ctstar = 0.88 / (M_shapiro**2)

#arrays to store results
#farm scale loss factor
fsl = np.ones(4)
#turbine scale loss factor
tsl = np.zeros(4)

cases = ['H1000-C5-G4', 'H500-C5-G4',
                'H300-C8-G1', 'H300-C2-G1']

for case_no, case_id in enumerate(cases):

    print(case_id)
    u_star0 = u_star0_dict[case_id]

    ##############################################
    # 1. Calculate U_F0
    ##############################################

    #open precursor file
    f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_first_order.h5', 'r')
    u = f['u']
    v = f['v']

    #horziontally average
    u = np.mean(u[:,:,:100], axis=(0,1))
    v = np.mean(v[:,:,:100], axis=(0,1))

    #vertical grid - use cell centered points  
    with open('/mnt/d/LES_data/zmesh','r') as file:       
        Nz_full     = int(float(file.readline()))   
        N_line = Nz_full+1
        line = N_line*[0]
        cnt = 0
        for lines in file:
            line[cnt]=lines.split()
            cnt+=1       
        z = np.array([float(line[k][0]) for k in range(int(Nz_full))])[1::2]

    #interpolate
    interp_u = sp.interp1d(1000*z[:100], 
    u, bounds_error=False, fill_value='extrapolate')
    interp_v = sp.interp1d(1000*z[:100], 
    v, bounds_error=False, fill_value='extrapolate')

    #calculate wind speed at turbine hub height
    u_hubh = interp_u(119)
    v_hubh = interp_v(119)
    M_hub = np.sqrt(u_hubh**2+v_hubh**2)

    #calculate hub height wind direction
    angle_hubh = np.arctan(v_hubh/u_hubh)

    #number of vertical levels for intergration
    n_z = 100
    u_farm_layer = interp_u(np.linspace(0,2.5*119,n_z))
    v_farm_layer = interp_v(np.linspace(0,2.5*119,n_z))
    u_f0 = np.mean(u_farm_layer)*np.cos(angle_hubh) + np.mean(v_farm_layer)*np.sin(angle_hubh)

    #################################
    # 7. Calculate C_{p,Nishino}
    #################################

    array_density = np.pi/(4*5*5)
    cf0 = u_star0**2/(0.5*u_f0**2)
    zeta = 1.18 + (2.18*h_f)/(cf0*farm_length*(1-shear_ratio_dict[case_id]))

    def ndfm(beta):
        lhs = ctstar*(array_density/cf0)*beta**2 + beta**2

        rhs = 1 + zeta*(1-beta)

        return lhs - rhs

    beta = opt.bisect(ndfm,1,0.3)
    power_ratio_nishino = beta**3

    #################################
    # 8. Calculate turbine-scale and
    #farm-scale loss factors
    #################################

    #farm-scale loss factor (fsl)
    fsl[case_no] = 1 - power_ratio_nishino

    print('FSL: ', fsl[case_no])
    print('TSL: ', tsl[case_no])


#################################
# 9. Plot results
#################################
plt.style.use("plots/style.mplstyle")

fig, ax = plt.subplots(figsize=[6,4], dpi=300)
ax.bar(np.arange(4)-0.2, (1-tsl)*(1-fsl), width=0.2, label=r'$\eta_f$', color='k')
ax.bar(np.arange(4), 1-tsl, width=0.2, label=r'$1-\Pi_T$')
ax.bar(np.arange(4)+0.2, 1-fsl, width=0.2, label=r'$1-\Pi_F$')
plt.xticks(np.arange(4), cases, fontsize=10, rotation='vertical')
ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5), ncols=1)
plt.ylim([0,1.15])
plt.xlim([-0.5,3.5])
#plt.axvline(1.5, c='k')
plt.tight_layout()
plt.savefig('plots/tsl_fsl.png')
plt.close()