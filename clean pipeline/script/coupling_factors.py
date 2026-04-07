# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 09:42:52 2026

@author: marsg
"""

def leakage_factor(T1,T10):
    f=1-T1/T10
    return f

def get_smaxzeta(T1s,T1_0,E_max,interpolated=False):# implement interpol later
    
    
    lfs= [leakage_factor(T1,T1_0)for T1 in T1s]
    get_smaxzeta.lf=lfs
    
    smz=[]
    for i in range(len(E_max)):
        smaxzeta=(E_max[i]-1)/(-lfs[i]*638.891)
        smz.append(smaxzeta)
        print(smz)
    
    return smz


        
        
        
    
    
    