# -*- coding: utf-8 -*-

#Spyder Editor Bastiaan

from readPars import load_input, plot_graph
import numpy as np

par= load_input(sheet="Dimensions and Positions")
#mot = load_input(sheet="")
#Aircraft Parameters
b =   par.bwing         #wingspan m
c_w = par.widthfus           # cabin diam  m

#Wing Parameters
A = par.Awing
#oswald
c_root = par.cwingroot        #Root chord
labd = 0.8                    #Taper Ratio
w_l = 0.5*(b-c_w)               #winglength m

# Rotor Parameters
M_rot = 20               #Mass Rotor
l_fan = par.pospropy1 - 0.5*c_w

#creating a mesh in y direction
steps = 100         # mesh density
y = []
for i in range(steps):
    pici = (i+1)*w_l/steps
    y.append(round(pici,3))

#Forces and Moments
Sy = np.zeros(steps)
#Sx = np.zeros(steps)
Mx = np.zeros(steps)
Ty = np.zeros(steps)
  
#Adding forces to the wing
RotorMass = True
WingMass = True
RotorLift = True
WingLift = True
WingDrag = True
AeroMoment = True
Rotortorque = True

if RotorMass:
   for i in range(steps):
       if y[i]> l_fan:
           Sy[i] = Sy[i] + 9.81*M_rot
          
if WingMass:
    for i in range(steps):
        Sy[i] =  Sy[i] + (c_root*y[i] -0.5*labd*y[i]**2)