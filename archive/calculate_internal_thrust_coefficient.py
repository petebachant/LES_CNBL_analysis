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


cases = ['H1000-C5-G4']#, 'H500-C0-G0',
                #'H300-C5-G4', 'H300-C8-G1', 'H300-C2-G1', 'H150-C5-G4']

for case_no, case_id in enumerate(cases):

    print(case_id)

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
    #forces in the direction of averge yaw angle
    force_hubh = force*np.cos((yaw-yaw_mean)*np.pi/180)
    #average turbine force over last 1.5hrs of simulation
    force_ave = np.mean(force_hubh[time[:]>75600,:], axis=0)

    #define x, y, z coordinates
    x = 31.25*np.arange(1600)
    y = 21.74*np.arange(1380)

    #open velocity file
    f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_main_first_order.h5', 'r')
    u = f['u']
    v = f['v']

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

    #create interpolating function for gridded data
    interp_u = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    u[544:1120,400:1050,:100], bounds_error=False, fill_value=None)
    interp_v = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), 
    v[544:1120,400:1050,:100], bounds_error=False, fill_value=None)

    #grid to extrapolate shear stress onto
    n_x = 500
    n_y = 500
    n_z = 100
    x_farm = np.linspace(17.505e3,33.345e3,n_x)
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

    rotor_area = np.pi*198**2 / 4

    ct_star_values = force_ave / (0.5 * u_f**2 * rotor_area)

    plt.plot(ct_star_values[5:160:10])

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
    plt.axhline(0.88/M_shapiro**2)
    plt.savefig(f'plots/{case_id}/ct_star.png')
    print(np.mean(ct_star_values))
