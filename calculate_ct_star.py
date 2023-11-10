"""Calculate internal turbine thurst coefficient
for a wind farm large-eddy simulation
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np

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

#calculate the average turbine orientation
aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
yaw = aux['yaw']
time = aux['time']
#mean yaw angle in degrees
yaw_max = np.mean(yaw[time[:]>75600],axis=0)
yaw_max = np.max(yaw_max)
print("Maximum yaw angle is ", yaw_max, "degrees")
yaw_mean = np.mean(yaw[time[:]>75600])
print(yaw_mean)

#check farm area is correct
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_main_first_order.h5', 'r')
u = f['u']
v = f['v']
plt.close()
plt.pcolormesh(u[559:1066,462:918,24])
plt.colorbar()
plt.savefig('plots/farm_area.png')

#calculate CV-averaged quantities
u_ave = 59*np.mean(u[559:1066,462:918,:59]) + 0.5*np.mean(u[559:1066,462:918,59])
u_ave = u_ave/59.5
print(u_ave)
v_ave = 59*np.mean(v[559:1066,462:918,:59]) + 0.5*np.mean(v[559:1066,462:918,59])
v_ave = v_ave/59.5
print(v_ave)

plt.close()
u_profile = np.mean(u[559:1066,462:918,:60], axis=(0,1))
plt.plot(u_profile, 1000*z[:60])
plt.axvline(u_ave)
plt.axhline(119)
plt.savefig('plots/u_profile.png')

#calculate U_F
u_f = u_ave*np.cos(np.pi*yaw_mean/180) + v_ave*np.sin(np.pi*yaw_mean/180)
print(u_f)

#calculate turbine force in direction of angle turbine orientation
yaw_diff = yaw - yaw_mean
force = aux['force']
force_component = force*np.cos(np.pi*yaw_diff/180)
force_ave = np.mean(force_component[time[:]>75600,:])
print(force_ave)

#calculate internal turbine thrust coefficient
turbine_area = (np.pi*198**2)/4
ct_star = force_ave / (0.5*turbine_area*u_f**2)
print(ct_star)