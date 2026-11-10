# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 19:05:02 2026

@author: marsg
"""
import pit2 as pit2
import bin_extraction as ex
from matplotlib.pyplot import subplots


def plot_param(radicals,param,ax,bl_mode='old',title=None,**kwargs):
    
    for k,radical in enumerate(radicals):
        
        
        # some conditions that were not ruled globally yet.. 
        
        if radical.find('old')!=-1 and bl_mode!= 'off':
            blc= True
           # print( f"baseline_correction enabled for {radical}")
            
           
        else: blc =False
        
        if bl_mode=='on': blc=True 
        
        
        #extracts data from multiple csv_files into one single iterable dataFrame: ex_dF
    
        fnames,conc=ex.load_files(radical)# loads the file
        ex_dF= ex.extract_cwise(param,conc,fnames,out=False,bl_corr=blc)
        concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
        
        x= concs
        y= ex_dF['values']
    
      
        # This is the plotting line. Note that errorbar also includes the standard line plot associoated with ax.plot
        
        pit2.pit(ax,title,x,y,yerror=ex_dF['dev'],label=radical[:-4],**kwargs)
        
#%% 3x1 plot


def plot_3x1(radicals):
    fig,axe= subplots(1,3,figsize=(12,5),dpi=300)
    
    plot_param(radicals,' E_max',axe[0],bl_mode='old',title= r'$\mathrm{E_{max}}$')
    plot_param(radicals,' P1/2',axe[1],bl_mode='old',title= r'$\mathrm{P_{1/2}}$')
    plot_param(radicals,' b1',axe[2],bl_mode='old',title= 'linewidth')
    axe[2].legend(fontsize=8)
    


        