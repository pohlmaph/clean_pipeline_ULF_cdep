# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 13:42:13 2026

@author: marsg
"""
import matplotlib as mpl
from matplotlib.pyplot import subplots
import numpy as np

import bin_extraction as ex
import load_default_params as ldp
import processing_functions as prc

from scipy.optimize import curve_fit

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

def E_max_int(radical,out=False,plot=False,bl_mode='old'):
    
    if plot ==True: Fig,axe= subplots(figsize=(16,9))
    
    def func(c,S,b,d):
        
        y= S*(1-np.exp(-b*c))+d
        
        return y 
    E_max_int.func=func
    
    if radical.find('old')!=-1 and bl_mode != 'off':
        blc= 'on'    
    else: blc ='off'
    #if radical.find('old')!=-1 and old==False: continue # omits old data    
    if bl_mode=='on': blc='on' 
    
    fnames,conc=ex.load_files(radical)
    
    ex_dF= ex.extract_cwise(' E_max',conc,fnames,out=False,bl_corr=blc)
    concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
    exp_val=list(ex_dF['values'])
    
    if plot ==True: axe.scatter(concs,exp_val,s=20)
    params,pcov=curve_fit(func,concs,exp_val,p0=[-155.49125959,0.79470354,-8.00616629])
    
    x_opt= np.linspace(min(concs),max(concs))
    y_opt=func(x_opt,*params)
    
    if plot == True: axe.plot(x_opt,y_opt)
        #axe.scatter(concs,exp_val,s=20)
        
        
        
    return params,concs,exp_val

def P_12_int(radical,out=False,bl_mode='old',plot=False):
    
    if plot ==True: Fig,axe=subplots(figsize=(16,9))
    
    fnames,conc_ul=ex.load_files(radical)
    ex_dF= ex.extract_cwise(' P1/2',conc_ul,fnames,out=False)
    concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.otherwise c is given by the order of filenames
    if plot ==True: axe.scatter(ex_dF['values'].index,ex_dF['values'])
    
    x_opt,y_opt,fit_params,errors,perc,rsquare=prc.lin_fit(ex_dF['values'].index,ex_dF['values'])
    
    exp_values=ex_dF['values']
    if plot ==True: axe.plot(x_opt,y_opt)
    
    return fit_params,exp_values
    
    
    
    
def fixed_p_plot(radicals,powers,old=True,bl_mode='old'):

    Fig,axe=subplots(1,3,figsize=(10,4))
    axes=axe.reshape(-1)
    
    #Fig.suptitle(str(old)+'|'+bl_mode)
    
    
    for radical in radicals:
        
        fnames,conc=ex.load_files(radical)
        
        
        if radical.find('old')!=-1 and bl_mode != 'off':
            blc= 'on'
            # print( f"baseline_correction enabled for {radical}")
        else: blc ='off'
        
        #if radical.find('old')!=-1 and old==False: continue # omits old data
            
        if bl_mode=='on': blc='on' 
        
        ex_dF1= ex.extract_cwise(' E_max',conc,fnames,out=False,bl_corr=blc)
        concs=list(ex_dF1.index)# This overwrites concs with the sorted list matching the dataframe order.
        
        ex_dF2= ex.extract_cwise(' P1/2',conc,fnames,out=False,bl_corr='off')
        for i,ax in enumerate(axes):
            fpvs= Enhancement(powers[i],ex_dF1['values'],ex_dF2['values']) 
            
            ax.plot(concs,fpvs,label= radical,marker='o')
            ax.set_title(str(powers[i])+' W')
            #ax.set_ylim(-200,0)
        axes[2].legend()    
    return axes

def fixed_P_int(radicals,powers,old=False,bl_mode='on'):
    
    Fig,axe=subplots(1,3,figsize=(10,4),sharey=True)
    axes=axe.reshape(-1)
    
    
        
    for radical in radicals:
        
        print(radical)
        
        Emax_params,conc,E_max_raw=E_max_int(radical,plot= True,bl_mode='old')
        print('E_max_fit worked')
        print(radical, Emax_params)
        
        P_12_params,P_12_raw=P_12_int(radical,out=False,bl_mode='old',plot=True)
        print('P_12 fit worked')
        
        c_plot= np.linspace(min(conc),max(conc))
        
        E_max= [E_max_int.func(c,*Emax_params) for c in c_plot]
        P_12=[prc.lin_fit.lin_func(c,*P_12_params) for c in c_plot]
        
        for i,ax in enumerate(axes):
            E= [Enhancement(powers[i],*pair) for pair in zip(E_max,P_12)]
            E_raw= [Enhancement(powers[i],*pair) for pair in zip(E_max_raw,P_12_raw)]
        # caution, self built functions cannot handle arrays. use list comprehension.
        
            min_idx= E.index(min(E))
            c_min=c_plot[min_idx]
            E_min=min(E)
            ax.plot(c_plot,E)
            ax.scatter(conc,E_raw,label=radical)
            ax.set_xlabel('concentration in mM',fontsize=10)
            ax.set_title(str(powers[i])+' W',fontsize=10)
            
            ax.vlines(c_min,-145,E_min,linestyle=':',color='orange')
            ax.set_ylim(-145,0)
        axes[0].set_ylabel('Enhancement')
        
        
        
        
            
        
    