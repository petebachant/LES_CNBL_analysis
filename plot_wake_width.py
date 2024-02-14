"""Plot wake recovery
in wind farm LES
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp
from scipy import stats
from scipy.optimize import curve_fit

plt.style.use("plots/style.mplstyle")

#load csv file to store results
loss_factors = np.genfromtxt('loss_factors.csv', delimiter=',', dtype=None, names=True, encoding=None)

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

#define x, y, z coordinates
x = 31.25*np.arange(1600)
y = 21.74*np.arange(1380)

#create meshgrid
xg, yg ,zg = np.meshgrid(x, y, z, indexing='ij', sparse=True)

for case_no in range(31,40):

    case_id = loss_factors[case_no][0]

    #load u data
    f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_main_first_order.h5', 'r')
    u = f['u']
    v = f['v']

    #load auxiliary data
    aux = h5py.File(f'/mnt/d/LES_data/{case_id}/aux_files.h5', 'r')
    yaw = aux['yaw']
    time = aux['time']
    yaw = np.mean(yaw[time[:]>75600,:],axis=0)

    #load precursor data
    f = h5py.File(f'/mnt/d/LES_data/{case_id}/stat_precursor_first_order.h5', 'r')
    u_precursor = f['u']
    u_prec_profile = np.mean(u_precursor[:,:,:100],axis=(0,1))
    interp_u_prec = sp.interp1d(1000*z[:100], u_prec_profile)
    #hub height precursor u velocity
    u_prec_hubh = interp_u_prec(119)

    #create interpolating function for gridded data
    print('Begin interpolation')
    interp_u = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), u[544:1120,400:1050,:100])
    interp_v = sp.RegularGridInterpolator((x[544:1120], y[400:1050], 1000*z[:100]), v[544:1120,400:1050,:100])
    print('Interpolation finished')

    #x position of turbine no.0
    x_pos_turb = 18e3
    #y position of turbine no.0
    y_pos_turb = 10.2975e3

    #function to fit to wake deficits
    def fit_func(z,a,b,c):
        return a*stats.norm.pdf(z,c,b*198)

    wake_distance = np.linspace(2,9,8)
    wake_span = np.linspace(-2*198, 2*198, 80)
    wake_zslice = np.zeros((10,8,100))
    wake_yslice = np.zeros((10,8,80))
    #array to store wake widths
    sigma = np.zeros((14, 8))
    wake_growth_rate = np.zeros(14)

    #define colormap
    cmap1 = plt.get_cmap('viridis', 8)
    cmap2 = plt.get_cmap('viridis', 14)

    #loop over turbine rows
    for k in range(2,16):

        #loop over x positions
        for i, distance in enumerate(wake_distance):

            #loop over turbine column
            for j in range(10):

                        #loop over vertical column
                        for z_index in range(100):

                            x_pos = x_pos_turb + distance*198*np.cos(np.pi*yaw[j+k*10]/180) + 5*198*k
                            #staggered alternate rows
                            if k%2 == 0:
                                y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j+k*10]/180) + 5*198*j
                            else:
                                y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j+k*10]/180) + 5*198*j + 2.5*198

                            pos = np.array([x_pos, y_pos, 1000*z[z_index]])
                            u_min = interp_u(pos)
                            v_min = interp_v(pos)

                            wake_zslice[j, i, z_index] = u_min*np.cos(np.pi*yaw[j+k*10]/180) + v_min*np.sin(np.pi*yaw[j+k*10]/180)

                        #loop across spanwise position
                        for y_index in range(80):

                            x_pos = x_pos_turb + distance*198*np.cos(np.pi*yaw[j+k*10]/180) + 5*198*k - \
                                wake_span[y_index]*np.sin(np.pi*yaw[j+k*10]/180)
                            #staggered alternate rows
                            if k%2 == 0:
                                y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j+k*10]/180) + 5*198*j + \
                                wake_span[y_index]*np.cos(np.pi*yaw[j+k*10]/180)
                            else:
                                y_pos = y_pos_turb + distance*198*np.sin(np.pi*yaw[j+k*10]/180) + 5*198*j + 2.5*198 +\
                                wake_span[y_index]*np.cos(np.pi*yaw[j+k*10]/180)

                            pos = np.array([x_pos, y_pos, 119])
                            u_min = interp_u(pos)
                            v_min = interp_v(pos)

                            wake_yslice[j, i, y_index] = u_min*np.cos(np.pi*yaw[j+k*10]/180) + v_min*np.sin(np.pi*yaw[j+k*10]/180)

            #vertical wake deficit
            wake_zprofile = np.mean(wake_zslice, axis=0)
            plt.figure(2)
            plt.plot((u_prec_profile-wake_zprofile[i,:])/u_prec_hubh, 1000*z[:100], c=cmap1(i))
            plt.savefig(f'plots/{case_id}/wake_recovery_z{k}.png')

            #fit Gaussian function to wake deficit across turbine disk
            popt, pcov = curve_fit(fit_func, 1000*z[4:44], (u_prec_profile[4:44]-wake_zprofile[i,4:44])/u_prec_hubh)
            #wake width in z direction
            sigma_z = popt[1]
            plt.plot(fit_func(1000*z[4:44], *popt), 1000*z[4:44], c='k')
            plt.xlim([-0.1,0.8])
            plt.xlabel(r'$\frac{u_{\infty}-U}{u_{\infty,hubh}}$')
            plt.ylabel(r'$z$ (m)')
            plt.tight_layout()
            plt.savefig(f'plots/{case_id}/wake_recovery_z{k}.png')

            #spanwise wake deficit
            wake_yprofile = np.mean(wake_yslice, axis=0)
            plt.figure(3)
            plt.plot((u_prec_hubh-wake_yprofile[i,:])/u_prec_hubh, wake_span, c=cmap1(i))
            plt.savefig(f'plots/{case_id}/wake_recovery_y{k}.png')

            #fit Gaussian function to wake deficit across turbine disk
            popt, pcov = curve_fit(fit_func, wake_span[30:50], (u_prec_hubh-wake_yprofile[i,30:50])/u_prec_hubh)
            #wake width in y direction
            sigma_y = popt[1]
            plt.plot(fit_func(wake_span[30:50], *popt), wake_span[30:50], c='k')
            plt.xlim([-0.1,0.8])
            plt.xlabel(r'$\frac{u_{\infty}-U}{u_{\infty,hubh}}$')
            plt.ylabel(r'$y$ (m)')
            plt.tight_layout()
            plt.savefig(f'plots/{case_id}/wake_recovery_y{k}.png')

            sigma[k-2, i] = np.sqrt(sigma_y*sigma_z)
            plt.figure(4)
            plt.scatter(wake_distance[i], sigma[k-2, i], c=cmap2(k-2))
            plt.savefig(f'plots/{case_id}/wake_width.png')

        linreg = stats.linregress(wake_distance, sigma[k-2,:])
        print(linreg.slope)
        wake_growth_rate[k-2] = linreg.slope
        plt.figure(4)
        plt.ylim([0.4,1.4])
        plt.plot(wake_distance, linreg.slope*wake_distance + linreg.intercept, c=cmap2(k-2))
        plt.savefig(f'plots/{case_id}/wake_width.png')
        
        plt.close(2)
        plt.close(3)

    plt.figure(4)
    plt.title(r'$k^*=$'+f"{np.mean(wake_growth_rate):.3}")
    plt.ylabel(r'$\sigma/D$')
    plt.xlabel(r'$x/D$')
    plt.tight_layout()
    plt.savefig(f'plots/{case_id}/wake_width.png')
    plt.close(4)
