# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:50:41 2019

@author: Miks
"""

import numpy as np
import matplotlib.pyplot as plt
from readPars import load_input

#MTOWi=3353.9570706384593
#pars=[4., 2., 5.0, 1300., 250.]

missiondat=load_input(sheet='Mission')
acdat=load_input(sheet='Aircraft parameters')
energdat=load_input(sheet='Energy storage')
miscdat=load_input(sheet='Misc')

def IterNew(MTOWi=acdat.MTOW, pars=None, missiondat=missiondat, acdat=acdat, energdat=energdat, miscdat=miscdat, retrn=None, mode='read'):
    '''
       retrn - Variabl name as a string that you want to output in read mode
       mode - 'read' or 'optimize' - optimize only used if new parameters have to be re-iterated with new design changes
    '''
    showdiag=False
    #========================================================================================
    #Known parameter values (Class I)
    #========================================================================================
    Espec=energdat.Espec
    WmotPmax=miscdat.WmotPmax
    if mode=='read':
       Nprops=acdat.Nprops
       Nblades=acdat.Nblades
       A=acdat.A
       DL=acdat.DL
       Vcruise=missiondat.Vcruise
       MTOWi=acdat.MTOW
    elif mode=='optimize':
        retrn=None
        if pars==None:
            raise Exception('Optimization parameters not specified')
        Nprops=pars[0]
        Nblades=pars[1]
        A=pars[2]    
        DL=pars[3]
        Vcruise=pars[4]/3.6
    else:
        raise Exception('Please specify the usage of the function in mode input parameter')
    
    rhoSL=missiondat.rhoSL #Density at sea level
    rhoTrans=missiondat.rhoTrans #Density at transition altitude of hT=500m
    rhoCruise=missiondat.rhoCruise #Density at cruise altitude of hC=3000ft
    bmax=acdat.bmax
    #========================================================================================
    #Assumed parameter values (Class I)
    #========================================================================================
    
    CLmax=acdat.CLmax
    CD0=acdat.CD0
    
    Vstall=0.5*Vcruise
    Pset=acdat.Pset
    mup=acdat.mup
    e=acdat.e
    k=1/(np.pi*A*e)
    
    ROCff=missiondat.ROCff
    CLROC=np.sqrt(3*CD0*1/k)
    CDROC=4*CD0
    
    M=acdat.M 
    TWto=acdat.TWto
    TWland=acdat.TWland
    Ti=acdat.Ti
    #========================================================================================
    #Requirement value generation
    #========================================================================================
    WSgen=np.arange(1, 3000)
    WSstall=0.5*rhoTrans*(Vstall**2)*CLmax
    PWcruise=(1/(Pset*mup))*(((CD0*0.5*rhoCruise*Vcruise**3)/(WSgen))+((WSgen)/(0.5*rhoCruise*Vcruise/k)))
    PWroc=(1/mup)*(ROCff+((np.sqrt(WSgen*(2/rhoCruise)))/((CLROC**1.5)/CDROC)))
    PWrod=0.5*rhoCruise*(Vcruise**3)*(1./WSgen)*(CD0+k*WSgen/(0.5*rhoCruise*Vcruise**2))
    PWhover=TWto*np.sqrt((DL)/(2*rhoTrans*(Ti**3)))*(1./M)
    PWland=TWland*np.sqrt((DL)/(2*rhoTrans*(Ti**3)))*(1./M) # Not sure if the rate of descent foruma applicable here, so we're just going for the rate of descent formula, with T/W=1
    
    Smax=(bmax**2)/A
    #========================================================================================
    #Plot generation
    #========================================================================================
    if showdiag:
        fig, ax1 = plt.subplots()
        plt.xlim(75, 1000)
        plt.ylim(0, 60)
        ax1.plot(WSgen, PWhover*np.ones((len(WSgen),)), label='Take-off (hover) requirement')
        ax1.plot(WSgen, PWland*np.ones((len(WSgen), )), label='Landing (hover) requirement')
        ax1.plot(WSgen, PWroc, label='FF Rate of Climb requirement')
        ax1.plot(WSstall*np.ones((len(WSgen),)), np.linspace(0, ax1.get_ylim()[1], len(WSgen)), label='FF Stall requirement')
        ax1.plot(WSgen, PWcruise, label='FF Cruise requirement')
        ax1.plot(WSgen, PWrod, label='FF Descent requirement')
        #ax1.fill_between(WSroc, PWhover*np.ones((len(WSroc))), 0, color="#fac2c2", alpha=0.4)
        #ax1.fill_between(WSroc, PWcruise, 0, color="#fac2c2", alpha=0.4)
        #ax1.fill_between(WSroc, 1/WProc, 0, color="#fac2c2", alpha=0.4)
        #ax1.axvspan(WSstall, ax1.get_xlim()[1], alpha=0.4, color='#fac2c2')
        plt.xlabel(r'$\frac{W}{S}$ [N/m2]', fontsize=18)
        plt.ylabel(r'$\frac{P}{W}$ [W/N]', fontsize=18)
        plt.legend()    
    #========================================================================================
    #Known parameter values (Class II)
    #========================================================================================
    Kmaterial=miscdat.Kmaterial
    Hcruise=missiondat.Hcruise
    R=missiondat.R
    Mpl=missiondat.Mpl
    HHVH2=energdat.HHVH2 #Higher heating value of H2, J/kg
    
    N_mot_hor=2
    N_prop_hor=N_mot_hor
    #========================================================================================
    #Assumed parameter values (Class II)
    #========================================================================================
    Kprop=miscdat.Kprop
    Htrans=missiondat.Htrans
    DoD=energdat.DoD
    MFstruct=acdat.MFstruct
    Msubsys=acdat.Msubsys
    Mavion=acdat.Mavion
    mubat=energdat.mubat
    mu_comp=energdat.mu_comp #Energy loss due to pump/valve/compressor losses
    mupem=energdat.mupem # PEM stack efficiency
    mutank=energdat.mutank #Tank efficiency estimate
    tankfactor=energdat.tankfactor #Some factor to take mass increase due to some tank component into account
    mfact_comp=energdat.mfact_comp #30% to take into account the mass of the fuel cell + battery components
    
    
    ROCvtol=missiondat.ROCvtol
    ROCfactor=missiondat.ROCfactor
    Wcabin=1.56
    #========================================================================================
    #Estimation of the parameters
    #========================================================================================
    Phover=PWhover*MTOWi*9.81
    S=MTOWi*9.81/WSstall
    b=np.sqrt(A*S)
    ROCh=ROCfactor*ROCff
    Wmax=WSstall*Smax/9.81
    vh=np.sqrt(DL/(2*rhoTrans))
    #
    Pto=((0.5*ROCvtol/vh)+np.sqrt(0.25*((ROCvtol/vh)**2)+1))*Phover
    Pclimb=(1/mup)*(ROCh+((np.sqrt(WSstall*(2./rhoCruise)))/((CLROC**1.5)/CDROC)))*MTOWi*9.81
    Pcruise=(1/(Pset*mup))*(((CD0*0.5*rhoCruise*Vcruise**3)/(WSstall))+((WSstall)/(0.5*rhoCruise*Vcruise/k)))*(MTOWi-0.25*Mpl)*9.81
    Pdesc=(0.5*rhoCruise*(Vcruise**3)*(1./WSstall)*(CD0+k*WSstall/(0.5*rhoCruise*Vcruise**2)))*MTOWi*9.81 #Assumption - descent in forward flight is performed at cruise velocity
    if -ROCvtol/vh<=-2:
        Pland=((0.5*-ROCvtol/vh)-np.sqrt(0.25*((-ROCvtol/vh)**2)-1))*Phover
    else:
        Pland=((-ROCvtol/vh)+0.974-1.125*(-ROCvtol/vh)-1.372*((-ROCvtol/vh)**2)*-1.718*((-ROCvtol/vh)**3)-0.655*((-ROCvtol/vh)**4))*Phover
    VROC=(Pclimb/(0.5*rhoCruise*S*CDROC))**(1/3.)
    
    if Nblades == 2:
        Kp = 0.1072
    elif Nblades == 3:
        Kp = 0.0995
    elif Nblades == 4:
        Kp = 0.0938
    elif Nblades == 5:
        Kp = 0.0908
    
    
    MESC=0.7383e-04*(Pto/Nprops)**(0.8854)
    MESC_hor=0.7383e-04*(Pcruise/N_prop_hor)**(0.8854) #Do I take the Ti=1.26 into account for cruise?
    
    P_mot_hor=Pcruise/N_mot_hor
    Dprop_hor = Kp*P_mot_hor**(1./4.)
    Mprop_hor=Kmaterial*Kprop*N_prop_hor*(Nblades**0.391)*(Dprop_hor*P_mot_hor/(1000))**0.782
    Mpropulsion_hor=1.1*(N_mot_hor*(WmotPmax*(P_mot_hor/(9.81))+MESC_hor)+Mprop_hor)
    
    Sprop=(MTOWi*9.81)/(DL*Nprops)
    Dprop=np.sqrt(4*Sprop/np.pi)
    Mprop=Kmaterial*Kprop*Nprops*(Nblades**(0.391))*(Dprop*Pto/(1000*Nprops))**0.782
    Mpropulsion=1.1*(Nprops*(WmotPmax*(Pto/(9.81*Nprops))+MESC)+Mprop)
    Tvtol=Htrans/ROCvtol
    Tclimb=(Hcruise-Htrans)/ROCh
    Tcruise=((R/3.)-VROC*np.cos(np.arcsin(ROCh/VROC))*Tclimb-Vcruise*np.cos(np.arcsin(ROCh/VROC))*Tclimb)/Vcruise #Insert VROC
    Tsegment=Tvtol*2+Tclimb*2+Tcruise
    Tmission=Tsegment*3
    Propspace=((b-Wcabin)/Nprops)-Dprop
    
    Pavg=(Pto*Tvtol+Pclimb*Tclimb+Tcruise*Pcruise+Pdesc*Tclimb+Pland*Tvtol)/(Tvtol*2+Tclimb*2+Tcruise)    
    Ebatt=((Pto-Pavg)*2*Tvtol)*3
    Efc=(3*Pclimb*Tclimb+3*Pcruise*Tcruise+3*Pdesc*Tclimb)/mu_comp
    Etot=Ebatt+Efc
    
    
    MFbatt=Ebatt/(MTOWi*Espec*DoD*mubat)
    MFH2=Efc/(MTOWi*HHVH2*mupem)
    MFtank=((MFH2/mutank)-MFH2)*tankfactor
    MFsys=(MFbatt+MFtank+MFH2)*mfact_comp
    MTOWnew=(Mpropulsion+Mpropulsion_hor+Mpl+Msubsys+Mavion)/(1-MFsys-MFstruct)
        
    
    if retrn==None:
        return MTOWnew, Wmax, S, A, b, Propspace, Dprop, WmotPmax, ROCvtol, DL, Vcruise, Pcruise/Pto
    else:
        return locals()[retrn]
