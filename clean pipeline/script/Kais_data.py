# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 14:34:34 2026

@author: marsg
"""

import pandas as pd
from matplotlib.pyplot import subplots

from glob import glob


import bin_extraction as ex
import load_default_params as ldp
import processing_functions as prc

mass_dict= {'Amino-14N-TEMPO_3_26': 171.1,
             '4-Amino-14N-TEMPO_old': 171.1,
             '4-Amino-15N-TEMPO_old':172.1,
             'Oxo-15N-TEMPO_3_26': 171.1,
             '4-Oxo-15N-TEMPO_old': 171.1,
             '4-Hydroxy-14N-TEMPO_old':172.1,
             '4-Oxo-14N-TEMPO_old':170.1,
             'Hydroxy-14N-TEMPO': 172.1,
             'Oxo-14N-TEMPO': 170,
             'Oxo71':'enter mass',
             'TEMPO-14N':156,
             'TEMPO-14N_old': 156,
             '14N-TEMPO_old':156,
             'TEMPO-15N':157,
             'Carboxy-14N-Proxyl':'enter mass',
             '4-Amino-15N-TEMPO':172.15,
             '4-Hydroxy-15N-TEMPO':173.15,
             
             
             }

def plot_pool_data(radicals,bl_mode='old'):
    
    filename = glob('*.csv')[0]
    
    dF=pd.read_csv(filename)
    
    print(dF)
    print(dF.columns)
    
    Fig,axe=subplots(figsize=(16,9),dpi=300)
    Fig2,axe2=subplots(figsize=(16,9),dpi=300)
    
    axe=[axe,axe2]
    
    
    P12_values=[]
    lw_values=[]
    
    #Pauls data
    k=0
    for k,Kradical in enumerate(dF['Radical']):
        
        if Kradical in ['M4','M6']:
            color='blue'
        else:color='black'
        
        
        #axe0
        x=dF['MW'][k]
        y=-dF['E_max'][k]
        yerr=dF['E_max_err'][k]
        xerr=None
        
        axe[0].scatter(x,y,s=20,color=color)
        axe[0].errorbar(x,y,yerr=yerr,color= color)
        axe[0].text(x,y+2,dF['Radical'][k])
        
        #axe[1]
        x= dF['lw'][k]
        y= dF['P1/2'][k]
        xerr=dF['lw_err'][k]
        yerr=dF['P_12_err'][k]
        
        axe[1].scatter(x,y,s=20,color=color)
        axe[1].errorbar(x,y,xerr=xerr,yerr=yerr,color=color)
        axe[1].text(x,y+0.2,dF['Radical'][k])
        
    #our data    
    
    for radical in radicals:
        
        # some conditions that were not ruled globally yet.. 
        
        if radical.find('old')!=-1 and bl_mode!= 'off':
            blc= True
           # print( f"baseline_correction enabled for {radical}")
            
            #if old==False: continue # omits old data
        else: blc =False
        #
        if bl_mode=='on': blc=True 
        
        if radical.find('15N') != -1: color='purple'
        else: color ='red'
        
        
        
        ## axe 0
        
        #extracts data from multiple csv_files into one single iterable dataFrame: ex_dF
    
        fnames,conc_ul=ex.load_files(radical)# loads the file
        ex_dF= ex.extract_cwise(' E_max',conc_ul,fnames,out=False,bl_corr=blc)
        concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
        
        print(ex_dF.columns) 
        
        y= ex_dF['values'].loc[2.0]
        x=mass_dict[radical]
        yerr= ex_dF['dev'].loc[2.0]
        xerr=None
        
        print(yerr)
        
        axe[0].scatter(x,y,color=color,s=30)
        axe[0].text(x,y+2,ldp.name_dict[radical] ,color=color)
        axe[0].errorbar(x,y,xerr=xerr,yerr=yerr,color=color)
        
        axe[0].set_ylabel(r'$\mathrm{E_{max}}$')
        axe[0].set_xlabel('Molar mass in g/mol')
        
        #axe1
        
        lw_dF= ex.extract_cwise(' b1',conc_ul,fnames,out=False,bl_corr=blc)
        concs=list(lw_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
        
        P12_dF= ex.extract_cwise(' P1/2',conc_ul,fnames,out=False,bl_corr=blc)
        concs=list(P12_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
        
        # the lw values are in units of the sweep variable (correction factor= 1.464)
        x=lw_dF['values'].loc[2.0]*1000/1.548
        y=P12_dF['values'].loc[2.00]
        
        xerr= lw_dF['dev'].loc[2.0]*1000/1.548
        yerr= P12_dF['dev'].loc[2.0]
        
        lw_values.append(x)
        P12_values.append(y)
        
        axe[1].scatter(x,y,color=color,s=30)
        axe[1].text(x,y+0.2,ldp.name_dict[radical], color=color)
        axe[1].errorbar(x,y,xerr=xerr,yerr=yerr,color=color)
        
        axe[1].vlines(x,0,y,color=color,alpha=0.2,)
        axe[1].hlines(y,0,x,color=color,alpha=0.2)
        
        axe[1].set_xlim(20,140)
        axe[1].set_ylabel(r'$\mathrm{P_{1/2}}$')
        axe[1].set_xlabel(r'linewidth/b1 in $\mu T$')
        
    #print(lw_values)
    #print(P12_values)
    fit_data=prc.lin_fit(lw_values,P12_values)
    axe[1].plot(*fit_data[:2],label='linear trendline',color='red')
        
 