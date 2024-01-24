import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

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

for case_id in ['H500-C5-G4', 'H500-C2-G1']:

    #open velocity file file
    f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_second_order.h5', 'r')
    uw = f['uw']
    vw = f['vw']
    uw = np.mean(uw[:,:,:100], axis=(0,1))
    vw = np.mean(vw[:,:,:100], axis=(0,1))
    speed = np.sqrt(uw**2+vw**2)

    plt.plot(speed, 1000*z[:100], label=case_id)
    #plt.xlabel('Velocity (m/s)')
    plt.legend()
    #plt.ylabel('z (m)')
    #plt.ylim([20,218])
    #plt.xlim([8,10])
    plt.savefig('plots/precursor_stress.png')