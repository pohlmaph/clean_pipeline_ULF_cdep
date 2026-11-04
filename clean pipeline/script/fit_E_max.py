# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 10:02:34 2026

@author: marsg
"""
from matplotlib.pyplot import subplots
import numpy as np

import bin_extraction as ex
import processing_functions as prc
import coupling_factors as cf
import pit2 as p2
import processing_functions as prc

from fit_cf import handler
from coupling_factors import leakage_factor

from processing_functions import get_r

from scipy.optimize import curve_fit



def fit_Emax(radical,isotope=15,N_relax=False,fix_zeta=None,bl_mode='old'): 
    
    
    



    fnames,conc_ul=ex.load_files(radical)   
    #Note: conc_ul here is in the order of the filenames- i.e. an unordered list
    #it has to be that way- otherwise filenames and concentrations are not aligned anymore
    # ordering happens in extract_cwise, when the values extracted from the filenames and concentrations are linked in a dataFrame
    #__________________________________________________________________
    ## condtions relevant only if bl_mode = 'old':
      
    if radical.find('old')!=-1 and bl_mode!= 'off':
        blc= True
       # print( f"baseline_correction enabled for {radical}")
    else: blc =False
    
    
    if bl_mode=='on': blc=True
    else: pass
    #_______________________________________________________________
    
    ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=False)
    concs=list(ex_dF.index)
    #_____get continuous T1s____________________________________________
    T1s=ex_dF['values']
    #T1_0= prc.get_r(radical,concs,ex_dF['values'])[1]
    
    r,offset,perc=get_r(radical,concs,T1s,plot=False,exclude=None)
    
    def T1(c):
        T1_inv= r*c+offset
        
        T1=1/T1_inv
        return T1
    
    ex_dF2=ex.extract_cwise(' E_max',conc_ul,fnames,out=False,bl_corr=blc)
    y_raw=list(ex_dF2['values'])
    x_raw=concs
    
    x_raw=x_raw[1:]
    y_raw=y_raw[1:]
    
    #select smax_zeta predicting function 
    smaxzeta_func=handler(isotope=isotope,N_relax=N_relax,fix_zeta=fix_zeta)
    
    def E_max_func(c,b,T10,zeta,d):
        
        #d=-0.5
        E_max= smaxzeta_func(c-d,b,zeta)*leakage_factor(T1(c-d),T10)*638.891
        
        return E_max
    
    lower_bounds=[0,0,-0.4,0]
    upper_bounds=[10,10000,-0.2,1]
    
    if N_relax==True:
        
        lower_bounds=[0,0,-0.4]
        upper_bounds=[10,4000,-0.2]
    
    params,pcov= curve_fit(E_max_func,x_raw,y_raw,p0=[0.5,2174,-0.35,0.5], bounds=(lower_bounds,upper_bounds)) #2174 [6.62424179 0.33569342]
    
    errors= np.sqrt(np.diag(pcov))
    perc=errors/params
    
    X=np.linspace(0,10,50)
    Y= E_max_func(X,*params)
    
    Fig,axe=subplots(figsize=(16,9))
    
    axe.scatter(x_raw,y_raw)
    axe.plot(X,Y)
    
    print(params)
    print(errors)
        
