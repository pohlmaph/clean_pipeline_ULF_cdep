# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:24:44 2026

@author: marsg
"""

import bin_extraction as ex
import load_default_params as ldp
import tile_plot_params as tpp
import single_plot as sp

from matplotlib.pyplot import subplots
#%% set user defined initial parameters 

old_glob= False

bl_glob='on'
# 'on','off', or 'old'
#('old' enables baseline correction only for data tagged with old in the radical name )  


#directory stuff
raw_dir,process_dir,parent=ex.get_paths() #returns file paths for all folders to global space

#out: paths
#%% determine and debug sweep parameters

#load single file for getting params

radical_path, fnames, concs,parameters = ex.load_single_file()
radicals=ex.get_radicals()



print('radicals:',radicals)
print('concs:', concs )

#print('popped out: ' + radicals.pop(-1))
#returns fnames, concs, parameters, radicals
#%% get old _radicals
def get_old_radicals(radicals):
    old_radicals=[]
    for radical in radicals: 
        
        if radical.find('old')!= -1: 
            old_radicals.append(radical)
    return old_radicals
    
old_radicals=get_old_radicals(radicals)

#%% tile plot

prc_params = ['r1','r2','r1bar','r2bar',' P1/2','cc','smaxzeta','lf']

abb=ldp.gen_abbreviations(radicals,old=old_glob)  

axes=tpp.tile_plot_raw(radicals,parameters,ldp.spider_colors,old=old_glob,bl_mode=bl_glob)
axes[3].set_ylim(-300,0)
#tpp.tile_plot_prc(radicals,ldp.spider_colors,prc_params=prc_params,abb=abb,old=old_glob,bl_mode=bl_glob)

#import tile_plot_prc_clean as tppc
#tppc.tile_plot_prc(radicals,spider_colors,prc_params=prc_params,short_labels= ldp.short_labels)

#%% spider plots

import spider_plot as spp
#short_labels=['A-14','A14o','O-15N-o','O-15N-o']
short_labels=ldp.gen_short_labels(radicals,old=old_glob)
#short_labels=['NH2-14','NH2-15N','Oxo-14N','Oxo-15N', 'TEMPO','Hydroxy']
spp.spider_plots(radicals,short_labels,sel_params=[' E_max', ' P1/2',' b1', ' T1'],norm_to=-1)
#%% fixed_power_plot

import fixed_P_plot as fpp

powers=[2,5,6,8,10,15,20,50]

fpp.fixed_p_plot(old_radicals,powers,old=True,bl_mode='on')
fpp.fixed_p_plot(radicals,powers,old=False,bl_mode='on')
fpp.fixed_p_plot(radicals,powers,old=False,bl_mode='off')

#%%power sweeps

# for radical in radicals: 

#     fpp.power_sweep_fit(radical,20)

#%% figure for Kai
Fig, axes =subplots(2,3,figsize=(16,9))

sp.single_plot(axes[0,0],' E_max', radicals,old=False, bl_mode='on',number=1)
sp.single_plot(axes[1,0],' E_max', radicals,old=False, bl_mode='off',number=4)
sp.single_plot(axes[0,1],' E_max', old_radicals,old=True, bl_mode='on',number=2)    
sp.single_plot(axes[1,1],' baseline', radicals, old=False, bl_mode='off',number=5) 
sp.single_plot(axes[1,2],' baseline', old_radicals, old=True, bl_mode='off',number=6) 
sp.single_plot(axes[0,2],' E_max', radicals, old=False, bl_mode='constant',number =3)
# sp.single_plot(axes[1,1],' E_max', radicals,old=True, bl_mode='on')
for ax in axes.reshape(-1): ax.set_ylim(-300,0)
for ax in axes.reshape(-1)[4:6]: 
    ax.set_ylim(0,30)#
    ax.text(1,1,'baseline')

#%%
import signal_plot as sigp

sigp.signal_plot(radicals, old=False, bl_mode='on')



