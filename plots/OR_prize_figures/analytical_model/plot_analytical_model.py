import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpl


plt.style.use("../style.mplstyle")

cm = 1/2.54
textwidth = 15
golden_ratio = 1.61803
fig, ax = plt.subplots(figsize=[textwidth*cm,textwidth*cm/(2*1.1*golden_ratio)], dpi=300, layout='constrained')

#wu et.al. 2017
#r = 1 K/km
plt.scatter(0,0.640,marker='o',s=20, c='blue', label='Staggered farm LES')
plt.scatter(0,0.575,marker='o',s=20, c='red', label='Aligned farm LES')
plt.plot([0,0],[0.607,0.470], c='k', label='Analytical prediction', zorder=0)
#r = 5 K/km
plt.scatter(1,0.516,marker='o',s=20, c='blue')
plt.scatter(1,0.440,marker='o',s=20, c='red')
plt.plot([1,1],[0.543,0.426], c='k', zorder=0)

#allaerts et. al. 2017
#s1
plt.scatter(2,0.536,marker='o',s=20, c='red')
plt.plot([2,2],[0.398/0.562,0.301/0.562], c='k', zorder=0)
#s2
plt.scatter(3,0.462,marker='o',s=20, c='red')
plt.plot([3,3],[0.360/0.562,0.277/0.562], c='k', zorder=0)
#s4
plt.scatter(4,0.402,marker='o',s=20, c='red')
plt.plot([4,4],[0.295/0.562,0.232/0.562], c='k', zorder=0)

#lanzilao et. al. 2022
#CS & CA
plt.scatter(5,0.585,marker='o',s=20, c='blue')
plt.scatter(5,0.449,marker='o',s=20, c='red')
plt.plot([5,5],[0.554,0.433], c='k', zorder=0)
#NS
plt.scatter(6,0.570,marker='o',s=20, c='blue')
plt.plot([6,6],[0.554,0.433], c='k', zorder=0)

plt.ylim([0,0.75])
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.ylabel(r'$P/P_{\infty}$')
ax.set_xticks(range(7))
ax.set_xticklabels([r'$\Gamma1$',r'$\Gamma5$',r'$S1$',r'$S2$',r'$S4$',r'$CA\&CS$',r'$NS$'])

plt.text(0.5,-0.15,r'$\textit{Wu et. al. }$'+'\n'+r'$ 2017$', ha='center', va='top', ma='center')
plt.text(3,-0.15,r'$\textit{Allaerts et. al. }$'+'\n'+r'$ 2017$', ha='center', va='top', ma='center')
plt.text(5.5,-0.15,r'$\textit{Lanzilao et. al. }$'+'\n'+r'$ 2022$', ha='center', va='top', ma='center')

plt.axvline(1.5)
plt.axvline(4.5)

#plt.tight_layout()
plt.savefig('KirbyFig2.png', bbox_inches='tight')
plt.savefig('fig2.pdf', bbox_inches='tight')