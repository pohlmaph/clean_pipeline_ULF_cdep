# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:36:00 2026

@author: marsg
"""

#make this code work from Main.py!!

import bin_extraction as ex
import processing_functions as prc
import load_default_params as ldp
import coupling_factors as cf



import matplotlib as mpl
import pandas as pd 
import numpy as np

from matplotlib.pyplot import subplots
from glob import glob
from scipy.optimize import curve_fit
from pathlib import Path
import os
#%% all in one param plot. 

def tile_plot_raw(radicals,parameters,spider_colors,old =True,bl_mode='old'): 


# nested loop order is aligned with the spider plots. 
# -> the plot takes values of different radicals for one parameter
# i.E  one column at a at time. 
# with the new dataFrame order this means looping over the same column index in different dataframes

# loop over parameters

    FigA,axeA=subplots(2,3,figsize=(16,9))
    FigA.suptitle('Radical_comp|parameter plot A')
    axesA= axeA.reshape(-1)
    FigB,axeB=subplots(2,3,figsize=(16,9))
    FigB.suptitle('Radical_comp |parameter plot B')
    axesB= axeB.reshape(-1)
    FigC,axeC=subplots(2,3,figsize=(16,9))
    FigC.suptitle('Radical_comp |parameter plot C')
    axesC= axeC.reshape(-1)
    
    all_axes= list(axesA)+list(axesB)+list(axesC)
    
    
    
    P12_plist=[]
    
    
    #recheck position!!
    i=0   
    for param in parameters:
        k=0
        if i >len(all_axes): break
        ax= all_axes[i]
        
        for radical in radicals:
            
            fnames,conc=ex.load_files(radical)
            
            ## determination of concs has to be automized !
            #done
            # currently the second radical data is just a copy of the first
            if radical.find('old')!=-1 and bl_mode!= 'off':
                blc= True
               # print( f"baseline_correction enabled for {radical}")
                
                if old==False: continue # omits old data
            else: blc =False
            #
            if bl_mode=='on': blc=True 
            
            ex_dF= ex.extract_cwise(param,conc,fnames,out=False,bl_corr=blc)
            concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
            
            
            
            
            
                
            
            if param==' P1/2':
                x_opt,y_opt,fit_params,errors,perc,rsquare=prc.lin_fit(ex_dF['values'].index,ex_dF['values'])
                axesA[i].plot(x_opt,y_opt,alpha=0.5)#color=spider_colors[k]
                
                P12_plist.append([radical,*fit_params, *errors,*perc, rsquare])
                
            
            
            
            ax.errorbar(concs,ex_dF['values'],yerr= ex_dF['dev'],label=radical) #color=spider_colors[k]
            ax.set_title(param)
            ax.set_xlabel('concentration')
        
            #axesA[i].set_ylabel(ylabels[i])
                
            # elif i<12:
            #     axesA[i].errorbar(concs,ex_dF['values'],yerror= ex_dF['dev'],marker='o',color=spider_colors[k],label=radical)
            #     axesB[i-6].set_title(param)
            #     axesB[i-6].set_xlabel('concentration')
            # elif i<18:
            #     axesA[i].errorbar(concs,ex_dF['values'],yerror= ex_dF['dev'],marker='o',color=spider_colors[k],label=radical)
            #     axesC[i-12].set_title(param)
            #     axesC[i-12].set_xlabel('concentration')
            # else:   break
            k=k+1
        i=i+1
        
    axesA[0].legend()
    axesB[0].legend()
        #axesC[0].legend()
        
        
        
    print('-----P_1/2 fit parameters--------')    
    P12_dF= pd.DataFrame(data=P12_plist,columns=['radical','slope','intercept','m_error','c_error','m_perc','c_perc','rsquare']) 
    print((P12_dF))
    return all_axes

#%% tile plot processed
#prc_params=[' T1', 'T2',' E_max',' P1/2', ]
#prc_params = ['r1','r2',' P1/2','cc','r1bar']
#corresponding=[' T1',' T2', ' E_max', 'P 1/2', ]



def tile_plot_prc(radicals,spider_colors,prc_params,short_labels= None,abb=None,old =False,bl_mode='old'): 
    
    print('baseline_mode: '+ bl_mode)
    
    # nested loop order is aligned with the spider plots. 
    # -> the plot takes values of different radicals for one parameter
    # i.E  one column at a at time. 
    # with the new dataFrame order this means looping over the same column index in different dataframes



    FigA,axeA=subplots(2,3,figsize=(16,9))
    FigA.suptitle('Radical_comp|processed parameters plot A ')
    axesA= axeA.reshape(-1)
    FigB,axeB=subplots(2,3,figsize=(16,9))
    FigB.suptitle('Radical_comp |parameter plot B')
    axesB= axeB.reshape(-1)
    # FigC,axeC=subplots(2,3,figsize=(16,9))
    # FigC.suptitle('Radical_comp |parameter plot C')
    # axesC= axeC.reshape(-1)
 #_______________________   
    def pit(i,param,x,y,yerror=None,linestyle='-',**kwargs):#plot in tile
    
            if i<6: 
                axesA[i].plot(x,y,**kwargs)
                axesA[i].set_title(param)
                axesA[i].set_xlabel('concentration')
                #axesA[i].set_ylabel(ylabels[i])
                
                kwargs['marker']=None
                axesA[i].errorbar(x,y,yerr=yerror,**kwargs)
                    
                
            elif i<12:
                axesB[i-6].plot(x,y,**kwargs)
                axesB[i-6].set_title(param)
                axesB[i-6].set_xlabel('concentration')
                
                kwargs['marker']=None
                if yerror: axesB[i-6].errorbar(x,y,yerr=yerror,**kwargs)
                
            # elif i<18:
            #     axesC[i-12].plot(concs,ex_dF['values'],marker='o',color=spider_colors[k],label=radical)
            #     axesC[i-12].set_title(param)
            #     axesC[i-12].set_xlabel('concentration')
        
        # if scatter == True:# exception can be made obsolete by using the linestyle=None keyword
            
        #     if i<6: 
        #         axesA[i].scatter(x,y,**kwargs)
        #         axesA[i].set_title(param)
        #         axesA[i].set_xlabel('concentration')
                
        #         if yerror: axesA[i].errorbar(x,y,yerr=yerror)
        #         #axesA[i].set_ylabel(ylabels[i])
                
        #     elif i<12:
        #         axesB[i-6].scatter(x,y,**kwargs)
        #         axesB[i-6].set_title(param)
        #         axesB[i-6].set_xlabel('concentration')
                
        #         if yerror: axesB[i-6].errorbar(x,y,yerr=yerror)
    
#_____________________________    
    P12_plist=[]
    r1s=[]
    r2s=[]
    barloc= []
    T1_0=[]
    
    
    # loop over parameters
    
      
    i=0
    for i,param in enumerate(prc_params):
        
        #print('i=',i)
        #print(param)
        if i>11: break
    
        for k,radical in enumerate(radicals):
            #print(radical)
            fnames,conc_ul=ex.load_files(radical)
            
            if radical.find('old')!=-1 and bl_mode!= 'off':
                blc= True
               # print( f"baseline_correction enabled for {radical}")
                
                if old==False: continue # omits old data
            else: blc =False
            #
            if bl_mode=='on': blc=True 
            
            
            
            #Note: conc_ul here is in the order of the filenames- unordered list
            #it has to be that way- otherwise filenames and concentrations are not aligned anymore
            
            # currently the second radical data is just a copy of the first-> solved 
            
            if param == 'r1':
        
                
                ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=False)
                concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.otherwise c is given by the order of filenames
                
                r1,T1_0,perc= prc.get_r(radical,concs,ex_dF['values'])
                #print(ex_dF)
                r1s.append(r1)
                x_opt,y_opt= prc.get_r.plotdata
                print(radical,prc.get_r.fit_report['rsquare'])
                
                pit(i,param,x_opt,y_opt,label=radical,color=spider_colors[k],alpha=0.5)
                pit(i,param,concs,[1/T for T in ex_dF['values']],color=spider_colors[k],marker='o')
                #axesA[i].plot(x_opt,y_opt,label=radical,color=spider_colors[k],alpha=0.5)
                #axesA[i].plot(concs,[1/T for T in ex_dF['values']],color=spider_colors[k],marker='o')
                
                
            elif param == 'r2':
                
                
                ex_dF= ex.extract_cwise(' T2',conc_ul,fnames,out=False)
                concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.otherwise c is given by the order of filenames
                
                r2,T2_0,perc= prc.get_r(radical,concs,ex_dF['values'])
                x_opt,y_opt= prc.get_r.plotdata
                
                r2s.append(r2)
                
                pit(i,param,x_opt,y_opt,label=radical,color=spider_colors[k],alpha=0.5)
                pit(i,param,concs,[1/T for T in ex_dF['values']],color=spider_colors[k],marker='o')
                
                #axesA[i].plot(x_opt,y_opt,label=radical,color=spider_colors[k],alpha=0.5)
                #axesA[i].plot(concs,[1/T for T in ex_dF['values']],color=spider_colors[k],marker='o')
                
            elif param == 'r1bar':
                
                barloc.append(i)
                break
            elif param == 'r2bar':
                
                barloc.append(i)
                
                break
                      
                
            #_____ plotted on AxesB[i] from now on  
            # somewhen implement passing the axis as an object and preselecting it at the beginning of the loop depending on i count.
            #see chatGPT help
                
            elif param ==' P1/2':
                ex_dF= ex.extract_cwise(' P1/2',conc_ul,fnames,out=False)
                concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.otherwise c is given by the order of filenames
                
                x_opt,y_opt,fit_params,errors,perc,rsquare=prc.lin_fit(ex_dF['values'].index,ex_dF['values'])
                
                pit(i,param,x_opt,y_opt,color=spider_colors[k])
                pit(i,param,concs,ex_dF['values'],yerror=ex_dF['dev'],linestyle=None,color=spider_colors[k],marker='o')
                
                P12_plist.append([radical,*fit_params, *errors,*perc, rsquare])
                
                
            elif param == 'cc':
                
                if radical.find('Trityl')!=-1: continue
            
                ccs,concs,errors=prc.get_cc(radical,conc_ul,fnames)# function takes unordered list, sorted concs are returned from the function. processing step takes place in extract_cwise
                pit(i,param,concs,ccs,yerror=errors,label=radical,color=spider_colors[k])
                
                
            elif param == 'smaxzeta':
                
                ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=False)
                concs=list(ex_dF.index)
                
                T1s=ex_dF['values']
                T1_0= prc.get_r(radical,concs,ex_dF['values'])[1]
                
                ex_dF2=ex.extract_cwise(' E_max',conc_ul,fnames,out=False,bl_corr=blc)
                E_max=list(ex_dF2['values'])
                smz=cf.get_smaxzeta(T1s,T1_0,E_max)
                
                pit(i,param,concs,smz,label=radical,color=spider_colors[k])
                
                
            elif param=='lf':
                
                ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=False)
                concs=list(ex_dF.index)
                
                T1s=ex_dF['values']
                T1_0= prc.get_r(radical,concs,ex_dF['values'])[1]
                
                lfs=[cf.leakage_factor(T1,T1_0) for T1 in T1s] 
            
                pit(i,param,concs,lfs,marker='o',color=spider_colors[k],label=radical)
                
            
            else: print( 'parameter can not be handled' )
                
        
        if i<6:   axesA[i].set_title(param)  
        elif i<12: axesB[i-6].set_title(param)
        
            
        
      
    axesA[barloc[0]].bar(abb[:len(r1s)],r1s,color=spider_colors[:len(r1s)])
    axesA[barloc[1]].bar(abb[:len(r1s)],r2s,color=spider_colors[:len(r1s)])
    #for b in barloc: axesA[b].set_title(param)
    axesA[0].legend()
    
    axesB[1].legend()
        
        
    
    
    #axesB[0].legend()
    #axesC[0].legend()s
        
        
        
    print('-----P_1/2 fit parameters--------')    
    P12_dF= pd.DataFrame(data=P12_plist,columns=['radical','slope','intercept','m_error','c_error','m_perc','c_perc','rsquare']) 
    print((P12_dF))
    
    return
