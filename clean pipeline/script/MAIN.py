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
import numpy 
import pandas 



from matplotlib.pyplot import subplots
from matplotlib.pyplot import Figure

#%% set user defined initial parameters 

#old_globserves as a central switch: automatically sets the keywords for all following functions

bl_glob='constant'
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

radicals=ex.sort_radicals(True,False,radicals)# args: old,new,radicals 
# this allows you to use subsets of radical datasets, consisting of 1st generation, 2nd generation or both 
#cp and Oxo only exist in new generation 

# loads these groups in the MAIN wordspace in case you want to manually adress them
#old_radicals=ex.get_old_radicals(radicals)
#new_radicals=ex.get_new_radicals(radicals)

#%% storage for code lines to remove radicals from the list
# caution: some downstream functionalities  or T10-averaging require all radicals
# double check before implementing



custom_radicals= radicals
# print("popped:",custom_radicals.pop(custom_radicals.index('4-Amino-14N-TEMPO_old')))
# print("popped:",custom_radicals.pop(custom_radicals.index('4-Oxo-15N-TEMPO_old')))
# print("popped:",custom_radicals.pop(custom_radicals.index('4-Hydroxy-14N-TEMPO_old')))

#skip_radicals is  passed to functions which require all radicals for some calculations but skip the given radicals for the final purpose

skip_radicals= ['4-Amino-14N-TEMPO_old','4-Oxo-15N-TEMPO_old','4-Hydroxy-14N-TEMPO_old']
#skip_radicals= ['4-Amino-15N-TEMPO', '3-Carboxy-14N-Proxyl','Oxo71-Trityl','4-Hydroxy-14N-TEMPO','4-Oxo-15N-TEMPO_3_26',]
#skip_radicals=[]
# for radical in radicals: 
#     if radical.find('14N') !=-1:
#         print(radicals.pop(radicals.index(radical)))
#print("popped:",custom_radicals.pop(radicals.index('4-Hydroxy-14N-TEMPO_old')))

#custom_radicals=['4-Oxo-14N-TEMPO','4-Amino-15N-TEMPO','14N-TEMPO']
#radicals=['Oxo71-Trityl']
#%%
#radicals=custom_radicals
print('radicals:',radicals)
print('concs:', concs )
print('skipped: ', skip_radicals)
#radicals=radicals



#print('popped out: ' + radicals.pop(-1))
    # this line can be used to delete radicals from the list by index



#%% tile plot

#!! caution !! T1_0_ mean was deactivated in the script!!
#fixed

prc_params = ['r1','r2','r1bar','r2bar',' P1/2','cc','smaxzeta','lf']
# 1/T1,2 plots,  relaxivities as bar plots, P_1,2(c), coupling factors multiplied with s_max, leakage factor, 
#abb=ldp.gen_abbreviations(radicals)  
# the names in radicals are too long for plot names. This method generates short abbreviations from the radical names. 
#

#plots all parameters as they are into 3x2 plot
#axes_raw=tpp.tile_plot_raw(radicals,parameters,ldp.spider_colors,old=True,bl_mode='on')
#axes_raw[3].set_ylim(-250,0)
    # returns the axes so you can modify from the console

#axes[3].set_ylim(-300,0)

#plots a bunch of processed parameters given by prc_params
axes_prc=tpp.tile_plot_prc(radicals,ldp.spider_colors,prc_params=prc_params,abb=None,old=True,bl_mode=bl_glob)

axes_prc[1][0].set_xlim(0,8)
axes_prc[1][1].set_xlim(0,8)
axes_prc[1][2].set_xlim(0,8)
axes_prc[1][2].set_ylim(-200,0)





#import tile_plot_prc_clean as tppc
#tppc.tile_plot_prc(radicals,spider_colors,prc_params=prc_params,short_labels= ldp.short_labels)

#%%

#%% spider plots

# nice to produce publication-ready plots.

#needs to be updated
# check label positions 
# for some reason norm_to does not change the plot


import spider_plot as spp
#short_labels=['A-14','A14o','O-15N-o','O-15N-o']
short_labels=ldp.gen_short_labels(radicals,old=True)
long_names=[radical[:-4] for radical in radicals]

#short_labels=['NH2-14','NH2-15N','Oxo-14N','Oxo-15N', 'TEMPO','Hydroxy']
spp.spider_plots(radicals,short_labels,sel_params=[' E_max', ' P1/2',' b1', ' T1'],norm_to=0,target_conc=1.0)
#%% heatmap
import heatmap_2 as hm


#short_labels=ldp.gen_short_labels(radicals,old=True)

long_names=[radical[:-4] for radical in radicals]
dF_abs,dF_norm=hm.generate_dF(radicals,
                              long_names,
                              sel_params=[' E_max', ' P1/2',' b1', ' T1',' T2'],
                              norm_to= 0,
                              target_conc=1.0,
                              exclude_rad=['4-Amino-14N-TEMPO_old','4-Hydroxy-14N-TEMPO_old'],
                              bl_mode=bl_glob,
                              )
hm.plot_mosaic_heatmap(dF_abs,dF_norm,
                       absolute=True,
                       target_conc=1.0,
                       cmap="coolwarm",
                       figsize=None,#
                       show_values=True,
                       fmt_norm=".3g",
                       fmt_abs=".3g",
                       vmin=0.7,
                       vmax=1.3,
                       par_names=[r'$\mathrm{E_{max}}$',r'$\mathrm{P_{1/2}}$','b1',r'$\mathrm{r_1}$',r'$\mathrm{r_2}$']
                       )
# print(dF_abs)
# print(dF_norm)

#%%horizontal heatmap
import heatmap_horizontal as hhm

# E_max: problem with baseline selecting keywords not checked here

short_labels=ldp.gen_short_labels(radicals,old=True)
dF_abs,dF_norm=hhm.generate_dF(radicals,short_labels,sel_params=[' E_max', ' P1/2',' b1', ' T1'], norm_to= -1)
hhm.plot_mosaic_heatmap(dF_abs,dF_norm,absolute=True, cmap="coolwarm", figsize=(8, 5),show_values=True, fmt=".3g",vmin=0.8, vmax=1.2)

#TODO flip string formating: not done already by Chatgpt 

#%%cc_plot
import cc_plot as ccp

ccp.cc_plot(radicals)

#%% fit coupling_factors

import fit_cf as fcf

radical_selection=['4-Oxo-14N-TEMPO_old','4-Amino-15N-TEMPO_old','14N-TEMPO_old' ]



passed_colors=ldp.spider_colors

#T_10 Oxo= 2617
#   amino 15: 2174
#TEMPO : 2290, zeta= 0.33

T10_values={'4-Oxo-14N-TEMPO_old': 2787.4,#2725,
            '4-Amino-15N-TEMPO_old': 2764.5,#2174,
            '14N-TEMPO_old':2683.6,
            '4-Amino-14N-TEMPO_old':2683.6,# same as TEMPO as Bp is close
            '4-Hydroxy-14N-TEMPO_old':2683.6,# same as TEMPO as Bp is close
            '4-Oxo-15N-TEMPO_old':2764.5,
            'Oxo71-Trityl':2787.4,
            } # same as Amino-15N-TEMPO #2305}

#alternative location, both working
#T10_values= ldp.T10_values 

c_offset_list=[0,0,0]

#for bl_mode in ['constant','on','off']:
exclude=True

print(bl_mode,exclude, sep='\t')

Fig,axe=subplots(figsize=(9,5),dpi=300)
Fig2,axe2=subplots(figsize=(9,5),dpi=300)
Fig2.suptitle('saturation factors')

Fig3,axes3= subplots(1,3,figsize=(12,4), dpi=300,sharey=True)
axes3=axes3.reshape(-1)


for k,radical in enumerate(radical_selection): 

    fcf.fit_cf(radical,
               k=None,
               ax=axe,
               ax2=axe2,
               ax3=axes3[k],
               Power=2,
               bl_mode=bl_mode,
               bl_constant=23,
               radicals=radicals,
               passed_color=passed_colors[k],
               exclude =exclude,
               guess=False,
               N_relax =False,
               x_offset=(k)*0.1,
               c_offset=c_offset_list[k],
               skip_radicals=skip_radicals,
               show_cf=True,
               T10_mean=T10_values[radical], #T10_values[radical]
               T1_field = 't_hyp',
               fix_zeta=None,
               label=radical[:-4]#radical+r' |$T_{1,0} = $'+str(T10_values[radical])+' ms'
               )
    
#%% find T_10



import fit_cf as fcf

Fig,axe=subplots(figsize=(9,5),dpi=300)
#axes=axe.reshape(-1)

passed_colors=ldp.spider_colors

#T_10 Oxo= 2617
#   amino 15: 2174
#TEMPO : 2290, zeta= 0.33

T10_values={'4-Oxo-14N-TEMPO_old': 2725,
            '4-Amino-15N-TEMPO_old': 2174,
            '14N-TEMPO_old':2305}

for i,T1_0 in enumerate(numpy.linspace(2100,2400,5)):
    for k,radical in enumerate(['4-Amino-15N-TEMPO_old']): 
        
    
        op= fcf.fit_cf(radical,
                   k=None,
                   ax=axe,
                   bl_mode='old',
                   radicals=radicals,
                   passed_color=passed_colors[i],
                   guess=True,
                   N_relax =False,
                   x_offset=(i)*0.1,
                   skip_radicals=skip_radicals,
                   show_cf=True,
                   T10_mean=T1_0, 
                   fix_zeta=None,
                   label=radical+r' |$T_{1,0} = $'+str(T1_0)+' ms', )#radical+r' |$T_{1,0} = $'+str(T10_values[radical])+' ms'
 #%%
#baseline keyword problem not adressed

import fit_E_max as fem   

fem.fit_Emax('4-Amino-15N-TEMPO_old',isotope=15,N_relax=False)
#%%

import Kais_data as Kd

Kd.plot_pool_data(radicals,bl_mode='on')
#%% fixed_power_plot

import fixed_P_plot as fpp

#currently set to 3 axes
# watch out, the recent changes in the dataset messed up the plots and datapoint are missing. 
#recheck.
powers=[2,10,30]

# create fp_plots for different bl_modes and generations

#fpp.fixed_p_plot(old_radicals,powers,bl_mode='on')
#fpp.fixed_p_plot(new_radicals,powers,bl_mode='on')

axes_fp=fpp.fixed_p_plot(['4-Oxo-14N-TEMPO_old','4-Amino-15N-TEMPO_old','14N-TEMPO_old'],powers,bl_mode='old',lf_out=False)

#axes_fp[0].set_ylim(-60,0) #just an experience value 

#%% fpp interpolated 
import fixed_P_plot as fpp


powers=[2,10,30]

fpp.fixed_P_int(['4-Oxo-14N-TEMPO_old','4-Amino-15N-TEMPO_old','14N-TEMPO_old'],powers,old=False,bl_mode='on')#['4-Oxo-14N-TEMPO_old']
#%%power sweeps

# one plot per radical contaiing each power sweep for all concentrations
# reconstructed from the fit! no raw data included

for radical in radicals: 

    fpp.power_sweep_fit(radical,20)

#%% figure for Kai,   compares differences in datasets with baseline correction etc.
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
sigp.signal_plot(radicals, bl_mode='on')

#%% print ex_dF for all radicals

Fig,axe= subplots(figsize=(16,9))

axe.plot()

for radical in radicals: #['4-Oxo-14N-TEMPO_old','4-Amino-15N-TEMPO_old','14N-TEMPO_old' ]: 
    
    fnames,concs= ex.load_files(radical)
    dF= ex.extract_cwise(' E_max',concs,fnames,out=False,bl_corr='on')
    concs=
    #print(radical, dF['values'].loc[1.0])
    
    axe.plot()
    

    # dF2=ex.extract_cwise(' T1',concs,fnames,out=False,bl_corr='on')
    # #print(dF['values'],dF2['values'])
    
    # delta= dF['values']/dF2['values']
    
    # data={'t_hyp': dF['values'], 
    #       'T1': dF2['values'],
    #       'delta': delta
    #       }
    
    # dF_show=pandas.DataFrame(data=data)
    # print(dF_show)
    
    
#    print('x1= '+str(dF['values'].loc[2.0]))
    
#%% 3D plot using plotly

#TODO: get raw data from MPI as csv file and integrate

import ECP_plots as ecp

import plotly.io as pio
pio.renderers.default='browser'

Fig_ratio,axe_ratio=subplots(figsize=(16,9))

for radical in radicals:
    print(radical)
    ecp.ECP_plot(radical,ax=axe_ratio)
    
