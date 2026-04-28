# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 13:42:13 2026

@author: marsg
"""
import matplotlib as mpl
from matplotlib.pyplot import subplots
import bin_extraction as ex
import load_default_params as ldp
import numpy as np

def Enhancement(P,E_max,P_12): # c is not required here, but is not changed to avoid follow up changes
    E= 1 + (((E_max - 1) * P/(P_12 + P)))
    #from ML file: E_(c,i) = 1 + (((E_max(c,1) - 1) * P(i)) / (P_12(c,1) + P(i)))
    return E

def power_sweep_fit(radical,Plim):
    
    fnames,conc=ex.load_files(radical)
    ex_dF1= ex.extract_cwise(' E_max',conc,fnames,out=False,bl_mode='on')
    concs=list(ex_dF1.index)# This overwrites concs with the sorted list matching the dataframe order.
    ex_dF2= ex.extract_cwise(' P1/2',conc,fnames,out=False,bl_mode=False)
    
    Fig,axe=subplots(figsize=(16,9))
    
    
    for i, E_max in enumerate(ex_dF1['values']):
        x= np.linspace(0,Plim)
        y= Enhancement(x,ex_dF1['values'].iloc[i],ex_dF2['values'].iloc[i])
        
        axe.plot(x,y,label=concs[i])
    axe.legend()
    axe.set_title(radical)
        
    return None
    
def fixed_p_plot(radicals,powers,old=False,bl_mode='on'):

    Fig,axe=subplots(2,3,figsize=(16,9))
    axes=axe.reshape(-1)
    
    
    
    for radical in radicals:
        
        fnames,conc=ex.load_files(radical)
        
        ## determination of concs has to be automized !
        #done
        # currently the second radical data is just a copy of the first
        if radical.find('old')!=-1 and bl_mode != 'off':
            blc= True
            # print( f"baseline_correction enabled for {radical}")
        else: blc =False
        
        if radical.find('old')!=-1 and old==False: continue # omits old data
            
        if bl_mode=='on': blc=True 
        
        ex_dF1= ex.extract_cwise(' E_max',conc,fnames,out=False,bl_corr=blc)
        concs=list(ex_dF1.index)# This overwrites concs with the sorted list matching the dataframe order.
        
        ex_dF2= ex.extract_cwise(' P1/2',conc,fnames,out=False,bl_corr='off')
        for i,ax in enumerate(axes):
            fpvs= Enhancement(powers[i],ex_dF1['values'],ex_dF2['values']) 
            
            ax.plot(concs,fpvs,label= radical,marker='o')
            ax.set_title(str(powers[i])+' W')
        axes[0].legend()    
    return   