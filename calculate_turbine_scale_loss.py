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

#dictionary for surface shear stress from precursor simulation
u_star0_dict = {'H1000-C5-G4': 0.275, 'H1000-C5-G4_aligned': 0.275,
                'H500-C5-G4': 0.277, 'H500-C5-G4_aligned': 0.277,
                'H500-C0-G0': 0.277, 'H300-C5-G4' : 0.281,
                'H300-C2-G1': 0.280, 'H300-C8-G1': 0.281}

#dictionary for single turbine power
P_infty_dict = {'H1000-C5-G4': 7.62e6, 'H1000-C5-G4_aligned': 7.62e6,
                'H500-C5-G4': 7.90e6, 'H500-C5-G4_aligned': 7.90e6,
                'H500-C0-G0': 7.90e6, 'H300-C5-G4' : 8.00e6,
                'H300-C2-G1': 8.00e6, 'H300-C8-G1': 8.00e6}

#arrays to store results
#farm scale loss factor
fsl = np.ones(4)
#turbine scale loss factor
tsl = np.ones(4)
#non-local efficiency
eta_nl = np.ones(4)
#wake efficinecy
eta_w = np.ones(4)

cases = ['H1000-C5-G4', 'H1000-C5-G4_aligned',
                'H500-C5-G4', 'H500-C5-G4_aligned']

for case_no, case_id in enumerate(cases):

    print(case_id)
    u_star0 = u_star0_dict[case_id]

    ##############################################
    # 1. Calculate M_hub from precursor simulation
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
    #calculate uncorrected power coefficient
    cp_ad_overpredict = cp_ad / (M_shapiro**3)

    #calculate P_Betz (per unit density)
    turbine_area = np.pi * 198**2 / 4
    P_betz = 0.5 * cp_ad_overpredict * turbine_area * M_hub**3

    ##############################################
    # 3. Calculate P_LES from LES
    ##############################################

    #calculate turbine power
    aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
    power = aux['power']
    time = aux['time']
    #average turbine power over last 1.5hrs of simulation
    P_les = np.mean(power[time[:]>75600,:])
    #first row turbine power
    P_1 = np.mean(power[time[:]>75600,:10])

    power_ratio_les = P_les / P_betz

    ##############################################
    # 4. Calculate U_F0
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
    ##############################################

    aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
    #calculate average yaw angle
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
    force_ave = np.mean(force_hubh[time[:]>75600,:])
    plt.plot([75600,81000],[force_ave,force_ave])
    plt.savefig('plots/turbine_force.png')
    plt.close()

    #define x, y, z coordinates
    x = 31.25*np.arange(1600)
    y = 21.74*np.arange(1380)

    #open velocity file
    f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_main_first_order.h5', 'r')
    u = f['u']
    v = f['v']

    #create interpolating function for gridded data
    print('Begin interpolation')
    interp_u = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    u[544:1120,400:1050,:100], bounds_error=False, fill_value=None)
    interp_v = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    v[544:1120,400:1050,:100], bounds_error=False, fill_value=None)
    print('Interpolation finished')

    #grid to extrapolate shear stress onto
    n_x = 500
    n_y = 500
    n_z = 100
    x_farm = np.linspace(17.4735e3,33.3135e3,n_x)
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

    yaw_mean_rad = np.pi*np.mean(yaw_mean)/180

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
    beta = u_f/u_f0

    M = force_ave/(5**2 * 198**2 * u_star0**2) + beta**2
    zeta = (M-1)/(1-beta)

    #################################
    # 7. Calculate C_{p,Nishino}
    #################################

    array_density = np.pi/(4*5*5)
    ctstar = 0.88 / (M_shapiro**2)
    cf0 = u_star0**2/(0.5*u_f0**2)

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

    #turbine-scale loss factor (tsl)
    tsl[case_no] = 1 - power_ratio_les/power_ratio_nishino

    print('FSL: ', fsl[case_no])
    print('TSL: ', tsl[case_no])

    #non local efficiency
    eta_nl[case_no] = P_1 / P_infty_dict[case_id]
    #wake efficiency
    eta_w[case_no] = P_les / P_1

    print('eta_nl: ', eta_nl[case_no])
    print('eta_w: ', eta_w[case_no])


#################################
# 9. Plot results
#################################
plt.style.use("plots/style.mplstyle")

fig, ax = plt.subplots(figsize=[6,4], dpi=300)

ax.bar(np.arange(4)-0.2, eta_w*eta_nl, width=0.2, label=r'$\eta_f$', color='k')
ax.bar(np.arange(4), eta_w, width=0.2, label=r'$\eta_w$')
ax.bar(np.arange(4)+0.2, eta_nl, width=0.2, label=r'$\eta_{nl}$')
plt.xticks(np.arange(4), [r'H1000-C5-G4', r'H1000-C5-G4_aligned', r'H500-C5-G4', r'H500-C5-G4_aligned'], fontsize=10, rotation='vertical')
ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5), ncols=1)
plt.ylim([0,1.15])
plt.xlim([-0.5,3.5])
plt.axvline(1.5, c='k')
plt.tight_layout()
plt.savefig('plots/wake_blockage_loss.png')
plt.close()


fig, ax = plt.subplots(figsize=[6,4], dpi=300)
ax.bar(np.arange(4)-0.2, (1-tsl)*(1-fsl), width=0.2, label=r'$\eta_f$', color='k')
ax.bar(np.arange(4), 1-tsl, width=0.2, label=r'$1-\Pi_T$')
ax.bar(np.arange(4)+0.2, 1-fsl, width=0.2, label=r'$1-\Pi_F$')
plt.xticks(np.arange(4), [r'H1000-C5-G4', r'H1000-C5-G4_aligned', r'H500-C5-G4', r'H500-C5-G4_aligned'], fontsize=10, rotation='vertical')
ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5), ncols=1)
plt.ylim([0,1.15])
plt.xlim([-0.5,3.5])
plt.axvline(1.5, c='k')
plt.tight_layout()
plt.savefig('plots/tsl_fsl.png')
plt.close()