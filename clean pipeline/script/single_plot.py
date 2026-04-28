# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 13:21:56 2026

@author: marsg
"""
import bin_extraction as ex
import load_default_params as ldp


def single_plot(ax,param, radicals,old=True, bl_mode='off'):
    
    k=0
    
    ax.set_title('old='+str(old)+'|'+bl_mode)
    ax.set_xlabel('concentration')
    
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
        
        
        
        ex_dF= ex.extract_cwise(param,conc,fnames,out=False,bl_corr=blc)
        concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
        
               
        
        ax.errorbar(concs,ex_dF['values'],yerr= ex_dF['dev'],label=radical)
        ax.set
        
        
        
        k=k+1
    ax.legend(loc='lower right')
        
    
