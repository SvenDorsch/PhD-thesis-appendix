# -*- coding: utf-8 -*-
"""
Classical rate equation based model for current through QD with single spin degenerate level.
For description, see thesis section 4 and references therein.
Model is also reproduced using QmeQ.

Bias is applieds to the elads symmetrically. An electron travelling from drain (R) to source (L)
gives a positive current contribution.
"""
import qmeq
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.constants import e, k, hbar


## Define functions:

def fL(E, V, T):
    """
    Fermi-Dirac function left lead incl. symmetric bias contribution.
    Parameters: 
        E: Energy (meV) 
        V: Bias (mV)
        T: Reservoir temperature (K)
    """
    k_meV = k*6.241506363094e+18*1e3 # Boltzmann constant in meV
    return 1/(math.e**((E+V/2)/(k_meV*T))+1)

def fR(E, V, T):
    """
    Fermi-Dirac function right lead incl. symmetric bias contribution.
    Parameters: E: Energy. V: Bias. T: Reservoir temperature
    """
    k_meV = k*6.241506363094e+18*1e3 # Boltzmann constant in meV
    return 1/(math.e**((E-V/2)/(k_meV*T))+1)


def I01(E, V, TL, TR, GL, GR):
    """
    Current across 0 to 1 charge state transition.
    Parameters:
        E: Energy (meV)
        V: Bias (mV)
        TL: Temperature left lead (K)
        TR: Temperature right lead (K)
        GL: Tunnel coupling to left reservoir (Hz)
        GR: Tunnel coupling to right reservoir (Hz)
    """
    return 2*e*((GL*GR)/(GL+GR+GR*fR(E, V, TR)+GL*fL(E, V, TL)))*(fR(E, V, TR)-fL(E, V, TL))


def I12(E, V, TL, TR, GL, GR):
    """
    Current across 1 to 2 charge state transition.
    Parameters:
        E: Energy (meV)
        V: Bias (mV)
        TL: Temperature left lead (K)
        TR: Temperature right lead (K)
        GL: Tunnel coupling to left reservoir (Hz)
        GR: Tunnel coupling to right reservoir (Hz)
    """
    return e*(2*(GL*GR)/(2*(GL+GR)-GL*fL(E, V, TL)-GR*fR(E, V, TR)))*(fR(E, V, TR)-fL(E, V, TL))

def SimpleRates(Eg_vals, Vbias, TL, TR, gam=100e6):
    """
    Calculate current across QD: I = I01 + I12.
    Parameters:
        Eg_vals: List of energy values for QD levels, corresponds to e*alpha_g*V_g, supply in (meV)
        Vbias: Bias voltage (mV)
        TL: Temperature left lead (K)
        TR: Temperature right lead (K)
        gam: Tunnel coupling across both barriers, assumed symmetric (Hz)
    """
    Ec = 5  # Charging energy in meV
    E1_0 = 0  # Level position for N = 1 in meV
    E2_0 = E1_0+Ec  # Level position for N = 2 in meV
    GL = gam  # in GHz
    GR = GL
    I = []
    for Eg in Eg_vals:
        E1 = E1_0+Eg  # Calculate shifted energy states
        E2 = E2_0+Eg
        I01_tmp = I01(E1, Vbias, TL, TR, GL, GR)  # Calculate current ontribution through each level
        I12_tmp = I12(E2, Vbias, TL, TR, GL, GR)
        I.append((I01_tmp+I12_tmp)*1e12)  # Calculate total current in pA        
    return I


def QmeQ_MasterEq(Eg_vals, Vbias, TL, TR, gam=100e6, kern='Pauli'):
    """
    Use QmeQ to calculate current through QD with a single spin degenerate resonance.
    Parameters:
        Eg_vals: List of energy values for QD levels, corresponds to e*alpha_g*V_g, supply in (meV)
        Vbias: Bias voltage (mV)
        TL: Temperature left lead (K)
        TR: Temperature right lead (K)
        gam: Tunnel coupling across both barriers, assumed symmetric (Hz)
        kern: QmeQ kernel type. Example: Pauli, RTD, Lindblad.
    Note that Pauli can fail for low temperatures, but RTD usually works.   
    """
    # General QD parameters
    Ec = 5  # Charging energy (meV)
    gammaR = 1000*(hbar*gam)/e  # Left tunnel coupling
    gammaL = gammaR  # Right tunnel coupling
    tempL = TL*1000*k/e  # Temperature left reservoir
    tempR = TR*1000*k/e  # Temperature right reservoir
    
    
    ## Define QD system:
    
    nsingle = 2  # Total number of levels on DQD
    e0 = 0  # initial ground state energy
    #hsingle supplies single particle energy states and tunneling between levels
    hsingle = {(0,0): e0, (1,1): e0}

    # Define leads:
    nleads = 4  # Total number of leads, 4 incl. both spins
    # Prepare bare tunnel rates for QmeQ
    tl, tr = np.sqrt((1000*(hbar*gam)/e)/(2*np.pi)), np.sqrt((1000*(hbar*gam)/e)/(2*np.pi))
    mulst = {0: -Vbias/2, 1: -Vbias/2, 2: Vbias/2, 3: Vbias/2}  # Define lead el.chem. potentials
    tlst = {0: tempL, 1: tempL, 2: tempR, 3: tempR}  # Assign lead temperatures   
    tleads = {(0,0): tl, (1,1): tl, (2,0): tr, (3,1): tr}  # Define tunneling between (lead,level)     
    coulomb = {(0,1,1,0): Ec} # Supply Coulomb matrix elements

    # Create system:
    system = qmeq.Builder(nsingle, hsingle, coulomb,
                  nleads, tleads, mulst, tlst, 100, kerntype = kern)
    
    # Calculate current
    I = []
    for Eg in Eg_vals: #Get index/value of energy for QD L        
        #update hsingle:        
        hsingle = {(0,0): +Eg, (1,1): +Eg}       
        # Update chemical potentials:
        mulst = {0: -Vbias/2, 1: -Vbias/2, 2: Vbias/2, 3: Vbias/2}        
        system.change(hsingle=hsingle, mulst = mulst)  # Update system
        system.solve()  # Solvve updated system       
        #Sum up current contributions from left and right lead, in (pA)
        I.append(-((system.current[0] + system.current[1])*1.E9*e**2/hbar/(1)))            
    return I


## Simple example based on above models: Thermoelectric current, TL = 1 K, TR = 2 K, Vbias = 0 V

# Define energy axis, corresponds to e*alpha_g*Vg and thus gate induced level shift
Eg_vals = np.linspace(3, -8, 500) # in meV, corresponds to alpha_g*Vg
I_rateEq = SimpleRates(Eg_vals, 0, 1, 2)  # Calculate current with rate eq.
I_QmeQ = QmeQ_MasterEq(Eg_vals, 0, 1, 2, kern='RTD')  # Calculate current with QmeQ and RTD

# Plot results:
plt.plot(Eg_vals, I_rateEq, color='black', label='rate eq.')
plt.plot(Eg_vals, I_QmeQ, color='red', ls=':', label='QmeQ: RTD')
plt.xlabel(r'-e$\alpha_\mathrm{g}\mathrm{V_g}$ (meV)')
plt.ylabel('I (pA)')
plt.legend()
plt.show()
