# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 18:19:52 2026

@author: marsg
"""

import bin_extraction as ex

from matplotlib.pyplot import subplots
import numpy as np
from math import pi
#%% spider plots

#TODO
#put keyword absolute= False ?
#put keyword norm_to= -2
#take short_labels as optional arguments
#include all radicals

#solve structural problem: Where generate r1 and other processed parameters ( coupling constants)
    # when generate ex_dF

#take colors as spider colors colors


#default values pastebin

#sel_params=[' E_max', ' P1/2',' b1', ' T1']

#short_labels=['NH2-14','NH2-15N', 'Hydroxy', 'Oxo-14N','Oxo-15N', 'TEMPO']

#short_labels=['NH2-14','NH2-14N']

def spider_plots(radicals,short_labels,sel_params=[' E_max', ' P1/2',' b1', ' T1'], absolute= False, norm_to= -3):

    Fig_spider,axe_spider= subplots(2,2,figsize=(14,14),subplot_kw={'projection': 'polar'}) 
    axes_spider=axe_spider.reshape(-1)
    Fig_spider.suptitle('individual parameter values normalized to TEMPO',fontsize=25)
    
    
    Fig_spider_2,axe_spider_2= subplots(figsize=(10,10),subplot_kw={'projection': 'polar'}) 
    Fig_spider_2.suptitle('Parameter values normalized to TEMPO ',fontsize=25)
    
    
    
    
    polygons= sel_params# polygons representing one parameter
    N = len(radicals)
    labels= radicals
    
    
    angles= [2*pi*n/N for n in np.linspace(0,N,N,endpoint=False)]
    angles += angles[:1] 
    
    par_names=['E_max', 'P_1/2','linewidth', 'longitudinal relaxivity']
    spider_colors=['#eba750','#a740bc','#408dbc','#40bcaa' ]
    
    
    #hb_dF_norm= hb_dF/hb_dF.iloc[-1]
    
    
    
    #print('raw')
    #print(hb_dF)
    #print("normalized to TEMPO: ")
    #print(hb_dF_norm) 
    
    
    
    
    i=0
    for polygon in polygons:
        k=0
        values=[]
        for radical in radicals:
            
            
            fnames,conc=ex.load_files(radical)
            
            # currently the second radical data is just a copy of the first
            
            ex_dF= ex.extract_cwise(polygon,conc,fnames,out=False)
            concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
            
            #exception until r1 is correctly implemented  
            if polygon==' T1': values.append(1/(ex_dF['values'].loc[2.0]))
                
            else: values.append(ex_dF['values'].loc[2.0])
            k=k+1
        values.append(values[0])# duplicate first item to close the circle (specialty of polar plots )
        
        if absolute == False: 
            values=[value/values[norm_to] for value in values]
             
        
        # Erste Achse nach oben
        # axes_spider[i].set_theta_offset(pi / 2)
        # axes_spider[i].set_theta_direction(-1)
        
        axes_spider[i].plot(angles,values,linewidth=4,color=spider_colors[i])
        axes_spider[i].set_title(par_names[i], fontsize=24, color=spider_colors[i],pad=40)
        
        axes_spider[i].set_thetagrids([angle*(360/(2*pi))for angle in angles][:-1],short_labels,fontsize=20)
        #axes_spider[i].set_xticklabels([])
        axes_spider[i].tick_params(axis='x', pad=20) 
            
        
        # label adjustments deactivated until all data is included
        
        # labels_obj = axes_spider[i].get_xticklabels()
        # # 1st label left-aligned
        # labels_obj[0].set_horizontalalignment('left')
        # # 4th label right-aligned
        # labels_obj[3].set_horizontalalignment('right')
    
        # all in one plot
        
        #has to be normalized anyway
        values_norm= [value/values[-3] for value in values]
        axe_spider_2.plot(angles,values_norm, label=par_names[i],linewidth=3, color=spider_colors[i])
        axe_spider_2.set_thetagrids([angle*(360/(2*pi))for angle in angles][:-1],labels,fontsize=20)
        axe_spider_2.tick_params(axis='x', pad=40) 
        
        # labels_obj = axe_spider_2.get_xticklabels()
        # # 1st label left-aligned
        # labels_obj[0].set_horizontalalignment('left')
        # # 4th label right-aligned
        # labels_obj[3].set_horizontalalignment('right')
        
        # pos0 = labels_obj[0].get_position()
        # labels_obj[0].set_position((pos0[0], pos0[1] + 0.03))  # outward shift
        # i=i+1
        
        # pos3 = labels_obj[3].get_position()
        # labels_obj[3].set_position((pos3[0], pos3[1] + 0.03))  # outward shift
    
        i=i+1
    
    
    # Get all radial grid lines for each figure
    #works only for full dataset
    
    # radial_grids = axe_spider_2.yaxis.get_gridlines()
    # radial_grids1 = axe_spider.yaxis.get_gridlines()
    # # Find the gridline corresponding to r = 1
    # # (gridline order corresponds to tick order)
    # r_ticks = axe_spider_2.get_yticks()
    # r_ticks1 = axe_spider.get_yticks()
    
    # for tick_value, gridline in zip(r_ticks, radial_grids):
    #     if np.isclose(tick_value, 1.0):          # the ring at r = 1
    #         #gridline.set_color('black')
    #         gridline.set_linewidth(3)
    #         break
        
    # for tick_value, gridline in zip(r_ticks1, radial_grids1):
    #     if np.isclose(tick_value, 1.0):          # the ring at r = 1
    #         #gridline.set_color('black')
    #         gridline.set_linewidth(3)
    #         break
    
        
    Fig_spider.tight_layout()
    axe_spider_2.legend(loc=(0.95,0),fontsize=15)