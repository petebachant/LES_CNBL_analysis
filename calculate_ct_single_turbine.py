"""Calculate turbine thrust
coefficient for large-eddy simulations
of a single turbine
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

for h in [150]:

    case_id = f'H{h}-C5-G4_st'
    print(case_id)

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

    #plot u and v profile from precursor simulation
    f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_first_order.h5', 'r')
    u = f['u']
    u_profile = np.mean(u[:,:,:60],axis=(0,1))
    v = f['v']
    v_profile = np.mean(v[:,:,:60],axis=(0,1))
    #plt.plot(u_profile, 1000*z[:60], c='b')
    #plt.plot(v_profile, 1000*z[:60], c='r')
    #plt.savefig('plots/precursor_profile.png')

    speed = np.sqrt(u_profile**2+v_profile**2)
    #angle in degrees!
    angle = 180*np.arctan(v_profile/u_profile)/np.pi
    #plt.close()
    #plt.plot(speed, 1000*z[:60], c='b')
    #plt.plot(angle, 1000*z[:60], c='r')
    #plt.savefig('plots/precursor_speed.png')

    #interpolate to find velocity at hub height
    f_speed = sp.interp1d(1000*z[:60], speed, fill_value="extrapolate")
    print(f_speed(119))
    u_infty = f_speed(119)
    f_angle = sp.interp1d(1000*z[:60], angle, fill_value="extrapolate")

    #calculate turbine force
    aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
    print(list(aux.keys()))
    force = aux['force']
    power = aux['power']
    time = aux['time']
    plt.figure(1)
    plt.plot(time[:],force[:])
    plt.axvline(75600)
    #plt.ylim([1e6,1.5e6])
    plt.savefig('plots/turbine_force.png')
    force_ave = np.mean(force[time[:]>75600,:])
    print(force_ave)
    power_ave = np.mean(power[time[:]>75600,:])
    print(power_ave)

    turbine_area = (np.pi*198**2)/4
    ct = force_ave / (0.5*turbine_area*u_infty**2)
    print(ct)

    cp = power_ave / (0.5*turbine_area*u_infty**3)
    print(cp)