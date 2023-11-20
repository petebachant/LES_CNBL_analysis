"""Calculate turbine power
coefficient for large-eddy simulations
of a single turbine
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

#calculate power coefficient from actuator disc theory
ct_prime = 1.9417
#cp_ad - power coefficient according to actuator disc theory
cp_ad = 64*ct_prime / (4 + ct_prime)**3
print(cp_ad)

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
M = delta_r/turbine_radius
M = M / np.sqrt(3*np.pi)
M = M * ct_prime / 4
M = M + 1
M = M**(-1)
#calculate uncorrected power coefficient
cp_ad_overpredict = cp_ad / (M**3)
print(cp_ad_overpredict)

#array to store power coefficient from LES
cp_les = np.zeros(4)

#loop over different boundary layer heights
for i, h_bl in enumerate([1000, 500, 300, 150]):

    case_id = f'H{h_bl}-C5-G4_st'

    #vertical grid - use cell centered points
    #change file path below!
    with open('/mnt/d/LES_data/zmesh','r') as file:       
        Nz_full     = int(float(file.readline()))   
        N_line = Nz_full+1
        line = N_line*[0]
        cnt = 0
        for lines in file:
            line[cnt]=lines.split()
            cnt+=1       
        z = np.array([float(line[k][0]) for k in range(int(Nz_full))])[1::2]

    #u and v profile from precursor simulation
    #change file path below!
    f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_first_order.h5', 'r')
    u = f['u']
    u_profile = np.mean(u[:,:,:60],axis=(0,1))
    v = f['v']
    v_profile = np.mean(v[:,:,:60],axis=(0,1))

    #calculate velocity magnitude at turbine hub height
    speed = np.sqrt(u_profile**2+v_profile**2)
    #interpolate to find velocity at hub height
    f_speed = sp.interp1d(1000*z[:60], speed, fill_value="extrapolate")
    #reference velocity for power coefficient
    u_infty = f_speed(119)

    #plot vertical velocity profile to check calculation of u_infty
    plt.plot(speed, 1000*z[:60])
    plt.axhline(119)
    plt.axvline(u_infty)
    plt.xlabel('Velocity magnitude (m/s)')
    plt.ylabel('z (m)')
    plt.savefig(f'plots/{case_id}/u_infty.png')
    plt.close()

    #calculate turbine power
    #change file path below!
    aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
    power = aux['power']
    time = aux['time']
    #average turbine power over last 1.5hrs of simulation
    power_ave = np.mean(power[time[:]>75600,:])

    #calculate measured power coefficient from LES
    turbine_area = (np.pi*198**2)/4
    cp_les[i] = power_ave / (0.5*turbine_area*u_infty**3)

    #check convergence of turbine power
    plt.plot(time[:], power[:])
    plt.xlabel('Time (s)')
    plt.ylabel('Turbine power per unit density (m^5/s^3)')
    plt.axvline(75600)
    plt.savefig(f'plots/{case_id}/turbine_power.png')
    plt.close()

    #vary averaging period for turbine power
    #array to store results
    power_ave_period = np.zeros(1800)
    for j in range(1800):
        time_indices = [x for x in range(-(j+1),0)]
        power_ave_period[j] = np.mean(power[time_indices,:])
    #plot turbine power against averaging period
    plt.plot(5*np.arange(1800)+5, power_ave_period)
    plt.axvline(5400)
    plt.xlabel('Averaging period (s)')
    plt.ylabel('Turbine power per unit density (m^5/s^3)')
    plt.savefig(f'plots/{case_id}/turbine_power_averaging_period.png')
    plt.close()


#plot power coefficients for the different cases
plt.scatter(range(4), cp_les)
plt.axhline(cp_ad)
plt.axhline(cp_ad_overpredict)
plt.xticks(range(4), ['H1000-C5-G4_st', 'H500-C5-G4_st', 'H300-C5-G4_st', 'H150-C5-G4_st'])
plt.ylabel('Turbine power coefficient')
plt.text(0, cp_ad, 'AD theory', va='bottom', ha='left')
plt.text(3, cp_ad_overpredict-0.002, 'AD theory with overprediction (Shapiro et. al. 2019)', va='top', ha='right')
plt.savefig('plots/power_ceofficient.png')

