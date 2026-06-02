# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:24:44 2026

@author: marsg
"""
# Code was stored into modules. Inside each modules you find functions and default parameters. 
#When changing th dataset, doublecheck load_default_params- if youre default params need to be updated.

# I recommend to check out the keywords for custom functions: I implemented typical problems for data analysis into keywords. 
#I wanted to documented them all, but if you see this code, it might have not occurred yet- so maybe quickly the check the function definition statement


#%%
# #%% if activated checks which code lines spam your console. ( credits to ChatGPT)
#restart the console for to apply deactivation
# helpful for debugging not relevant for pipeline

# import builtins
# import inspect

# old_print = builtins.print

# def traced_print(*args, **kwargs):
#     frame = inspect.currentframe().f_back

#     filename = frame.f_code.co_filename
#     lineno = frame.f_lineno
#     func = frame.f_code.co_name

#     old_print(
#         f"\n[PRINT from {filename}:{lineno} in {func}]",
#         *args,
#         **kwargs
#     )

# builtins.print = traced_print
#%%

import bin_extraction as ex 
import load_default_params as ldp
import tile_plot_params as tpp
import single_plot as sp

from matplotlib.pyplot import subplots
#%% set user defined initial parameters 

#old_glob= False #serves as a central switch: automatically sets the keywords for all following functions
# implement radicals= old_Radicals/new_radicals/ both  instead of skipping steps in the loop. 
bl_glob='off'
# 'on','off', or 'old'
#('old' enables baseline correction only for data tagged with old in the radical name )  
print('global baseline mode: '+ bl_glob)


#baseline correction: The measured signal(integral of proton spectrum) with Hyperpolarization (RFAamp)  
#is normalized to the signal without HP(RFoff) for each concentration. 
#baseline correction uses the average over all concentrations instead of individual values


#directory stuff
raw_dir,process_dir,parent=ex.get_paths() #returns file paths for all folders to global space

#out: paths
#%% determine and debug sweep parameters

#load single file for getting params. This cell has to be executed before the tile plots.

radical_path, fnames, concs,parameters = ex.load_single_file()
radicals=ex.get_radicals()

radicals=ex.sort_radicals(False,True,radicals)# args: old,new,radicals 
# this allows you to use subsets of radical datasets, consisting of 1st generation, 2nd generation or both 
#cp and Oxo only exist in new generation 

# loads these groups in the MAIN wordspace in case you want to manually adress them
old_radicals=ex.get_old_radicals(radicals)
new_radicals=ex.get_new_radicals(radicals)

print('radicals:',radicals)
print('concs:', concs )



#print('popped out: ' + radicals.pop(-1))
    # this line can be used to delete radicals from the list by index



#%% tile plot


prc_params = ['r1','r2','r1bar','r2bar',' P1/2','cc','smaxzeta','lf']
# 1/T1,2 plots,  relaxivities as bar plots, P_1,2(c), coupling factors multiplied with s_max, leakage factor, 
abb=ldp.gen_abbreviations(radicals)  
# the names in radicals are too long for plot names. This method generates short abbreviations from the radical names. 
#

#plots all parameters as they are into 3x2 plot
axes_raw=tpp.tile_plot_raw(radicals,parameters,ldp.spider_colors,old=True,bl_mode=bl_glob)
    # returns the axes so you can modify from the console

#axes[3].set_ylim(-300,0)

#plots a bunch of processed parameters given by prc_params
axes_prc=tpp.tile_plot_prc(new_radicals,ldp.spider_colors,prc_params=prc_params,abb=abb,old=True,bl_mode=bl_glob)

#import tile_plot_prc_clean as tppc
#tppc.tile_plot_prc(radicals,spider_colors,prc_params=prc_params,short_labels= ldp.short_labels)

#%% spider plots

# nice to produce publication-ready plots.

#needs to be updated
# check label positions 
# for some reason norm_to does not change the plot


import spider_plot as spp
#short_labels=['A-14','A14o','O-15N-o','O-15N-o']
short_labels=ldp.gen_short_labels(radicals,old=True)
#short_labels=['NH2-14','NH2-15N','Oxo-14N','Oxo-15N', 'TEMPO','Hydroxy']
spp.spider_plots(radicals,short_labels,sel_params=[' E_max', ' P1/2',' b1', ' T1'],norm_to=-3)
#%% fixed_power_plot

import fixed_P_plot as fpp

powers=[2,5,6,8,10,15,20,50]

# create fp_plots for different bl_modes and generations

#fpp.fixed_p_plot(old_radicals,powers,bl_mode='on')
#fpp.fixed_p_plot(new_radicals,powers,bl_mode='on')
axes_fp=fpp.fixed_p_plot(new_radicals,powers,bl_mode='off')

axes_fp[0].set_ylim(-60,0) #just an experience value 
#%%power sweeps

# one plot per radical contaiing each power sweep for all concentrations
# reconstructed from the fit! no raw data included

# for radical in radicals: 

#     fpp.power_sweep_fit(radical,20)

#%% figure for Kai,  
Fig, axes =subplots(2,3,figsize=(16,9))

sp.single_plot(axes[0,0],' E_max', new_radicals, bl_mode='on',number=1)
sp.single_plot(axes[1,0],' E_max', new_radicals, bl_mode='off',number=4)
sp.single_plot(axes[0,1],' E_max', old_radicals, bl_mode ='on',number=2)    
sp.single_plot(axes[1,1],' baseline', new_radicals, bl_mode='off',number=5) 
sp.single_plot(axes[1,2],' baseline', old_radicals, bl_mode='off',number=6) 
sp.single_plot(axes[0,2],' E_max', new_radicals, bl_mode='constant',number =3)
# sp.single_plot(axes[1,1],' E_max', radicals,old=True, bl_mode='on')
for ax in axes.reshape(-1): ax.set_ylim(-300,0)
for ax in axes.reshape(-1)[4:6]: 
    ax.set_ylim(0,30)#
    ax.text(1,1,'baseline')

#%%
import signal_plot as sigp

#sigp.signal_plot(new_radicals, bl_mode='on')
sigp.signal_plot(old_radicals, bl_mode='on')
# #%% print ex_dF for all radicals
# for radical in radicals: 
    
#     fnames,concs= ex.load_files(radical)
#     print(ex.extract_cwise(' baseline',concs,fnames,out=False,bl_corr='on'))

