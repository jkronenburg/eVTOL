import numpy as np
from readPars import load_input, plot_graph
#aero = load_input(sheet = 'Aero')
mission = load_input(sheet = 'Mission')
sweep_wing =  0#rad ---------------------------------------------
tailfactor = .1

def design(V, rho, W, S, sweep, factor_tail):
    '''Wing'''
    q = 0.5 * rho * V**2
    CL_design = (1 + factor_tail)/q*(W/S) #cl design calculation; assumption; decrease of hydrogen almost no influence --> not average 
    
    '''Airfoil'''
    Veff = V*cos(sweep)
    qeff = .5*rho*Veff**2
    Cl = CL_design*q/qeff
    
    return CL_design, Cl

#make distinction between different airfoils


#V = mission.Vcruise, rho=mission.rhoCruise, 
#design(mission.Vcruise, mission.rhoCruise, ..., ..., tailfactor)