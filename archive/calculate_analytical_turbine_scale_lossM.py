"""Calculate turbine-scale power
loss using analytical zeta model
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp
import scipy.optimize as opt

case_id = 'H300-C5-G4'
u_star0 = 0.281

#interpolate stress data
stress_data = np.loadtxt('../../part4_turbines/LES_data/lanzilao_et_al_2023/h300_shear_stress.csv', delimiter=',')
stress = 0.0756*stress_data[:,0]
heights = 1000*stress_data[:,1]
f_str = sp.interp1d(heights, stress, fill_value="extrapolate")
direction_data = np.loadtxt('../../part4_turbines/LES_data/lanzilao_et_al_2023/h300_direction.csv', delimiter=',')
direction = (np.pi/180)*19.4*direction_data[:,0]
heights = 1000*direction_data[:,1]
#interpolate wind direction
f_dir = sp.interp1d(heights, direction, fill_value="extrapolate")


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

##############################################
# 1. Calculate U_F0
##############################################

#open precursor file
f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_first_order.h5', 'r')
u = f['u']
v = f['v']

#horziontally average
u = np.mean(u[:,:,:100], axis=(0,1))
v = np.mean(v[:,:,:100], axis=(0,1))

#interpolate
interp_u = sp.interp1d(1000*z[:100], 
    u, bounds_error=False, fill_value='extrapolate')
interp_v = sp.interp1d(1000*z[:100], 
    v, bounds_error=False, fill_value='extrapolate')

#calculate wind direction at turbine height
u_hubh = interp_u(119)
v_hubh = interp_v(119)
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

#################################
# 3. Farm variables
#################################
cf0 = u_star0**2/(0.5*u_f0**2)
tauw0 = f_str(0)*np.cos(f_dir(0))
tautop0 = f_str(2.5*119)*np.cos(f_dir(2.5*119))


#################################
# 4. Calculate C_{p,Nishino}
#################################

array_density = np.pi/(4*5*5)
ctstar = 0.88*1.107


def ndfm(beta):
    lhs = ctstar*(array_density/cf0)*beta**2 + beta**2

    rhs_top = 1 + (2.5*119*(1-beta**2))/(cf0*15.8e3) - tautop0/tauw0
    
    rhs_bottom = beta*(1 - tautop0/tauw0)
    
    return lhs - rhs_top/rhs_bottom

beta = opt.bisect(ndfm,1,0.3)
print(beta**3)