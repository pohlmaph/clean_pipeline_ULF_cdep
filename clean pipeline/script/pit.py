# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 10:00:22 2026

@author: marsg
"""

def pit(i,param,x,y,scatter=False,**kwargs):#plot in tile
    
    if scatter==False:
        
        if i<6: 
            axesA[i].plot(x,y,*kwargs)
            axesA[i].set_title(param)
            axesA[i].set_xlabel('concentration')
            #axesA[i].set_ylabel(ylabels[i])
            
        elif i<12:
            axesB[i-6].plot(x,y,*kwargs)
            axesB[i-6].set_title(param)
            axesB[i-6].set_xlabel('concentration')
        # elif i<18:
        #     axesC[i-12].plot(concs,ex_dF['values'],marker='o',color=spider_colors[k],label=radical)
        #     axesC[i-12].set_title(param)
        #     axesC[i-12].set_xlabel('concentration')
    
    if scatter == True:
        
        if i<6: 
            axesA[i].scatter(x,y,*kwargs)
            axesA[i].set_title(param)
            axesA[i].set_xlabel('concentration')
            #axesA[i].set_ylabel(ylabels[i])
            
        elif i<12:
            axesB[i-6].scatter(x,y,*kwargs)
            axesB[i-6].set_title(param)
            axesB[i-6].set_xlabel('concentration')