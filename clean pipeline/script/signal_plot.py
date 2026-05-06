# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 09:50:21 2026

@author: marsg
"""

from matplotlib.pyplot import subplots
import load_default_params as ldp
import bin_extraction as ex
import pandas as pd


def signal_plot(radicals, old=True, bl_mode='off',number=None,**kwargs):
    
    Fig,axes=subplots(2,2,figsize=(16,9))
    axes=axes.reshape(-1)
    
    #Fig.suptitle('old='+str(old)+'| bl_mode='+bl_mode)
    
    for ax in axes: 
        ax.set_xlabel('concentration')
        ax.set_xlim(1,8)
    dF=pd.DataFrame()
    labels=ldp.gen_short_labels(radicals,old=old)
    
    k=0
        
    for radical in radicals:
        
        fnames,conc=ex.load_files(radical)
              
        
        if radical.find('old')!=-1 and old==False: continue # omits old data
       
    
        ex_dF= ex.extract_cwise(' E_max',conc,fnames,out=False,bl_corr='off',signal=True) 
        concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
        I_vals = ex.extract_cwise.I_vals
        
        ex_dF2= ex.extract_cwise(' baseline',conc,fnames,out=False,bl_corr='off',signal=True)
        
        ex_dF3= ex.extract_cwise(' E_max',conc,fnames,out=False,bl_corr='on',signal=True) 
               
        
        axes[0].errorbar(concs,ex_dF['values'],yerr= ex_dF['dev'],label=radical)
        axes[0].set_ylabel('E_max')
        axes[0].set_title('E_max (I normalized to baseline)')
        axes[0].set_ylim(-300,0)
        
        axes[1].errorbar(concs,ex_dF3['values'],yerr= ex_dF['dev'],label=radical)
        axes[1].set_ylabel('E_max ')
        axes[1].set_title('E_max (I normalized to averaged baseline)')
        axes[1].set_ylim(-300,0)
        
        axes[2].plot(concs,I_vals,label=radical)
        axes[2].set_ylabel('not normalized signal')
        axes[2].set_title ('not normalized signal')
        
        
        axes[3].plot(concs,ex_dF2['values'],label=radical)
        axes[3].set_ylabel('baseline')
        axes[3].set_title ('baseline')
        
        #dF[labels[k]]=ex_dF['values']
        
        k=k+1
    axes[3].legend(fontsize=8)
    #print(dF) 
    #dF.to_csv('single_plot'+str(number))
    Fig.tight_layout()