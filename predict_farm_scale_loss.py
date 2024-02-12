"""Predict turbine-scale and
farm-scale loss factors using equation A5
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
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

#load csv file to store results
loss_factors = np.genfromtxt('loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

#path to wind farm LES data
path = '/mnt/e/LES_data/'

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

for case_no in range(23,24):

    case_id = loss_factors[case_no][0]
    print(case_id)

    ##############################################
    # 1. Calculate U_F0
    ##############################################

    #open precursor file
    f = h5py.File(f'{path}{case_id}/stat_precursor_first_order.h5', 'r')
    u = f['u']
    v = f['v']

    #horziontally average
    u = np.mean(u[:,:,:100], axis=(0,1))
    v = np.mean(v[:,:,:100], axis=(0,1))

    #vertical grid - use cell centered points  
    with open(f'{path}zmesh','r') as file:       
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
    # 2. Calculate u_star0 from
    # precursor simulation
    #################################

    #open shear stress file
    f = h5py.File(f'{path}{case_id}/stat_precursor_second_order.h5', 'r')
    uw = f['uw']
    #open sub-grid shear stress file
    f = h5py.File(f'{path}{case_id}/stat_precursor_second_order_sgs.h5', 'r')
    uw_sgs = f['uw_sgs']

    uw_profile = np.mean(uw[:,:,:100]+uw_sgs[:,:,:100],axis=(0,1))
    interp_uw = sp.interp1d(1000*z[:100], 
    uw_profile, bounds_error=False, fill_value='extrapolate')

    #fit 2nd order polynomial to uw shear stress profile between z=20m and z=200m
    poly = PolynomialFeatures(degree=2, include_bias=False)
    x = 1000*z[np.logical_and(1000*z>20,1000*z<200)]
    y = uw_profile[np.logical_and(1000*z[:100]>20,1000*z[:100]<200)]
    poly_features = poly.fit_transform(x.reshape(-1, 1))
    poly_reg_model = LinearRegression()
    poly_reg_model.fit(poly_features, y)
    x_test = np.linspace(0,200,101)
    test_features = poly.fit_transform(x_test.reshape(-1, 1))
    y_test = poly_reg_model.predict(test_features)
    #extrapolate shear stress at surface
    tau_w0 = y_test[0]
    u_star0 = np.sqrt(np.abs(tau_w0))
    #interpolate shear stress at z = 2.5H_{hub}
    tau_t0 = interp_uw(h_f)
    #shear stress ratio tau_t0/tau_w0
    shear_ratio = tau_t0/tau_w0

    #################################
    # 3. Calculate C_{p,Nishino}
    #################################

    #turbine rotor area divided surface area per turbine
    cf0 = u_star0**2/(0.5*u_f0**2)
    #wind `extractability' factor
    zeta = 1.18 + (2.18*h_f)/(cf0*farm_length*(1-shear_ratio))

    def ndfm(beta):
        lhs = ctstar*(array_density/cf0)*beta**2 + beta**2

        rhs = 1 + zeta*(1-beta)

        return lhs - rhs

    beta = opt.bisect(ndfm,1,0.3)
    power_ratio_nishino = beta**3

    #################################
    # 4. Calculate turbine-scale and
    #farm-scale loss factors
    #################################

    #farm-scale loss factor (fsl)
    fsl = 1 - power_ratio_nishino

    print('FSL: ', fsl)
    loss_factors[case_no][5] = fsl
    np.savetxt('loss_factors.csv', loss_factors, delimiter=',', fmt="%s,%f,%f,%f,%f,%f", header=','.join(loss_factors.dtype.names))
