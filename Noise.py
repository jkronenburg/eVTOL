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

#print('freq and SPL value ',acceptable_noys[0][0],acceptable_noys[0][1])       #only change first [0]

N_blades = np.arange(2,6,1)                                                     #constraint on number of blades. Min = 2, Max = 5
parameter = []                                                                  #To append in for loop next lines, [RPM,N_blades]
M_tmax = 0.8                                                                    #Set a maximum tip speed to 0.8Mach
sos = 343                                                                       #Speed of sound at sea level in m/s
N_prop = np.arange(1,11,1)                                                      #range of number of possible propellers
r = 50                                                                          #Distance from sound source to sound receiver
MTOW = 3353*9.81                                                                #MTOW from the previous midterm report in N
FOM = 0.7                                                                       #Figure of Merit from the helicopter lady
rho = 1.225                                                                     #At sea level


for i in range(len(N_blades)):
    for l in range(len(acceptable_noys)):
        RPM = (acceptable_noys[l][0]*60)/N_blades[i]                              #RPMs
        D_prop = (M_tmax*60*sos)/(pi*RPM)                                              #b = diameter propeller
        if D_prop < 7.5 and D_prop > 0.5:                                                 # Define range of propeller diameter between 0.5 and 7.5m
            for m in range(len(N_prop)):
                P_mot = e**(1/15.3*(acceptable_noys[l][1]-83.4+20*log(D_prop)-38.5*M_tmax+3*(N_blades[i]-2)-10*log(N_prop[m])+20*log(r)))    #Formula for SPL rewritten to get P_motor       
                
                DL = MTOW/(pi*D_prop**2/4)/N_prop[m]                                 #Disk loading formula in N/m^2
                P_req = sqrt((MTOW/1.26)**3/(2*rho*DL))/FOM/1000                     #Power required for hover from the drone report, divided by 1.26 is relationship for ducted propellers,
                if DL < 5000:    
                    if P_req < P_mot:      
                        parameter.append([RPM,N_blades[i],acceptable_noys[l][1],D_prop,P_mot,DL,P_req,N_prop[m]])     #Appended in 'parameter' is [RPM,N_blades, SPL value, N_diameter, P_mot, Disk Loading, P_req, N_propellers] related to eachother
                        #print(P_mot)
print(parameter[4])             
print(len(parameter))   
    

    

    
    
    





