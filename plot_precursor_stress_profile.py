import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp

case_id = 'H1000-C5-G4'

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

#open shear stress file
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_second_order.h5', 'r')
uw = f['uw']
vw = f['vw']
#open sub-grid shear stress file
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_second_order_sgs.h5', 'r')
uw_sgs = f['uw_sgs']
vw_sgs = f['vw_sgs']

plt.plot(np.mean(uw[:,:,:100]+uw_sgs[:,:,:100],axis=(0,1)), 1000*z[:100], label='uw+uw_sgs')
plt.plot(np.mean(vw[:,:,:100]+vw_sgs[:,:,:100],axis=(0,1)), 1000*z[:100], label='vw+vw_sgs')
plt.legend()
plt.xlabel('Shear stress (m^2/s^2)')
plt.ylabel('z (m)')
plt.ylim([0,500])
plt.savefig('plots/precursor_shear_stress.png')