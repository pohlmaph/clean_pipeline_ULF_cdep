# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 09:42:52 2026

@author: marsg
"""
from numpy import mean

import bin_extraction as ex
import processing_functions as prc

def get_mean_T10(radicals,exclude=None):
    
    op=[]
    # print('T1_0')
    # print('_____________________')
    
    if exclude!=None: 
        radicals.pop(radicals.find(exclude))
    for radical in radicals:
        #print(radical)
        fnames,conc_ul=ex.load_files(radical)
        
        ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=False)
        concs=list(ex_dF.index)
        
        T1s=ex_dF['values']
        T1_0= prc.get_r(radical,concs,ex_dF['values'])[1]
        op.append(T1_0)
        
        
    #     print(radical, T1_0,sep='\t'+'\t')
    # print('popped',op.pop(2))# pop TEMPOL)    
    T10_mean= mean(op)
    return(op,T10_mean)    
        
        

def leakage_factor(T1,T10):
    f=1-T1/T10
    return f

def get_smaxzeta(T1s,T1_0,E_max,interpolated=False, T10_mean=False,radicals=None):# implement interpol later
    
    if T10_mean== True and radicals!=None: 
        T1_0= get_mean_T10(radicals,exclude='4-Hydroxy-14N-TEMPO_old')[1]
    
    
    lfs= [leakage_factor(T1,T1_0)for T1 in T1s]
    
    get_smaxzeta.lf=lfs
    
    smz=[]
    for i in range(len(E_max)):
        smaxzeta=(E_max[i]-1)/(-lfs[i]*638.891)
        smz.append(smaxzeta)
        #print(smz)
    
    return smz


        
        
        
    
    
    