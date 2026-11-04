# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 10:10:12 2026

@author: marsg
"""
from matplotlib.pyplot import subplots

import bin_extraction as ex 
import load_default_params as ldp
import processing_functions as prc





def cc_plot(radicals,ax_titles=[r'$ \mathrm{Prepolarization\/field\/B_p}$',r'Hyperfine splitting'], passed_colors=ldp.spider_colors,bl_mode='old'):
    
    Fig,axe=subplots(1,2,figsize=(10,4),dpi=300)

    
    params=[' x1','cc']
    #_______________________   
    def pit(ax,param,x,y,yerror=None,linestyle='-',**kwargs):#plot in tile
        # small handler for gathering all repetitive plotting commands. 
        # plotting options are available with keywords: 
        
        # linestyle=None: turns into scatter plot
        # marker= 'o': bullet points for markers
        # yerror = None: takes an array with y errors corresponding to y, usually originating from ex_dF['errors']. 
        #                default is None, deactivating the errorbars
    
                
                ax.set_title(param)
                ax.set_xlabel('concentration in mM')
                                
                kwargs['marker']=None #setting a marker keyword overrides the errorbars. if markers are desired, they can be added by an second ax.scatter command
                ax.errorbar(x,y,yerr=yerror,**kwargs)
                #ax.plot(x,y,**kwargs)
                    # Note that unintuitively ax.errorbar includes not only errorbars but also a standard line plot as expected from ax.plot
    #_____________________________    
    
    i=0
    for i,param in enumerate(params):
        
        
        ax=axe[i]
    
        
        
        ##loop over radicals
        k=0
        for k,radical in enumerate(radicals):
            #print(radical)
            fnames,conc_ul=ex.load_files(radical)
            
            #Note: conc_ul here is in the order of the filenames- i.e. an unordered list
            #it has to be that way- otherwise filenames and concentrations are not aligned anymore
            # ordering happens in extract_cwise, when the values extracted from the filenames and concentrations are linked in a dataFrame
            
            ## conditions relevant only if bl_mode = 'old':
              
            if radical.find('old')!=-1 and bl_mode!= 'off':
                blc= True
               # print( f"baseline_correction enabled for {radical}")
            else: blc =False
            
            #if radical.find('old')!=-1 and old==False: continue # omits old data
            if bl_mode=='on': blc=True
            
        
            if param == 'cc':
                
                if radical.find('Trityl')!=-1: continue
            
                ccs,concs,errors=prc.get_cc(radical,conc_ul,fnames)# function takes unordered list, sorted concs are returned from the function. processing step takes place in extract_cwise
                pit(ax,ax_titles[i],concs,ccs,yerror=errors,label=radical[:-4],color=passed_colors[k])
            elif param==' x1':
            
                ex_dF= ex.extract_cwise(param,conc_ul,fnames,out=False,bl_corr=blc)
                concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
                
                
                pit(ax,ax_titles[i],concs,ex_dF['values'],yerror= ex_dF['dev'],label=radical[:-4],color=passed_colors[k])
    axe[1].legend(fontsize=9,loc='lower right')
                
                
            