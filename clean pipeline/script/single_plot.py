# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 13:21:56 2026

@author: marsg
"""
import bin_extraction as ex
import load_default_params as ldp

import pandas as pd


def single_plot(ax,param, radicals,old=True, bl_mode='off',number=None,**kwargs):
    
    k=0
    
    ax.set_title('old='+str(old)+'|'+bl_mode)
    ax.set_xlabel('concentration')
    
    dF=pd.DataFrame()
    labels=ldp.gen_short_labels(radicals,old=old)
    print(labels)
    for radical in radicals:
        
        fnames,conc=ex.load_files(radical)
        
        ## determination of concs has to be automized !
        #done
        # currently the second radical data is just a copy of the first
        if radical.find('old')!=-1 and bl_mode != 'off':
            blc= 'on'
            # print( f"baseline_correction enabled for {radical}")
        else: blc ='off'
        if bl_mode=='on': blc='on' 
        if bl_mode=='constant': blc='constant'
        
        if radical.find('old')!=-1 and old==False: continue # omits old data
        
    
        
        
        
        
        ex_dF= ex.extract_cwise(param,conc,fnames,out=False,bl_corr=blc)
        concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
        
               
        
        ax.errorbar(concs,ex_dF['values'],yerr= ex_dF['dev'],label=radical)
        
        dF[labels[k]]=ex_dF['values']
        
        
        
        
        
        
        k=k+1
    ax.legend(fontsize=8)
    print(dF) 
    dF.to_csv('single_plot'+str(number))
    
