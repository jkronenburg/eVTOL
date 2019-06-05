#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 09:17:52 2019

@author: MatsKlijn
"""

from math import *
from matplotlib import *
import numpy as np 
from readPars_specialmac import load_input
import pandas as pd

missiondat=load_input(sheet='Mission')
acdat=load_input(sheet='Aircraft parameters')
energdat=load_input(sheet='Energy storage')
miscdat=load_input(sheet='Misc')

PNL_A = 88.5                                                                     #dB, requirement for aircraft at close range
noy = 10**((PNL_A-26)/(33+1/3))                                                  #maximum value of noy to achieve the requirements for PNL A-weighted
noy_range = np.arange(1,noy,0.07)

acceptable_noys = [[50, 114],[63, 113],[80, 111],[100, 109],[125, 108],
                   [160, 107],[200, 105], [250, 104],[315,103],[400,102],
                   [500, 102],[630, 102],[800,102], [1000,102], [1250,100],
                   [1600,96],[2000,94],[2500,92],[3150,91],[4000,91],
                   [5000,92],[6300,93],[8000,96],[10000,99]]                     #[freq, SPL]

N_blades    = np.arange(2,6,1)                                                   #constraint on number of blades. Min = 2, Max = 5
parameter   = []                                                                 #To append in for loop next lines, [RPM,N_blades]
M_tmax      = 0.8                                                                #Set a maximum tip speed to 0.8Mach
sos         = 343                                                                #Speed of sound at sea level in m/s
N_prop      = np.arange(1,11,1)                                                  #range of number of possible propellers
r           = 50                                                                 #Distance from sound source to sound receiver
MTOW        = acdat.MTOW                                                         #MTOW from parameter excel in kg
FOM         = acdat.M                                                            #Figure of Merit from the helicopter lady
rho         = missiondat.rhoSL                                                   #At sea level
rhotrans    = missiondat.rhoTrans                                                #Density at transitioning altitude
ROC_vtol    = missiondat.ROCvtol
TW_to       = acdat.TWto
Ti          = acdat.Ti

for i in range(len(N_blades)):
    for l in range(len(acceptable_noys)):
        RPM     = (acceptable_noys[l][0]*60)/N_blades[i]                         #RPMs
        D_prop  = (M_tmax*60*sos)/(pi*RPM)                                       #b = diameter propeller
        if D_prop < 7.5 and D_prop > 0.5:                                        # Define range of propeller diameter between 0.5 and 7.5m
            for m in range(len(N_prop)):
                P_mot       = e**(1/15.3*(acceptable_noys[l][1]-83.4+20*log(D_prop)-38.5*M_tmax+3*(N_blades[i]-2)-10*log(N_prop[m])+20*log(r)))    #Formula for SPL rewritten to get P_motor       
                P_mot_per_propeller = P_mot/N_prop[m]
                if P_mot_per_propeller < 500:                                    #Maximum technology motor now is 500kW so only take shit below this value
                    DL          = MTOW*9.81/(pi*D_prop**2/4)/N_prop[m]                    #Disk loading formula in N/m^2 per propeller
                    P_req_hover = TW_to*sqrt(DL/(2*rhotrans*Ti**3))/FOM*MTOW*9.81/1000    #Power required for hover
                    Vh          = sqrt(DL/(2*rhotrans))                          #Vh is induced velocity (or mass flow)
                    P_to        = P_req_hover*((0.5*ROC_vtol/Vh)+sqrt(0.25*((ROC_vtol/Vh)**2+1)))
                    if DL > 100 and DL < 1000:                                   #Assumed disk loading between 100 and 1000 N/m^2 due to lower disk loading is more efficient for hover
                        if P_to < P_mot:      
                            parameter.append(['RPM',RPM,'#Blades',N_blades[i],'#Propellers',N_prop[m],'SPl',acceptable_noys[l][1],'Diameter Prop',D_prop,'P_mot',P_mot,'DL',DL,'P_to',P_to])     #Appended in 'parameter' is [RPM,N_blades, SPL value, N_diameter, P_mot, Disk Loading, P_req, N_propellers] related to eachother
                            #print(P_mot)

print(parameter[4])             
print(len(parameter))   
    
panda_data_file = 'pandas.xlsx'
    

    
    
    





