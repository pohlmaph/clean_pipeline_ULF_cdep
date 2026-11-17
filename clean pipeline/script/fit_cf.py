# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 18:17:02 2026

@author: marsg
"""
from matplotlib.pyplot import subplots
import bin_extraction as ex
import processing_functions as prc
import coupling_factors as cf
import numpy as np
import fixed_P_plot as fpp

import load_default_params as ldp

linspace=np.linspace

from scipy.optimize import curve_fit

import pit2 as p2

def handler(isotope=15,N_relax=False,fix_zeta=None,c_offset=0):
    
    if isotope==15 and N_relax==True:
        def func(c,a,b,zeta):
            if fix_zeta:
                zeta= fix_zeta
            d=c_offset
            smaxzeta=(1-(1/(2+a+(b*(c-d)))))*zeta
            return smaxzeta
        handler.func=func
        
    elif isotope== 14 and N_relax==True:
         
         def func(c,a,b,zeta):
             if fix_zeta:
                 zeta= fix_zeta
             d=c_offset
             smaxzeta=(1-(2/(3+a+(b*(c-d)))))*zeta
             return smaxzeta
         handler.func=func
    
    elif isotope== 15 and N_relax==False:
        
         def func(c,b,zeta):
             if fix_zeta:
                 zeta= fix_zeta
             d=c_offset
             smaxzeta=(1-(1/(2+(b*(c-d)))))*zeta
             return smaxzeta
         handler.func=func
         
    elif isotope== 14 and N_relax==False:
         
         def func(c,b,zeta):    
             if fix_zeta:
                 zeta= fix_zeta
             d=c_offset
             smaxzeta=(1-(2/(3+(3*b*(c-d)))))*zeta
             return smaxzeta
         handler.func=func
    
    return func
    
        

def fit_cf(radical,
           k=None,
           ax=None,
           ax2=None,
           ax3=None,
           bl_mode='old',
           radicals=None,
           passed_color='blue',
           N_relax=True,
           x_offset=0,
           c_offset=0,
           guess=True,
           skip_radicals=None,
           show_cf=True,
           T10_mean=None,
           T1_field='B_0',
           label=None,
           fix_zeta=None,
           Power=None,
           
           **kwargs):
    
    if radical in skip_radicals: 
        print(radical+ ' was skipped' )
        return
    print(radical)
    #print('Nitrogen relaxation N_relax= ',N_relax, sep='\t')
    #print('plot guess data (guess) ', guess, sep='\t') 
    
    if ax==None:
        Fig,ax=subplots(figsize=(7,3),dpi=300)
    #____________________________________________________________________________
    fnames,conc_ul=ex.load_files(radical)   
    #Note: conc_ul here is in the order of the filenames- i.e. an unordered list
    #it has to be that way- otherwise filenames and concentrations are not aligned anymore
    # ordering happens in extract_cwise, when the values extracted from the filenames and concentrations are linked in a dataFrame
    
    ## condtions relevant only if bl_mode = 'old':
      
    if radical.find('old')!=-1 and bl_mode!= 'off':
        blc= True
       # print( f"baseline_correction enabled for {radical}")
    else: blc =False
    
    #if radical.find('old')!=-1 and old==False: continue # omits old data
    if bl_mode=='on': blc=True
    else: pass
    #________________________________________________________________________________
    if T1_field=='B_0':
        ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=False)
    if T1_field=='t_hyp':
        ex_dF= ex.extract_cwise('t_hyp',conc_ul,fnames,out=False)
    concs=list(ex_dF.index)
    print('intial concs', concs)
    T1s=ex_dF['values']
    #T1_0= prc.get_r(radical,concs,ex_dF['values'])[1]
    
    ex_dF2=ex.extract_cwise(' E_max',conc_ul,fnames,out=False,bl_corr=blc)
    E_max=list(ex_dF2['values'])
    
    if T10_mean==None:
        T10_mean= cf.get_mean_T10(radicals)[1]
    #print(T10_mean)
    smz=cf.get_smaxzeta(T1s,T10_mean,E_max,T10_mean=False,radicals=radicals)
    lf=cf.get_smaxzeta.lf
    
    if radical== '4-Hydroxy-14N-TEMPO_old': 
        smz=smz[:4]
        concs=concs[:4]
        lf=lf[:4]
        
    #cut values for  x mM  -> lazy hard coded implementation    
    if radical== '14N-TEMPO_old': #or '4-Oxo-14N-TEMPO_old'
        smz=smz[:]
        concs=concs[:] 
        lf=lf[:]
        
        smz.pop(0)
        concs.pop(0)
        lf.pop(0)
    if radical== '4-Amino-15N-TEMPO_old': #or '4-Oxo-14N-TEMPO_old'
        smz=smz[1:]
        concs=concs[1:] 
        lf=lf[1:]
        
        # append fictional data points to simulate impact
        # smz.append(0.3)
        # concs.append(6.0)
        # lf.append(lf[-1])
    else: 
         
          smz=smz[:]
          concs=concs[:]    
          lf=lf[:]
          
    print('final concs', concs) 
    param=' '
    
    #raw data
    #p2.pit(ax,param,concs,smz,label=radical,color=passed_color)
    #p2.pit(ax,param,concs,smz,label=radical,color=passed_color,)
    ax.scatter(concs,smz,marker='o',color=passed_color,s=20,label=label)
    
    #print(radical)
    #function selection
    
    if radical.find('15N')!= -1:
        predict_smaxzeta=handler(isotope=15,N_relax=N_relax,fix_zeta=fix_zeta,c_offset=c_offset)
    elif radical.find('14N')!=-1:
        predict_smaxzeta=handler(isotope=14,N_relax=N_relax,fix_zeta=fix_zeta,c_offset=c_offset)
    else: print('isotope could not be determined  from radical name') 
    
    
    
    #plot guess data
    if N_relax==True:
        guess=[ 1, 3, 0.31]
        if fix_zeta:
            guess[-1]==fix_zeta
        lower_bounds = [0,0,0]
        upper_bounds = [np.inf,np.inf, np.inf]
        
    else:  
        guess=[10, 0.31]
        lower_bounds = [0,0]
        upper_bounds = [np.inf,np.inf]
    
    
    y_guess= [predict_smaxzeta(c,*guess) for c in concs]  
    if guess==True: 
        p2.pit(ax,param,concs,y_guess,label=radical+'_guess',color=passed_color,alpha=0.5)
    
    #fitting step
    
    params,pcov=curve_fit(predict_smaxzeta, concs, smz,p0=guess,bounds=(lower_bounds,upper_bounds))
        
    print('params',params,sep='\t')
    errors= np.sqrt(np.diag(pcov))
    #(errors)
    perc= errors/params*100
    print('perc',perc,sep='\t')
    
    
    
    plot_concs=linspace(0,10,51)
    # if 2.0 in plot_concs:
    #     print(True)
    Y=[predict_smaxzeta(c,*params) for c in plot_concs]
    
    #print('zero_value:',   Y[0])
    
    p2.pit(ax,param,plot_concs,Y,color=passed_color,alpha=0.5,**kwargs)
    p2.pit(ax,param,10-x_offset,params[-1],yerror= errors[-1],linestyle=None,color=passed_color)#plot errorbars
    if show_cf==True: ax.scatter(10-x_offset,params[-1],s=60,color=passed_color,marker="X")# mark cf center value
    ax.set_ylim(0.1,0.4)
    ax.set_xlim(0,10.5)
    ax.set_ylabel(r'$s_{max}\cdot\zeta$')
    ax.legend(loc='lower right')
    
    ax.text(9.8,0.27,'estimated\ncoupling\nfactors',fontsize=7,ha='center')
    #print('c_offset: ', c_offset)
    
    
    #__________________________
    #show saturation factor only
    
    
    
    
    Y2=[predict_smaxzeta(c,*params)/params[-1] for c in plot_concs]
    y2=smz/params[-1]
    
    if ax2==None:
        Fig2,ax2 =subplots(figsize=(16,9))
    
    ax2.plot(plot_concs,Y2,color=passed_color)
    ax2.scatter(concs,y2,marker='o',color=passed_color,s=20,label=label)
    ax2.legend(fontsize=8)
    
    
    
    # ax.text(2,0.15,bl_mode+'\n'+'N_relax='+str(N_relax)+'\nT1_field='+str(T1_field),fontsize=6)
    # ax2.text(2,0.4,bl_mode+'\n'+'N_relax='+str(N_relax)+'\nT1_field='+str(T1_field),fontsize=6)
    
    
    #______
    # plot all three contributions in one plot: lf smax and zeta
    
    #at low powers:
        
    
    fit_params,exp_values=fpp.P_12_int(radical,out=False,bl_mode='old',plot=False)
    
    def lin_func(x,a,b): 
        y=a*x+b
        return y
    if Power: P=Power
    else: P=2 
    def sP(P,c):
        
        P_12= lin_func(c,*fit_params)
        sP= P/(P+P_12)
        return sP
    
    sP_values=[sP(P,c) for c in plot_concs]
    
    if ax3==None:
        Fig3,ax3= subplots(figsize=(16,9),dpi=300)
    
    ax3.plot(plot_concs,Y2,color=ldp.spider_colors[0],label=r'$\mathrm{s_{max}}$')# s_max fitted
    ax3.plot(concs,lf,color=ldp.spider_colors[1],label='leakage factor')# leakage factors exp
    ax3.axhline(params[-1],label=r'$\zeta$',color=ldp.spider_colors[2]) #coupling factor
    if Power: ax3.plot(plot_concs,sP_values,color=ldp.spider_colors[3],label='s(P)')
    
    ax3.set_title(radical[:-4])
    ax3.set_xlabel('concentration in mM')
    ax3.legend()
    ax3.yaxis.set_inverted(True)
    Y2=list(Y2)
    lf=list(lf)
    plot_concs=list(plot_concs)
    concs=list(concs)
    
    #ax3.vlines([1,2],[Y2[plot_concs.index(1.0)],Y2[plot_concs.index(2.0)]],[lf[concs.index(1.0)],lf[concs.index(2.0)]])
    return ax, perc
    