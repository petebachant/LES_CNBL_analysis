import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

case_id = 'H300-C2-G8'

#vertical grid - use cell centered points  
with open('/mnt/e/LES_data/zmesh','r') as file:       
    Nz_full     = int(float(file.readline()))   
    N_line = Nz_full+1
    line = N_line*[0]
    cnt = 0
    for lines in file:
        line[cnt]=lines.split()
        cnt+=1       
    z = np.array([float(line[k][0]) for k in range(int(Nz_full))])[1::2]

#open shear stress file
f = h5py.File(f'/mnt/e/LES_data/{case_id}/stat_precursor_second_order.h5', 'r')
uw = f['uw']
vw = f['vw']
#open sub-grid shear stress file
f = h5py.File(f'/mnt/e/LES_data/{case_id}/stat_precursor_second_order_sgs.h5', 'r')
uw_sgs = f['uw_sgs']
vw_sgs = f['vw_sgs']

uw_profile = np.mean(uw[:,:,:100]+uw_sgs[:,:,:100],axis=(0,1))
vw_profile = np.mean(vw[:,:,:100]+vw_sgs[:,:,:100],axis=(0,1))


interp_uw = sp.interp1d(1000*z[:100], 
uw_profile, bounds_error=False, fill_value='extrapolate')

poly = PolynomialFeatures(degree=2, include_bias=False)
x = 1000*z[np.logical_and(1000*z>20,1000*z<200)]
y = uw_profile[np.logical_and(1000*z[:100]>20,1000*z[:100]<200)]
poly_features = poly.fit_transform(x.reshape(-1, 1))
poly_reg_model = LinearRegression()
poly_reg_model.fit(poly_features, y)
x_test = np.linspace(0,200,101)
test_features = poly.fit_transform(x_test.reshape(-1, 1))
y_test = poly_reg_model.predict(test_features)
tau0 = y_test[0]
print(interp_uw(2.5*119))
print(tau0)

plt.plot(uw_profile, 1000*z[:100], label='uw+uw_sgs')
plt.plot(y_test, x_test, linestyle='--', c='k')
plt.plot(vw_profile, 1000*z[:100], label='vw+vw_sgs')
plt.legend()
plt.xlabel('Shear stress (m^2/s^2)')
plt.ylabel('z (m)')
plt.ylim([0,500])
plt.axvline(-0.552*0.275**2)
plt.axvline(-0.275**2)
plt.axhline(2.5*119)

plt.savefig('plots/precursor_shear_stress.png')


case_id = 'H300-C5-G1'

#vertical grid - use cell centered points  
with open('/mnt/e/LES_data/zmesh','r') as file:       
    Nz_full     = int(float(file.readline()))   
    N_line = Nz_full+1
    line = N_line*[0]
    cnt = 0
    for lines in file:
        line[cnt]=lines.split()
        cnt+=1       
    z = np.array([float(line[k][0]) for k in range(int(Nz_full))])[1::2]

#open shear stress file
f = h5py.File(f'/mnt/e/LES_data/{case_id}/stat_precursor_second_order.h5', 'r')
uw = f['uw']
vw = f['vw']
#open sub-grid shear stress file
f = h5py.File(f'/mnt/e/LES_data/{case_id}/stat_precursor_second_order_sgs.h5', 'r')
uw_sgs = f['uw_sgs']
vw_sgs = f['vw_sgs']

uw_profile = np.mean(uw[:,:,:100]+uw_sgs[:,:,:100],axis=(0,1))
vw_profile = np.mean(vw[:,:,:100]+vw_sgs[:,:,:100],axis=(0,1))


interp_uw = sp.interp1d(1000*z[:100], 
uw_profile, bounds_error=False, fill_value='extrapolate')

poly = PolynomialFeatures(degree=2, include_bias=False)
x = 1000*z[np.logical_and(1000*z>20,1000*z<200)]
y = uw_profile[np.logical_and(1000*z[:100]>20,1000*z[:100]<200)]
poly_features = poly.fit_transform(x.reshape(-1, 1))
poly_reg_model = LinearRegression()
poly_reg_model.fit(poly_features, y)
x_test = np.linspace(0,200,101)
test_features = poly.fit_transform(x_test.reshape(-1, 1))
y_test = poly_reg_model.predict(test_features)
tau0 = y_test[0]
print(interp_uw(2.5*119))
print(tau0)

plt.plot(uw_profile, 1000*z[:100], label='uw+uw_sgs')
plt.plot(y_test, x_test, linestyle='--', c='k')
plt.plot(vw_profile, 1000*z[:100], label='vw+vw_sgs')
plt.legend()
plt.xlabel('Shear stress (m^2/s^2)')
plt.ylabel('z (m)')
plt.ylim([0,500])
plt.axvline(-0.552*0.275**2)
plt.axvline(-0.275**2)
plt.axhline(2.5*119)

plt.savefig('plots/precursor_shear_stress.png')