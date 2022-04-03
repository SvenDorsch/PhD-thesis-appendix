# -*- coding: utf-8 -*-
"""
Model: QD with 3 spin degenerate levels. No exchange itneraction.
QmeQ is used to calculate the current through the system.
"""
import qmeq
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import e, k, hbar

## System parameters:
deltaE = 3  # Orbital spacing (meV)
Ec = 6  # Charging energy (meV)
gam = 100e6  #Tunnel coupling across both barriers (Hz)
tempL = 1000  # Temperature elft reservoir (mK)
tempR = 1000  # Temperature right reservoir (mK)
bias = 0  # External voltage bias


## System definition:
nsingle = 6  # Total nmumbers of levels on QD
e0 = 0  # Initial energy of ground state
# Supply single-particle energy spectrum
hsingle = {(0,0): e0, (1,1): e0, (2,2): e0+deltaE, (3,3): e0+deltaE,
           (4,4): e0+2*deltaE, (5,5): e0+2*deltaE}
nleads = 4  # Total number of leads
# Prepare bare tunnel rates for QmeQ
tl, tr = np.sqrt((1000*(hbar*gam)/e )/(2*np.pi)), np.sqrt((1000*(hbar*gam)/e )/(2*np.pi))
mulst = {0: -bias/2, 1: -bias/2, 2: bias/2, 3: bias/2}  # Chemical potentials of the leads
tlst = {0: tempL*k/e, 1: tempL*k/e, 2: tempR*k/e, 3: tempR*k/e}  # Lead temperatures
# Define tunnel couplings: (lead, level)
tleads = {(0,0): tl, (1,1): tl, (0,2): tl, (1,3): tl, (0,4): tl, (1,5): tl,
          (2,0): tr, (3,1): tr, (2,2): tr, (3,3): tr, (2,4): tr, (3,5): tr} 
# Supply Coulomb matrix elements, excluding exchange interaction
coulomb = {(0,1,1,0): Ec, (0,2,2,0): Ec, (0,3,3,0): Ec, (0,4,4,0): Ec,
           (0,5,5,0): Ec, (1,2,2,1): Ec, (1,3,3,1): Ec, (1,4,4,1): Ec,
           (1,5,5,1): Ec, (2,3,3,2): Ec, (2,4,4,2): Ec, (2,5,5,2): Ec,
           (3,4,4,3): Ec, (3,5,5,3): Ec, (4,5,5,4): Ec
           }

## Create system
system = qmeq.Builder(nsingle, hsingle, coulomb,
                 nleads, tleads, mulst, tlst, 1000, kerntype = 'Pauli')
# Note: For temperatures below 1 K Pauli fails, depending on tunnel couplings. Lindblad or RTD will
#       give good results in that regime.


## Example: Calculate charge stabiity diagram.

N1=200 # number of datapoints in gate- and bias voltage direction
N2=500
e1 = np.linspace(-10,10,N1)  # bias voltage
e2 = np.linspace(-5,40,N2)  # gate voltage induced energy shift
I = np.zeros([N1,N2])  # Create empty array for currents


# Loop over eL/eR values to calculate charge stability diagram.
for i,V in enumerate(e1):
    for j,eg in enumerate(e2):       
        #update hsingle:       
        hsingle = {(0,0): -eg, (1,1): -eg, (2,2): -eg+deltaE, (3,3): -eg+deltaE,
                   (4,4): -eg+2*deltaE, (5,5): -eg+2*deltaE}
        # Update chemical potentials:
        mulst = {0: -V/2, 1: -V/2, 2: V/2, 3: V/2}        
        system.change(hsingle=hsingle, mulst = mulst)  # Update system
        system.solve()  # Solve system      
        #Sum up current contributions from left and right lead, (pA)
        I[i,j] = (-(system.current[0] + system.current[1])*1.E9*e**2/hbar)      

# Plot charge stbility diagram
plt.pcolormesh(e2, e1 ,I, cmap='RdBu')
cbar = plt.colorbar()    
cbar.set_label('I (pA)')
plt.ylabel(r'V$_{SD}$ (mV)')
plt.xlabel(r'e$\alpha_\mathrm{g}$V$_{g}$ (V)')
plt.show()