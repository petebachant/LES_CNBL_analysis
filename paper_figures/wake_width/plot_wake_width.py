import h5py
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as sp
from scipy import stats
from scipy.optimize import curve_fit

#path variable to change
path = '/mnt/e/LES_data/'

plt.style.use("../style.mplstyle")

textwidth = 7
golden_ratio = 1.61803
fig, ax = plt.subplots(ncols=2, figsize=[textwidth,textwidth/(2*golden_ratio)], dpi=300)

#vertical grid - use cell centered points  
with open(f'{path}zmesh','r') as file:       
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

for plot_no, case_id in enumerate(['H300-C2-G1','H300-C8-G1']):

    #load u data
    f = h5py.File(f'{path}{case_id}/stat_main_first_order.h5', 'r')
    u = f['u']
    v = f['v']

    #load auxiliary data
    aux = h5py.File(f'{path}{case_id}/aux_files.h5', 'r')
    yaw = aux['yaw']
    time = aux['time']
    yaw = np.mean(yaw[time[:]>75600,:],axis=0)

    #load precursor data
    f = h5py.File(f'{path}{case_id}/stat_precursor_first_order.h5', 'r')
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
    cmap2 = plt.get_cmap('plasma', 14)

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

            #fit Gaussian function to wake deficit across turbine disk
            popt, pcov = curve_fit(fit_func, 1000*z[4:44], (u_prec_profile[4:44]-wake_zprofile[i,4:44])/u_prec_hubh)
            #wake width in z direction
            sigma_z = popt[1]

            #spanwise wake deficit
            wake_yprofile = np.mean(wake_yslice, axis=0)

            #fit Gaussian function to wake deficit across turbine disk
            popt, pcov = curve_fit(fit_func, wake_span[30:50], (u_prec_hubh-wake_yprofile[i,30:50])/u_prec_hubh)
            #wake width in y direction
            sigma_y = popt[1]

            sigma[k-2, i] = np.sqrt(sigma_y*sigma_z)
            ax[plot_no].scatter(wake_distance[i], sigma[k-2, i], c=cmap2(k-2), marker='x')

        linreg = stats.linregress(wake_distance, sigma[k-2,:])
        print(linreg.slope)
        wake_growth_rate[k-2] = linreg.slope

    ax[plot_no].set_ylim([0.4,1.4])
    ax[plot_no].text(2.2,1.3,rf'$k^*={round(np.mean(wake_growth_rate),4)}$', ha='left', va='center')

ax[0].set_title(r'(A) H300-C2-G1 $\eta_w=50\%$', loc='left')
ax[1].set_title(r'(B) H300-C8-G1 $\eta_w=100\%$', loc='left')
ax[0].set_ylabel(r'$\sigma/D$')
ax[0].set_xlabel(r'$x/D$')
ax[1].set_xlabel(r'$x/D$')

plt.tight_layout()

sm = plt.cm.ScalarMappable(cmap=cmap2, norm=plt.Normalize(vmin=3, vmax=16))
cbar2 = fig.colorbar(sm, ax=ax, ticks=np.linspace(3.5,15.5,14))
cbar2.set_ticklabels(np.arange(3,17,1))
cbar2.set_label(r'Turbine row number')

plt.savefig('KirbyFig8.png', bbox_inches='tight')
plt.savefig('fig8.pdf', bbox_inches='tight')
