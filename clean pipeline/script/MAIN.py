# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:24:44 2026

@author: marsg
"""




import bin_extraction as ex
import load_default_params as ldp
import tile_plot_params as tpp
#%% set user defined initial parameters 

#concs=[0.25,0.5,12,1,2,4,6,8]
Powers=[1,1.5,2,10]


spider_colors=['#eba750','#a740bc','#408dbc','#40bcaa','blue','yellow' ]


raw_dir,process_dir,parent=ex.get_paths() #returns file paths for all folders to global space


#out: paths

#%% determine and debug sweep parameters

#load single file for getting params



radical_path=ex.get_radicals(path=True)
fnames,concs=ex.load_files(ex.get_radicals()[0])
parameters= ex.get_pnames(fnames[0]) # fix fnames-> 
#parameters[4]=' P_12'
print("parameters:", parameters)

radicals=ex.get_radicals()

print('radicals:',radicals)
print('concs:', concs )


#returns fnames, concs, parameters, radicals
#%% tile plot

 


prc_params = ['r1','r2','r1bar','r2bar',' P1/2','cc','smaxzeta','lf']
#tpp.tile_plot_raw(radicals,concs,parameters, spider_colors)
tpp.tile_plot_prc(radicals,spider_colors,prc_params=prc_params)

#import tile_plot_prc_clean as tppc
#tppc.tile_plot_prc(radicals,spider_colors,prc_params=prc_params,short_labels= ldp.short_labels)


#%% spider plots

import spider_plot as spp
short_labels=['NH2-14','NH2-15N','Oxo-14N','Oxo-15N', 'TEMPO','Hydroxy']
spp.spider_plots(radicals, short_labels=short_labels,sel_params=[' E_max', ' P1/2',' b1', ' T1'])
#%%
#TODO next: first, spider plots, r1

