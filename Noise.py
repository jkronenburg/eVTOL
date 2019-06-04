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

SPL = 83.4 + 15.3*log(P_motor) - 20*log(diameter_blade) + 38.5*M_t - 3*(N_blades-2) + 10*log(N_propellers) - 20*log(r_source,receiver)  #Formula for SPl_max(r) from midterm report section Noise
M_t = (pi * diameter_blade * RPM_rotor)/(60 * speed_of_sound)                                                                           #Propeller tip speed as a mach number
f   = (N_blades * RPM_rotor)/60                                                                                                         #frequency of rotor system
PNL = 40 + ((33 + 1/3) * log(noy))                                                                                                        #PNL value dependent on noy value. Noy values comes from the noise table found in the noise book
