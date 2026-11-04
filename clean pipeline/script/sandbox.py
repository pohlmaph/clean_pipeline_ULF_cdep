# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:50:34 2026

@author: marsg
"""
from matplotlib.pyplot import subplots

import fit_cf as fcf

import numpy as np

fig,axe=subplots(figsize=(16,9))



function= fcf.handler(isotope=14,N_relax= False)

c=np.linspace(0,10)


params=[10,0.31]
Y= function(c,*params)

axe.plot(c,Y)