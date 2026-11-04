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

linspace=np.linspace

from scipy.optimize import curve_fit

import pit2 as p2

def handler(isotope=15,N_relax=False,fix_zeta=None):
    
    if isotope==15 and N_relax==True:
        def func(c,a,b,zeta):
            if fix_zeta:
                zeta= fix_zeta
            smaxzeta=(1-(1/(2+a+(b*c))))*zeta
            return smaxzeta
        handler.func=func
        
    elif isotope== 14 and N_relax==True:
         
         def func(c,a,b,zeta):
             if fix_zeta:
                 zeta= fix_zeta
             smaxzeta=(1-(2/(3+a+(b*c))))*zeta
             return smaxzeta
         handler.func=func
    
    elif isotope== 15 and N_relax==False:
        
         def func(c,b,zeta):
             if fix_zeta:
                 zeta= fix_zeta
             smaxzeta=(1-(1/(2+(b*c))))*zeta
             return smaxzeta
         handler.func=func
         
    elif isotope== 14 and N_relax==False:
         
         def func(c,b,zeta):    
             if fix_zeta:
                 zeta= fix_zeta
             smaxzeta=(1-(2/(3+(3*b*c))))*zeta
             return smaxzeta
         handler.func=func
    
    return func
    
        

def fit_cf(radical,k=None,ax=None,bl_mode='old',radicals=None,passed_color='blue',N_relax=True,guess=True, x_offset=0,skip_radicals=None,show_cf=True,T10_mean=None,label=None,fix_zeta=None,**kwargs):
    
    if radical in skip_radicals: 
        print(radical+ ' was skipped' )
        return
    
    #print('Nitrogen relaxation N_relax= ',N_relax, sep='\t')
    #print('plot guess data (guess) ', guess, sep='\t') 
    
    if ax==None:
        Fig,ax=subplots(figsize=(7,3),dpi=300)
    
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
    
    ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=False)
    concs=list(ex_dF.index)
    
    T1s=ex_dF['values']
    #T1_0= prc.get_r(radical,concs,ex_dF['values'])[1]
    
    ex_dF2=ex.extract_cwise(' E_max',conc_ul,fnames,out=False,bl_corr=blc)
    E_max=list(ex_dF2['values'])
    
    if T10_mean==None:
        T10_mean= cf.get_mean_T10(radicals)[1]
    #print(T10_mean)
    smz=cf.get_smaxzeta(T1s,T10_mean,E_max,T10_mean=False,radicals=radicals)
    
    if radical== '4-Hydroxy-14N-TEMPO_old': 
        smz=smz[:4]
        concs=concs[:4]
        
    #cut values for  x mM  -> lazy hard coded implementation    
    if radical== '14N-TEMPO_old': #or '4-Oxo-14N-TEMPO_old'
        smz=smz[1:-1]
        concs=concs[1:-1] 
        
    else: 
         
          smz=smz[:-1]
          concs=concs[:-1]    
        
    param='smaxzeta_fit'
    
    #raw data
    #p2.pit(ax,param,concs,smz,label=radical,color=passed_color)
    #p2.pit(ax,param,concs,smz,label=radical,color=passed_color,)
    ax.scatter(concs,smz,marker='o',color=passed_color,s=20,label=label)
    
    #print(radical)
    #function selection
    
    if radical.find('15N')!= -1:
        predict_smaxzeta=handler(isotope=15,N_relax=N_relax,fix_zeta=fix_zeta)
    elif radical.find('14N')!=-1:
        predict_smaxzeta=handler(isotope=14,N_relax=N_relax,fix_zeta=fix_zeta)
    else: print('isotope could not be determined  from radical name') 
    
    
    
    #plot guess data
    if N_relax==True:
        guess=[ 0.01, 0.01, 0.31]
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
        
    print(T10_mean,params)
    errors= np.sqrt(np.diag(pcov))
    #(errors)
    perc= errors/params*100
    print('perc',perc)
    
    
    
    concs=linspace(0,10)
    Y=[predict_smaxzeta(c,*params) for c in concs]
    
    print('zero_value:',   Y[0])
    
    p2.pit(ax,param,concs,Y,color=passed_color,alpha=0.5,**kwargs)
    p2.pit(ax,param,10-x_offset,params[-1],yerror= errors[-1],linestyle=None,color=passed_color,)
    if show_cf==True: ax.scatter(10-x_offset,params[-1],s=60,color=passed_color,marker="X")
    ax.set_ylim(0.1,0.4)
    ax.set_xlim(0,10.5)
    ax.set_ylabel(r'$s_{max}\cdot\zeta$')
    ax.legend(loc='lower right')
    
    ax.text(9.8,0.27,'estimated\ncoupling\nfactors',fontsize=7,ha='center')
    
    return ax, perc
    