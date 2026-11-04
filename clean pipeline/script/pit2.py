# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:55:08 2026

@author: marsg
"""

#_______________________   
def pit(ax,param,x,y,yerror=None,linestyle='-',title=None,**kwargs):#plot in tile
    # small handler for gathering all repetitive plotting commands. 
    # plotting options are available with keywords: 
    
    # linestyle=None: turns into scatter plot
    # marker= 'o': bullet points for markers
    # yerror = None: takes an array with y errors corresponding to y, usually originating from ex_dF['errors']. 
    #                default is None, deactivating the errorbars

            
            if title: ax.set_title(param)
            else:     ax.set_title(title)
            
            
            ax.set_xlabel('concentration in mM')
                            
            kwargs['marker']=None #setting a marker keyword overrides the errorbars. if markers are desired, they can be added by an second ax.scatter command
            ax.errorbar(x,y,yerr=yerror,**kwargs)
            #ax.plot(x,y,**kwargs)
                # Note that unintuitively ax.errorbar includes not only errorbars but also a standard line plot as expected from ax.plot
#_____________________________    