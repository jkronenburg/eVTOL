# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 11:10:19 2019

@author: Miks
"""

import numpy as np
import matplotlib.pyplot as plt
from readPars import load_input, plot_graph
from DesIter_H2_Ray import IterNew

class Geometry:
    def __init__(self):
        self.geo=load_input(sheet='Dimensions and Positions')
        self.acdat=load_input(sheet='Aircraft parameters')
        self.taper=0.2*(2-np.radians(self.acdat.lambdac4))
        self.rootchord=(2*IterNew(mode='read', retrn='S'))/((1+self.taper)*IterNew(mode='read', retrn='b'))
        self.tipchord=self.rootchord*self.taper
        self.lambdale=np.arctan(np.tan(np.radians(self.acdat.lambdac4))-((self.rootchord/(2*IterNew(mode='read', retrn='b')))*(self.taper-1)))
        self.MGC=(2./3.)*self.rootchord*((1+self.taper+self.taper**2)/(1+self.taper))
        self.yMGC=(IterNew(mode='read', retrn='b')/6.)*((1+2*self.taper)/(1+self.taper))
        self.xMGC=np.tan(self.lambdale)*self.yMGC
        
    def getTaper(self):
        return self.taper
    
    def getRootChord(self):
        return self.rootchord
    
    def getTipChord(self):
        return self.tipchord
        
    def drawPlanform(self):
        self.xoutline=np.linspace(0, self.rootchord, 1000)
        self.youtline=self.xoutline[(self.xoutline/np.tan(self.lambdale))<IterNew(mode='read', retrn='b')/2]/np.tan(self.lambdale)
        self.xoutline=self.xoutline[(self.xoutline/np.tan(self.lambdale))<IterNew(mode='read', retrn='b')/2]
        self.xoutline=np.append(self.xoutline, [self.xoutline[-1]+self.tipchord, self.rootchord])
        self.youtline=np.append(self.youtline, [self.youtline[-1], 0])
        
        self.xoutline=np.append(self.xoutline, self.xoutline)
        self.youtline=np.append(self.youtline, -self.youtline)
        
        plt.plot(self.xoutline, self.youtline, label='Sweep c/4 = {} degrees'.format(self.acdat.lambdac4))
        plt.plot([self.xMGC, self.xMGC+self.MGC], [self.yMGC, self.yMGC], label='Mean geometric chord')
        plt.legend()