# -*- coding: utf-8 -*-
"""
Created on Mon May 11 16:03:07 2026

@author: RAPohlP1
"""
import pandas as pd
import fixed_P_plot as fpp
import numpy as np
from matplotlib.pyplot import subplots

filenames=['6pH_general_radical_charac.csv', '7.6pH_general_radical_charac.csv']
labels =['pH = 6', 'pH = 7.4']

Fig,axe=subplots(figsize=(16,9))
Fig.suptitle('4-Amino-TEMPO|2mM')

for i,file in enumerate(filenames): 
    dF=pd.read_csv(file)
    
    E_max=dF[' E_max'].iloc[0]
    P12=dF[' P1/2'].iloc[0]
    
    powers= np.linspace(0,20)
    Enhancement=fpp.Enhancement(powers,E_max,P12)
    
    axe.plot(powers,Enhancement, label= labels[i])
    
axe.legend()
    
    