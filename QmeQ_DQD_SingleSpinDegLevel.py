# -*- coding: utf-8 -*-
"""
DQD with a single spin degenerate GS in each QD
Model incl. electron-phonon coupling, implemented as in 
Goldozian et al. Eur. Phys. J. Spec. Top. 2019
Bias is applied to the source (left) lead only while the drain side remains grounded. 
Electrons travelling from drain to source contribute to a positive current.
"""

import qmeq
from qmeq import  Builder
from qmeq.specfunc import Func
from scipy.constants import e, k, hbar
import numpy as np
import matplotlib.pyplot as plt


## Definition of system parameters

UL = 10  # Charging energy QD L in meV
UR = 10  # Charging energy QD R in meV
Un = 2  # Interdot Coulomb coupling energy in meV
omega = 0.05  # Interdot tunnel coupling in meV
gammaL = 100e6  # Tunnel coupling left QD to left reservoir in Hz
gammaR = gammaL  # Tunnel coupling right QD to right reservoir in Hz    
tempL = 1000  # Temperature left electron reservoir in mK
tempR = 1000  # Temperature right electron reservoir in mK
tempPh = 1000  # Temperature phonon bath in mK
bias = 2  # External voltage bias in mV


## System definition:

# Define DQD levels:

nsingle = 4  # Total number of levels on DQD

eL = 0  # Energy of ground state left QD
eR = 0  # Energy of ground state right QD

# hsingle defines energies of the single levels and tunneling between levels
hsingle = {(0,0): eL, (1,1): eL, (2,2): eR, (3,3): eR,
           (0,2): omega, (1,3): omega}

# Define leads:

nleads = 4  # Total number of leads, 4 incl. both spins

# Rescale tunnel couplings to tunnel rates:
tl, tr = np.sqrt((1000*(hbar*gammaL)/e)/(2*np.pi)), np.sqrt((1000*(hbar*gammaR)/e)/(2*np.pi))

mulst = {0: -bias, 1: -bias, 2: 0, 3: 0} # Chemical potentials of leads
tlst = {0: tempL*k/e , 1: tempL*k/e , 2: tempR*k/e , 3: tempR*k/e } # Lead temperatures

# Tunneling from leads to levels index: (lead, level)
tleads = {(0,0): tl, (1,1): tl, (2,2): tr, (3,3): tr} 

# Define interactions by providing Coulomb matrix (no exchange itneractions considered:)
coulomb = {(0,1,1,0): UL, (2,3,3,2): UR,
           (0,2,2,0): Un, (0,3,3,0): Un, (1,2,2,1): Un, (1,3,3,1): Un}

# Add electron-phonon coupling:

nbaths = 1  # Total number of phonon baths
dband_ph = {0:[1e-8, 100]}  # Phonon bandwidth
tlst_ph = {0: tempPh*k/e}  # Phonon bath temperature

# Define phonon spectral density: 
# Use spectral density for lowest phonon mode in InAs nanowires, taken from
# GoldozianEPJST2019 and WeberPRL2010
class JFunc(Func): # Phonon spectral density function
    def eval(self, E):
         return 3.8804*10**(-4)*E  # J(E) from GoldozianEPJST2019

Jfunc_ph = JFunc() # Define phonon spectral density

# DQD parameters in nm for phonon coupling matrix elements, see Goldozian EPJST 2019   
d=50  # Center to center distance
a=5  # Gaussian radius for wavefunctions
q=np.pi/(3*d)
alpha=q*d*1j  # Shifting exponent for QD R matrix elements by QD distance

# Define phonon coupling of states; notation: (bath,n,m) [inverse (bath,m,n) required]
zz=np.exp(alpha/2)*np.exp(-(d**2)/(4*a**2))  # ynm between GSL and GSR
yelph = {(0,0,2): zz, # GS L up -> GS R up
         (0,2,0): zz, # GS R up -> GS L up
         (0,1,3): zz, # GS L down -> GS R down
         (0,3,1): zz, # GS R down -> GS L down
         (0,0,0): 1,
         (0,1,1): 1,
         (0,2,2): np.exp(alpha),
         (0,3,3): np.exp(alpha)
         }

## Create system with QmeQ:
system = Builder.elph(nsingle, hsingle, coulomb,
                 nleads, tleads, mulst, tlst, 100, nbaths, yelph, tlst_ph,
                 dband_ph, bath_func=[Jfunc_ph],
                 kerntype = 'Pauli')
# Note: For low temperatures (below 1 K) the Pauli approach can fail. This can be solved by using
#       kerntype = 'Lindblad' instead but calculations will be significantly slower.


## Calculate and plot charge stability diagram

N = 100 # number of datapoints in stability diagram
# Energy level shift on QD L/R, convention: eL = mu_D - mu_QD, where mu_D is the electro-chemical
# potential of the drain lead and mu_QD the electro-chemical potential of the QD levels
# eL/R correspond to e*lever_arm*V_gL/R with the sign according to the above convention
eL = np.linspace(-5,20,N)  
eR = np.linspace(-5,20,N)

I = np.zeros([N,N]) # Create empty array for currents

for i,vL in enumerate(eL):  # Loop over left/right energy level shift
    for j,vR in enumerate(eR):
        
        # update hsingle: shift all levels  downward    
        hsingle = {(0,0): -vL, (1,1): -vL, (2,2): -vR, (3,3): -vR, 
                   (0,2): omega, (1,3): omega}
        
        # Update position of potentials:
        mulst = {0: -bias, 1: -bias, 2: 0, 3: 0}
        
        system.change(hsingle=hsingle, mulst = mulst)  # Update system
        system.solve()  # Solve updated system
        
        # Sum up current contributions from left and right lead, scale to pA
        I[j,i] = -(system.current[0] + system.current[1])*1.E9*e**2/hbar
    

# Plot charge stbility diagram:

# Pick appropriate colormap for voltage and thermally biased calculations: 
# red = negative currents, blue = positive currents, white = 0
I_abs_max = np.amax(abs(I))  # Get maximum absolute current to ensure white = 0 pA in colormap
plt.pcolormesh(eL, eR ,I, cmap='RdBu', vmin=-I_abs_max, vmax=I_abs_max)  # Plot results
cbar = plt.colorbar()
# Set axis labels
cbar.set_label('I (pA)')
plt.ylabel(r'e$\alpha_\mathrm{R}$V$_{\mathrm{R}}$ (meV)')
plt.xlabel(r'e$\alpha_\mathrm{L}$V$_{\mathrm{L}}$ (meV)')
plt.show()
    