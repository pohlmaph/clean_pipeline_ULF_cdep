# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 10:14:10 2026

@author: marsg
"""
import load_default_params as ldp
import bin_extraction as ex
import processing_functions as prc

import pandas as pd

from matplotlib.pyplot import subplots

def tile_plot_prc(radicals,spider_colors,prc_params=ldp.prc_params,short_labels= ldp.short_labels): 
    
    
    # nested loop order is aligned with the spider plots. 
    # -> the plot takes values of different radicals for one parameter
    # i.E  one column at a at time. 
    # with the new dataFrame order this means looping over the same column index in different dataframes



    FigA,axeA=subplots(2,3,figsize=(16,9))
    FigA.suptitle('Radical_comp|processed parameters plot A ')
    axesA= axeA.reshape(-1)
    # FigB,axeB=subplots(2,3,figsize=(16,9))
    # FigB.suptitle('Radical_comp |parameter plot B')
    # axesB= axeB.reshape(-1)
    # FigC,axeC=subplots(2,3,figsize=(16,9))
    # FigC.suptitle('Radical_comp |parameter plot C')
    # axesC= axeC.reshape(-1)
    
    
    

    
    def handle_r1(colors=ldp.spider_colors,**kwargs):
        
        r1s    = kwargs['r1s']
        radical = kwargs['radical']
        
        
        ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=True)
        concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.otherwise c is given by the order of filenames
        
        r1,T1_0,perc= prc.get_r(radical,concs,ex_dF['values'])
        r1s.append(r1)
        x_opt,y_opt= prc.get_r.plotdata
        
        axesA[i].plot(x_opt,y_opt,label=radical,color=colors[k],alpha=0.5)
        axesA[i].plot([1/T for T in ex_dF['values']],color=colors[k],marker='o')
        
    def handle_r2(colors=ldp.spider_colors,**kwargs):
        
        r2s    = kwargs['r2s']
        radical = kwargs['radical']
        
        ex_dF= ex.extract_cwise(' T2',conc_ul,fnames,out=False)
        concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.otherwise c is given by the order of filenames
        
        r2,T2_0,perc= prc.get_r(radical,concs,ex_dF['values'])
        x_opt,y_opt= prc.get_r.plotdata
        
        r2s.append(r2)
        
        axesA[i].plot(x_opt,y_opt,label=radical,color=colors[k],alpha=0.5)
        axesA[i].plot(concs,[1/T for T in ex_dF['values']],color=colors[k],marker='o')
        
    def handle_P12(colors=ldp.spider_colors,**kwargs):
        
        P12_plist = kwargs['P12_plist'],
        radical   = kwargs['radical'],
        
        ex_dF= ex.extract_cwise(' P1/2',conc_ul,fnames,out=False)
        concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.otherwise c is given by the order of filenames
        
        x_opt,y_opt,fit_params,errors,perc,rsquare=prc.lin_fit(ex_dF['values'].index,ex_dF['values'])
        axesA[i].plot(x_opt,y_opt,color=colors[k],alpha=0.5)
        axesA[i].plot(concs,ex_dF['values'],color=colors[k],alpha=0.5)
        P12_plist.append([radical,*fit_params, *errors,*perc, rsquare])
    
    def handle_cc(colors=ldp.spider_colors,**kwargs):
        
        radical = kwargs['radical'],
        conc_ul = kwargs['conc_ul'],
        fnames =  kwargs['fnames']
        
        
        ccs,concs=prc.get_cc(radical,conc_ul,fnames)# function takes unordered list, sorted concs are returned from the function. processing step takes place in extract_cwise
        axesA[i].plot(concs,ccs,label=radical,color=colors[k])
        
    def handle_r1bar(colors=ldp.spider_colors,**kwargs):
        i=kwargs['i']
        barlocs=kwargs['barlocs']
        barlocs.append(i)
    def handle_r2bar(colors=ldp.spider_colors,**kwargs):
        i=kwargs['i']
        barlocs=kwargs['barlocs']
        barlocs.append(i)
    
    ### catalogue of parameters and respective handlers
    handlers={'r1': handle_r1,
              'r2': handle_r2,
              ' P_1/2': handle_P12,
              'cc': handle_cc,
              'r1bar': handle_r1bar,
              'r2bar':handle_r2bar
               }   
    
    # loop over parameters
    P12_plist=[]
    r1s=[]
    r2s=[]
    barlocs= []
    
    for i,param in enumerate(prc_params): #does the same job as a the classical i=i+1  construction
        
        #print('i=',i)
        print(param)
        for k,radical in enumerate(radicals):
            #print(radical)
            fnames,conc_ul=ex.load_files(radical)
            
            print(conc_ul)
            #Note: conc_ul here is in the order of the filenames- unordered list
            #it has to be that way- otherwise filenames and concentrations are not aligned anymore
            
            #print(fnames)
            
            
            
            
            if param in list(handlers.keys()):
                handler= handlers.get(param)
                handler(radical=radical,
                        r1s=r1s,
                        r2s=r2s,
                        P12_plist= P12_plist,
                        conc_ul=conc_ul,
                        fnames=fnames,
                        i=i
                        )
                
                        # passing keywords instead of arguments
                        # allows to pass generally all arguments to all handlers in one line , even if the specific handlers dont need some of them.
                        # "Gießkannenprinzip"
            else: print( 'parameter can not be handled' )           
            if param=='r1bar' or param=='r2bar':
                 break # breaks after first radical. Otherwise handler is called for each radical( k iteration)
                 # should be handled outside the loop
            

        axesA[i].set_title(param)    
        
            
            
            # if i<6: 
            #     axesA[i].plot(ex_dF['values'],marker='o',color=spider_colors[k],label=radical)
            #     axesA[i].set_title(param)
            #     axesA[i].set_xlabel('concentration')
            #     #axesA[i].set_ylabel(ylabels[i])
                
            # elif i<12:
            #     axesB[i-6].plot(ex_dF['values'],marker='o',color=spider_colors[k],label=radical)
            #     axesB[i-6].set_title(param)
            #     axesB[i-6].set_xlabel('concentration')
            # elif i<18:
            #     axesC[i-12].plot(ex_dF['values'],marker='o',color=spider_colors[k],label=radical)
            #     axesC[i-12].set_title(param)
            #     axesC[i-12].set_xlabel('concentration')
            #else:   break
           
        
    print(barlocs)
    
    
    axesA[barlocs[0]].bar(radicals,r1s,color=spider_colors[i],label=short_labels)
    axesA[barlocs[1]].bar(radicals,r2s,color=spider_colors[i],label=short_labels)
    axesA[0].legend()
    #axesB[0].legend()
    #axesC[0].legend()s
        
        
        
    print('-----P_1/2 fit parameters--------')    
    P12_dF= pd.DataFrame(data=P12_plist,columns=['radical','slope','intercept','m_error','c_error','m_perc','c_perc','rsquare']) 
    print((P12_dF))
    

