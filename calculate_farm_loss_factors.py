"""Calculate turbine-scale and
farm-scale loss factors for wind farm LES

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

#path variable to change!
path = '/mnt/c/Users/trin3517/Documents/PhD/Year 4/Research plots and presentations/LES_data/'

#load LES data from precursor and single turbine simulations
LES_data = np.genfromtxt('LES_data.csv', delimiter=',', dtype=None, names=True, encoding=None)

#load csv file to store results
loss_factors = np.genfromtxt('loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

for case_no in range(43, 45):

    case_id = LES_data[case_no][0]
    u_star0 = LES_data[case_no][1]

    ##############################################
    # 1. Calculate M_hub from precursor simulation
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

    #interpolate precursor velocity profiles
    interp_u = sp.interp1d(1000*z[:100], 
    u, bounds_error=False, fill_value='extrapolate')
    interp_v = sp.interp1d(1000*z[:100], 
    v, bounds_error=False, fill_value='extrapolate')

    #calculate wind speed at turbine hub height
    u_hubh = interp_u(119)
    v_hubh = interp_v(119)
    M_hub = np.sqrt(u_hubh**2+v_hubh**2)

    ##############################################
    # 2. Calculate P_Betz using actuator disc theory
    ##############################################

    #calculate power coefficient from actuator disc theory
    ct_prime = 1.9417
    #cp_ad - power coefficient according to actuator disc theory
    cp_ad = 64*ct_prime / (4 + ct_prime)**3

    #power coefficient should be overpredicted due to
    #the effect of the Gaussian filter length
    #here we calculate the overpredicted power coefficient 
    #of an actuator disc with ct_prime = 1.9417 according to
    #Shapiro et. al. 2019

    #calculate shapiro correction factor
    #Gaussian filter length is yz direction is 32.61m
    delta_r = 32.61
    turbine_radius = 99
    #using equation 26 of Shapiro et. al. 2019
    M_shapiro = delta_r/turbine_radius
    M_shapiro = M_shapiro / np.sqrt(3*np.pi)
    M_shapiro = M_shapiro * ct_prime / 4
    M_shapiro = M_shapiro + 1
    M_shapiro = M_shapiro**(-1)
    #calculate power coefficient of LES actuator discs
    cp_ad_overpredict = cp_ad / (M_shapiro**3)

    #calculate P_Betz (per unit air density)
    #i.e. power of single isolated actuator disc
    #note that this is different from P_{\infty} from single turbine LES
    turbine_area = np.pi * 198**2 / 4
    P_betz = 0.5 * cp_ad_overpredict * turbine_area * M_hub**3

    ##############################################
    # 3. Calculate P_LES from LES
    ##############################################

    #calculate turbine power
    aux = h5py.File(f'{path}{case_id}/aux_files.h5', 'r')
    power = aux['power']
    time = aux['time']
    #average turbine power over last 1.5hrs of simulation
    P_les = np.mean(power[time[:]>75600,:])
    #first row turbine power
    #check whether case has normal or double spacing
    if case_id[11:] == 'double_spacing':
        P_1 = np.mean(power[time[:]>75600,:5])
    else:
        P_1 = np.mean(power[time[:]>75600,:10])

    power_ratio_les = P_les / P_betz

    ##############################################
    # 4. Calculate U_F0
    # i.e. calculate velocity averaged between the
    # surface and 2.5H_hub (turbine hub height 119m)
    # in the direction of the hub height velocity
    # from the precursor simulation
    ##############################################

    #calculate hub height wind direction
    angle_hubh = np.arctan(v_hubh/u_hubh)

    #number of vertical levels for intergration
    n_z = 100
    u_farm_layer = interp_u(np.linspace(0,2.5*119,n_z))
    v_farm_layer = interp_v(np.linspace(0,2.5*119,n_z))
    u_f0 = np.mean(u_farm_layer)*np.cos(angle_hubh) + np.mean(v_farm_layer)*np.sin(angle_hubh)

    plt.plot(u_farm_layer, np.linspace(0,2.5*119,n_z))
    plt.plot(v_farm_layer, np.linspace(0,2.5*119,n_z))
    plt.ylim([0,2.5*119])
    plt.axvline(u_f0)
    plt.savefig('plots/vertical_velocity_profiles.png')
    plt.close()

    #check convergence of u_f0 calculation with vertical levels
    while False:
        n_z_values = np.linspace(10,500,10)
        u_f0_convergence = np.zeros(10)
        for i, n_z in enumerate(n_z_values):
            print(n_z)
            n_z = int(n_z)
            u_farm_layer = interp_u(np.linspace(0,2.5*119,n_z))
            v_farm_layer = interp_v(np.linspace(0,2.5*119,n_z))
            u_f0_convergence[i] = np.mean(u_farm_layer)*np.cos(angle_hubh) + np.mean(v_farm_layer)*np.sin(angle_hubh)
        plt.plot(n_z_values, u_f0_convergence)
        plt.ylim([0,10])
        plt.savefig('plots/u_f0_convergence.png')
        plt.close()

    ##############################################
    # 5. Calculate U_F
    # i.e. calculate velocity averaged between the
    # surface and 2.5H_hub (turbine hub height 119m)
    # in the direction of the hub height velocity
    # from the wind farm LES 
    ##############################################

    #calculate average turbine yaw angle
    #yaw in degrees
    yaw = aux['yaw']
    time = aux['time']
    yaw_mean = np.mean(yaw[time[:]>75600,:],axis=0)

    #calculate turbine force
    force = aux['force']
    plt.plot(time[:], np.mean(force[:,:],axis=1))
    #forces in the direction of averge yaw angle
    force_hubh = force*np.cos((yaw-yaw_mean)*np.pi/180)
    plt.plot(time[:], np.mean(force_hubh[:,:],axis=1))
    #average turbine force over last 1.5hrs of simulation
    print(np.shape(force_hubh[:,:]))
    force_ave = np.mean(force_hubh[time[:]>75600,:])
    plt.plot([75600,81000],[force_ave,force_ave])
    plt.savefig('plots/turbine_force.png')
    plt.close()

    #define x, y, z coordinates
    x = 31.25*np.arange(1600)
    y = 21.74*np.arange(1380)

    #open velocity file
    f = h5py.File(f'{path}{case_id}/stat_main_first_order.h5', 'r')
    u = f['u']
    v = f['v']
    p = f['p']

    #create interpolating function for gridded data
    interp_u = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    u[544:1120,400:1050,:100], bounds_error=False, fill_value=None)
    interp_v = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    v[544:1120,400:1050,:100], bounds_error=False, fill_value=None)
    interp_p = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[15:30]), 
    p[544:1120,400:1050,15:30], bounds_error=False, fill_value=None)

    #grid to interpolate velocity onto
    n_x = 500
    n_y = 500
    n_z = 100
    #farm x coordinates (2.5D in front of first row and 2.5D behind final row)
    #check whether farm is full length or half length
    if case_id[11:] == 'half_farm':
        x_farm = np.linspace(17.505e3,25.425e3,n_x)
    else:
        x_farm = np.linspace(17.505e3,33.345e3,n_x)
    #farm y coordinates (1.25D left of first column and 1.25D right of final column)
    y_farm = np.linspace(10.050e3,19.950e3,n_y)
    z_farm = np.linspace(0,2.5*119,n_z)
    xg, yg, zg = np.meshgrid(x_farm, y_farm, z_farm)
    pos = np.zeros((n_x*n_y*n_z,3))
    pos[:,0] = xg.flatten()
    pos[:,1] = yg.flatten()
    pos[:,2] = zg.flatten()

    #calculate average u and v
    u = np.mean(interp_u(pos))
    v = np.mean(interp_v(pos))

    #calculate pressure 2.5D behind farm
    x_farm = 33.345e3
    y_farm = np.linspace(10.050e3,19.950e3,n_y)
    z_farm = 119
    xg, yg, zg = np.meshgrid(x_farm, y_farm, z_farm)
    pos = np.zeros((n_y,3))
    pos[:,0] = xg.flatten()
    pos[:,1] = yg.flatten()
    pos[:,2] = zg.flatten()
    p_rear = np.mean(interp_p(pos))
    #calculate pressure 2.5D in front farm
    x_farm = 17.505e3
    y_farm = np.linspace(10.050e3,19.950e3,n_y)
    z_farm = 119
    xg, yg, zg = np.meshgrid(x_farm, y_farm, z_farm)
    pos = np.zeros((n_y,3))
    pos[:,0] = xg.flatten()
    pos[:,1] = yg.flatten()
    pos[:,2] = zg.flatten()
    p_front = np.mean(interp_p(pos))
    p_farm = p_front - p_rear
    loss_factors[case_no][11] = p_farm

    #convert yaw angle to radians
    yaw_mean_rad = np.pi*np.mean(yaw_mean)/180

    #velocity in direction of mean turbine yaw direction
    u_f = u*np.cos(yaw_mean_rad)+v*np.sin(yaw_mean_rad)

    #check convergence of u_f calculation with horizontal discretisation
    while False:
        n_xy_values = np.linspace(10,500,10)
        u_f_convergence = np.zeros(10)
        for i, n_xy in enumerate(n_z_values):

            n_x = int(n_xy)
            n_y = int(n_xy)

            x_farm = np.linspace(17.4735e3,33.3135e3,n_x)
            y_farm = np.linspace(10.050e3,19.950e3,n_y)
            z_farm = np.linspace(0,2.5*119,n_z)
            xg, yg, zg = np.meshgrid(x_farm, y_farm, z_farm)

            pos = np.zeros((n_x*n_y*n_z,3))
            pos[:,0] = xg.flatten()
            pos[:,1] = yg.flatten()
            pos[:,2] = zg.flatten()

            u = np.mean(interp_u(pos))
            v = np.mean(interp_v(pos))

            yaw_mean_rad = np.pi*np.mean(yaw_mean)/180
            u_f_convergence[i] = u*np.cos(yaw_mean_rad)+v*np.sin(yaw_mean_rad)

        plt.plot(n_xy_values, u_f_convergence)
        plt.ylim([0,10])
        plt.savefig('plots/u_f_convergence.png')

    #################################
    # 6. Calculate M and zeta
    #################################

    #farm wind speed reduction factor beta
    beta = u_f/u_f0
    loss_factors[case_no][9] = beta

    #calculate `internal' turbine thrust coefficient
    ctstar = force_ave / (0.5 * turbine_area * u_f**2)
    loss_factors[case_no][7] = ctstar

    #Momentum availability factor M, calculated assuming gamma = 2.0
    #check whether turbine spacing is `normal' or double
    if case_id[11:] == 'double_spacing':
        M = force_ave/(10**2 * 198**2 * u_star0**2) + beta**2
    else:
        M = force_ave/(5**2 * 198**2 * u_star0**2) + beta**2
    loss_factors[case_no][8] = M
    #Wind `extratability' factor zeta`
    zeta = (M-1)/(1-beta)
    loss_factors[case_no][10] = zeta
    print('zeta: ',zeta)

    #################################
    # 7. Calculate C_{p,Nishino}
    #################################

    #array density is turbine rotor area / land area per turbine
    #check whether turbine spacing is `normal' or double
    if case_id[11:] == 'double_spacing':
        array_density = np.pi/(4*10*10)
    else:
        array_density = np.pi/(4*5*5)

    #'internal' turbine thrust coefficient
    ctstar = 0.88 / (M_shapiro**2)
    #natural surface friction coefficient
    cf0 = u_star0**2/(0.5*u_f0**2)
    print('cf0: ', cf0)

    #solve non-dimensional farm momentum (NDFM) equation for beta
    #see Nishino & Dunstan 2020 for more details https://doi.org/10.1017/jfm.2020.252
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
    fsl = 1 - power_ratio_nishino
    loss_factors[case_no][4] = fsl

    #turbine-scale loss factor (tsl)
    tsl = 1 - power_ratio_les/power_ratio_nishino
    loss_factors[case_no][3] = tsl

    print('FSL: ', loss_factors[case_no][4])
    print('TSL: ', loss_factors[case_no][3])

    #non local efficiency
    P_infty = LES_data[case_no][2]
    loss_factors[case_no][2] = P_1 / P_infty
    #wake efficiency
    loss_factors[case_no][1] = P_les / P_1

    print('eta_nl: ', loss_factors[case_no][2])
    print('eta_w: ', loss_factors[case_no][1])

    np.savetxt('loss_factors.csv', loss_factors, delimiter=',', fmt="%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f", header=','.join(loss_factors.dtype.names))
