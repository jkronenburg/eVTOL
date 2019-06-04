#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 09:17:52 2019

@author: MatsKlijn
"""

# =============================================================================
# input variables
#   RPM_rotor
#   
# =============================================================================

from math import *
from matplotlib import *
import numpy as np 

# =============================================================================
# SPL = 83.4 + 15.3*log(P_motor) - 20*log(diameter_blade) + 38.5*M_t - 3*(N_blades-2) + 10*log(N_propellers) - 20*log(r_source,receiver)  #Formula for SPl_max(r) from midterm report section Noise
# M_t = (pi * diameter_blade * RPM_rotor)/(60 * speed_of_sound)                                                                           #Propeller tip speed as a mach number
# f   = (N_blades * RPM_rotor)/60                                                                                                         #frequency of rotor system
# PNL = 40 + ((33 + 1/3) * log(noy))                                                                                                        #PNL value dependent on noy value. Noy values comes from the noise table found in the noise book
# =============================================================================

PNL_A = 88.5                                                                    #dB, requirement for aircraft at close range
noy = 10**((PNL_A-26)/(33+1/3))                                                 #maximum value of noy to achieve the requirements for PNL A-weighted
noy_range = np.arange(1,noy,0.07)

acceptable_noys = [[50, 114],[63, 113],[80, 111],[100, 109],[125, 108],
                   [160, 107],[200, 105], [250, 104],[315,103],[400,102],
                   [500, 102],[630, 102],[800,102], [1000,102], [1250,100],
                   [1600,96],[2000,94],[2500,92],[3150,91],[4000,91],
                   [5000,92],[6300,93],[8000,96],[10000,99]]                    #[freq, SPL]

#print('freq and SPL value ',acceptable_noys[0][0],acceptable_noys[0][1])        #only change first [0]

N_blades = np.arange(2,6,1)                                                     #constraint on number of blades. Min = 2, Max = 5
parameter = []                                                                  #To append in for loop next lines, [RPM,N_blades]
M_tmax = 0.8                                                                    #Set a maximum tip speed to 0.8Mach
sos = 343                                                                       #Speed of sound at sea level in m/s
N_prop = np.arange(1,11,1)                                                      #range of number of possible propellers
r = 50                                                                          #Distance from sound source to sound receiver

for i in range(len(N_blades)):
    for l in range(len(acceptable_noys)):
        a = (acceptable_noys[l][0]*60)/N_blades[i]                              #a = RPMs
        b = (M_tmax*60*sos)/(pi*a)                                              #b = diameter propeller
        if b < 7.5 and b > 0.5:                                                 # Define range of propeller diameter between 0.5 and 7.5m
            for m in range(len(N_prop)):
                c = 10**(1/15.3*(acceptable_noys[l][1]-83.4+20*log(b)-38.5*M_tmax+3*(N_blades[i]-2)-10*log(N_prop[m])+20*log(r)))    #Formula for SPL rewritten to get P_motor       
                
                parameter.append([a,N_blades[i],acceptable_noys[l][1],b,c])           #Appended in 'parameter' is [RPM,N_blades, SPL value, N_diameter] related to eachother
      



              
print(parameter)   
    
    

    
    
    





