# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:24:44 2026

@author: marsg
"""

import bin_extraction as ex
import load_default_params as ldp
import tile_plot_params as tpp
#%% set user defined initial parameters 


#directory stuff
raw_dir,process_dir,parent=ex.get_paths() #returns file paths for all folders to global space

#out: paths
#%% determine and debug sweep parameters

#load single file for getting params

radical_path, fnames, concs,parameters = ex.load_single_file()
radicals=ex.get_radicals()

print('radicals:',radicals)
print('concs:', concs )

#returns fnames, concs, parameters, radicals
#%% tile plot

prc_params = ['r1','r2','r1bar','r2bar',' P1/2','cc','smaxzeta','lf']

abb=ldp.gen_abbreviations(radicals,old=False)  

tpp.tile_plot_raw(radicals,parameters,ldp.spider_colors,old=False)
tpp.tile_plot_prc(radicals,ldp.spider_colors,prc_params=prc_params,abb=abb,old=False)

#import tile_plot_prc_clean as tppc
#tppc.tile_plot_prc(radicals,spider_colors,prc_params=prc_params,short_labels= ldp.short_labels)

#%% spider plots

import spider_plot as spp
#short_labels=['A-14','A14o','O-15N-o','O-15N-o']
short_labels=ldp.gen_short_labels(radicals)
#short_labels=['NH2-14','NH2-15N','Oxo-14N','Oxo-15N', 'TEMPO','Hydroxy']
spp.spider_plots(radicals, short_labels=short_labels,sel_params=[' E_max', ' P1/2',' b1', ' T1'],norm_to=-1)
#%% fixed_power_plot

import fixed_P_plot as fpp

powers=[1,1.5,2,5,7,8.5,20]

fpp.fixed_p_plot(radicals,powers,old=True)

#%%power sweeps

# for radical in radicals: 

#     fpp.power_sweep_fit(radical,20)



