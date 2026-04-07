# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 07:13:21 2026

@author: marsg
"""
from scipy.stats import linregress
import numpy as np
import bin_extraction as ex

def lin_fit(xdata,ydata):

    
    
   op= linregress(xdata,ydata)
   
   # array order: m,x in y= mx+c
   fit_params=[op.slope,op.intercept]
   rsquare=op.rvalue**2
   errors= [op.stderr,op.intercept_stderr]
   
   perc=[]
   for i in range(len(errors)): 
       perc.append(errors[i]/fit_params[i]*100)
   
   def lin_func(x,m,c):
       y=m*x+c
       return y
   
   x_opt= np.linspace(xdata[0],xdata[-1])
   y_opt= lin_func(x_opt,*fit_params)
   
   return x_opt,y_opt,fit_params,errors,perc,rsquare


def get_r(radical,concs,values):
    
    T_inv= [1/value for value in values]
    
    x_opt,y_opt,fit_params,errors,perc,rsquare = lin_fit(concs,T_inv)
    
    
    get_r.plotdata=[x_opt,y_opt]
    get_r.fit_report=[rsquare,fit_params,errors,perc]
    
    r = fit_params[0]
    Tx_0 = 1/fit_params[1]
    
    return r,Tx_0,perc

def get_cc(radical,conc,fnames):
    
    ex_dF= ex.extract_cwise(' x1',conc,fnames,out=False)
    concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.otherwise c is given by the order of filenames
    
    if radical.find('15N')!=-1: ex_dF2=ex.extract_cwise(' x2',conc,fnames,out=False)
    elif radical.find('14N')!=-1: ex_dF2=ex.extract_cwise(' x3',conc,fnames,out=False)
    else: print(' could not get isotope from radical name: please check radicals[]') 
    
    ccs= [ex_dF2['values'].iloc[x]-ex_dF['values'].iloc[x] for x in range(len(ex_dF2['values']))]
    # friendly reminder: ex_dF is a series object, not a list and has to be accessed respectively
    # output is a list
    
    half= [cc/2 for cc in ccs]
    #half is a list, not a series
    
    center=[]
    for i in range(len(ccs)):
        center.append(ex_dF['values'].iloc[i]+half[i])
    
    get_cc.center= center
    
    return ccs,concs


    
    
    