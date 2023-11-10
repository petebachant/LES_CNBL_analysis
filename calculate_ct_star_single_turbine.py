"""Calculate `internal' turbine thrust
coefficient for large-eddy simulations
of a single turbine
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np

for h in [1000,500,300,150]:

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

    #calculate the average turbine orientation
    aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
    yaw = aux['yaw']
    time = aux['time']
    #mean yaw angle in degrees
    yaw_mean = np.mean(yaw[time[:]>75600])

    #check farm area is correct
    f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_main_first_order.h5', 'r')
    u = f['u']
    v = f['v']
    plt.close()
    plt.pcolormesh(u[:240,:,24])
    plt.colorbar()
    plt.axvline(230, c='blue')
    plt.savefig('plots/farm_area.png')

    #calculate CV-averaged quantities
    u_ave = 59*np.mean(u[:240,:,:59]) + 0.5*np.mean(u[:240,:,59])
    u_ave = u_ave/59.5
    print(u_ave)
    v_ave = 59*np.mean(v[:240,:,:59]) + 0.5*np.mean(v[:240,:,59])
    v_ave = v_ave/59.5

    #calculate U_F
    u_f = u_ave*np.cos(np.pi*yaw_mean/180) + v_ave*np.sin(np.pi*yaw_mean/180)
    print(u_f)

    #calculate turbine force
    aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
    force = aux['force']
    time = aux['time']
    force_ave = np.mean(force[time[:]>75600,:])
    print(force_ave)

    turbine_area = (np.pi*198**2)/4
    ct_star = force_ave / (0.5*turbine_area*u_f**2)
    print(ct_star)
