# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:36:00 2026

@author: marsg
"""



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

#prints three windows with 3x2 tile plots. 
#Each parameter in the csv files is plotted over concentration. 
#no processing here, the little fit for P_1/2 is inactivated here
# console returns you statis

def tile_plot_raw(radicals,parameters,passed_colors,old=True,bl_mode='old'): 


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
    
    print('----tile_plot_raw-----------')
    print('baseline_mode: '+ bl_mode)
    #prints the bl_mode passed to the function-> useful for debugging
    #recheck position!!
    i=0   
    for param in parameters:
        k=0
        if i >= len(all_axes): break
        ax= all_axes[i]
        
        for radical in radicals:
            
            
            # some conditions that were not ruled globally yet.. 
            
            if radical.find('old')!=-1 and bl_mode!= 'off':
                blc= True
               # print( f"baseline_correction enabled for {radical}")
                
                if old==False: continue # omits old data
            else: blc =False
            #
            if bl_mode=='on': blc=True 
            
            
            #extracts data from multiple csv_files into one single iterable dataFrame: ex_dF
        
            fnames,conc=ex.load_files(radical)# loads the file
            ex_dF= ex.extract_cwise(param,conc,fnames,out=False,bl_corr=blc)
            concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
            
        
            
            
            
                
            # adds a fitted line-> currently deactivated
            # if param==' P1/2':
            #     x_opt,y_opt,fit_params,errors,perc,rsquare=prc.lin_fit(ex_dF['values'].index,ex_dF['values'])
            #     axesA[i].plot(x_opt,y_opt,alpha=0.5)#color=passed_colors[k]
                
            #     P12_plist.append([radical,*fit_params, *errors,*perc, rsquare])
                
            
           
            # This is the plotting line. Note that errorbar also includes the standard line plot associoated with ax.plot
            
            ax.errorbar(concs,ex_dF['values'],yerr= ex_dF['dev'],label=radical,color=passed_colors[k]) 
            ax.set_title(param)
            ax.set_xlabel('concentration')
            
            k=k+1
        i=i+1
        
    axesA[0].legend()
    axesB[0].legend()
        #axesC[0].legend()
        
          
    # print('-----P_1/2 fit parameters--------')    
    # P12_dF= pd.DataFrame(data=P12_plist,columns=['radical','slope','intercept','m_error','c_error','m_perc','c_perc','rsquare']) 
    # print((P12_dF))
    
    return all_axes

# by returning the all_axes array you can modify the axes from the console

#%% tile plot processed


# contains a lot of handling functions for any processed parameters. All parameters given in prc_params will be used. 

def tile_plot_prc(radicals,passed_colors,prc_params,short_labels= None,abb=None,old =True,bl_mode='old'): 
    
    print('----tile_plot prc-----------')
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
    
    all_axes=list(axesA)+list(axesB)
   
#_______________________   
    def pit(ax,param,x,y,yerror=None,linestyle='-',**kwargs):#plot in tile
        # small handler for gathering all repetitive plotting commands. 
        # plotting options are available with keywords: 
        
        # linestyle=None: turns into scatter plot
        # marker= 'o': bullet points for markers
        # yerror = None: takes an array with y errors corresponding to y, usually originating from ex_dF['errors']. 
        #                default is None, deactivating the errorbars
    
                
                ax.set_title(param)
                ax.set_xlabel('concentration')
                                
                kwargs['marker']=None #setting a marker keyword overrides the errorbars. if markers are desired, they can be added by an second ax.scatter command
                ax.errorbar(x,y,yerr=yerror,**kwargs)
                #ax.plot(x,y,**kwargs)
                    # Note that unintuitively ax.errorbar includes not only errorbars but also a standard line plot as expected from ax.plot
#_____________________________    


    P12_plist=[]
    r1s=[]
    r2s=[]
    barloc= []
    T1_0=[]
    
    
    ## loop over parameters
    
    i=0
    for i,param in enumerate(prc_params):
        
        #print('i=',i)
        #print(param)
        if i>11: break
        ax=all_axes[i]
    
        if param == 'r1': print('--- these are the r^2-values for the r1 fit---')# this seems random but has to  be exactly in this place to sort conosle output
        
        ##loop over radicals
        for k,radical in enumerate(radicals):
            #print(radical)
            fnames,conc_ul=ex.load_files(radical)
            
            #Note: conc_ul here is in the order of the filenames- i.e. an unordered list
            #it has to be that way- otherwise filenames and concentrations are not aligned anymore
            # ordering happens in extract_cwise, when the values extracted from the filenames and concentrations are linked in a dataFrame
            
            ## condtions relevant only if bl_mode = 'old':
              
            if radical.find('old')!=-1 and bl_mode!= 'off':
                blc= True
               # print( f"baseline_correction enabled for {radical}")
            else: blc =False
            
            #if radical.find('old')!=-1 and old==False: continue # omits old data
            if bl_mode=='on': blc=True
            else: pass
            

            
            if param == 'r1':
        
                
                ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=False)
                concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.otherwise c is given by the order of filenames
                
                r1,T1_0,perc= prc.get_r(radical,concs,ex_dF['values'])
                #print(ex_dF)
                r1s.append(r1)
                x_opt,y_opt= prc.get_r.plotdata
                print(radical,'r^2= ', prc.get_r.fit_report['rsquare'])
                
                pit(ax,param,x_opt,y_opt,label=radical,alpha=0.5,color=passed_colors[k]) 
                pit(ax,param,concs,[1/T for T in ex_dF['values']],marker='o',color=passed_colors[k]) 
                
                
                
            elif param == 'r2':
                
                
                ex_dF= ex.extract_cwise(' T2',conc_ul,fnames,out=False)
                concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.otherwise c is given by the order of filenames
                
                r2,T2_0,perc= prc.get_r(radical,concs,ex_dF['values'])
                x_opt,y_opt= prc.get_r.plotdata
                
                r2s.append(r2)
                
                pit(ax,param,x_opt,y_opt,label=radical,alpha=0.5,color=passed_colors[k])
                pit(ax,param,concs,[1/T for T in ex_dF['values']],marker='o',color=passed_colors[k])
                
                
            elif param == 'r1bar':
                
                barloc.append(i) # store the location for the bar plot. Basically this corresponds to the position of 'r1bar' in the prc_params list.
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
                
                pit(ax,param,x_opt,y_opt,color=passed_colors[k])
                pit(ax,param,concs,ex_dF['values'],yerror=ex_dF['dev'],linestyle=None,marker='o',color=passed_colors[k])
                
                P12_plist.append([radical,*fit_params, *errors,*perc, rsquare])
                
                
            elif param == 'cc':
                
                if radical.find('Trityl')!=-1: continue
            
                ccs,concs,errors=prc.get_cc(radical,conc_ul,fnames)# function takes unordered list, sorted concs are returned from the function. processing step takes place in extract_cwise
                pit(ax,param,concs,ccs,yerror=errors,label=radical,color=passed_colors[k])
                
                
            elif param == 'smaxzeta':
                
                ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=False)
                concs=list(ex_dF.index)
                
                T1s=ex_dF['values']
                T1_0= prc.get_r(radical,concs,ex_dF['values'])[1]
                
                ex_dF2=ex.extract_cwise(' E_max',conc_ul,fnames,out=False,bl_corr=blc)
                E_max=list(ex_dF2['values'])
                smz=cf.get_smaxzeta(T1s,T1_0,E_max)
                
                pit(ax,param,concs,smz,label=radical,color=passed_colors[k])
                
                
            elif param=='lf':
                
                ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=False)
                concs=list(ex_dF.index)
                
                T1s=ex_dF['values']
                T1_0= prc.get_r(radical,concs,ex_dF['values'])[1]
                
                lfs=[cf.leakage_factor(T1,T1_0) for T1 in T1s] 
            
                pit(ax,param,concs,lfs,marker='o',label=radical,color=passed_colors[k]) 
                
            
            else: print( 'parameter can not be handled' )
                
         
        ax.set_title(param)  
        
    #loop end    
    
    
    if abb==None: 
    
        abb=ldp.get_abbreviations(radicals)
    
    ## create the bar plots 
    # loop end    
    
    # 1. Create a dictionary to assign lists to columns, including colors
    bar_dF = pd.DataFrame(
        data={
            'r1s': r1s, 
            'r2s': r2s, 
            'colors': passed_colors[:len(r1s)]
        }, 
        index=abb[:len(r1s)]
    )
    
    # 2. Sort the DataFrame by r1s
    bar_dF = bar_dF.sort_values('r1s')
        
    # 3. Plot using the newly sorted index, values, and colors
    all_axes[barloc[0]].bar(bar_dF.index, bar_dF['r1s'], color=bar_dF['colors'])
    all_axes[barloc[1]].bar(bar_dF.index, bar_dF['r2s'], color=bar_dF['colors'])
    
    all_axes[barloc[0]].axhline(bar_dF['r1s']['H-14'],color= bar_dF['colors']['H-14'])
    all_axes[barloc[1]].axhline(bar_dF['r2s']['H-14'],color= bar_dF['colors']['H-14'])
    
    # 4. Rotate labels by 45 degrees and shrink font size slightly (default is usually 10)
    all_axes[barloc[0]].tick_params(axis='x', rotation=45, labelsize=9)
    all_axes[barloc[1]].tick_params(axis='x', rotation=45, labelsize=9)
    
    all_axes[0].legend()
    all_axes[7].legend()
    
    #axesB[1].legend()
    
        

        
    print('-----P_1/2 fit parameters--------')    
    P12_dF= pd.DataFrame(data=P12_plist,columns=['radical','slope','intercept','m_error','c_error','m_perc','c_perc','rsquare']) 
    print((P12_dF))
    
    FigA.tight_layout()
    FigB.tight_layout()
    return all_axes
    # by returning the all_axes array you can modify the axes from the console 