# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 07:12:00 2026

@author: marsg
"""

    
import matplotlib
from pylab import *
import pandas as pd 
import numpy as np
from glob import glob
from scipy.optimize import curve_fit
from pathlib import Path
import os
    
def get_paths():
    
        
    cwdir= Path.cwd()
    
    parent= cwdir.parent
    raw_dir= str(parent/'RAW')
    process_dir=str(parent/'process files')
    
    return raw_dir,process_dir,parent

raw_dir,process_dir,parent=get_paths()
    
def get_radicals(path=False):
    
    #raw_dir=get_paths()[0]
    folders= glob(raw_dir+'\\*')
    radicals=[]
    for folder in folders:
        if '.txt' in folder: continue
        rname=folder[folder.rfind('\\')+1:]
        radicals.append(rname)
    if path==False:    
        return radicals
    elif path==True: 
        return folders
    
def load_single_file(radical=get_radicals()[0]):
    radical_path=get_radicals(path=True)
    fnames,concs=load_files(radical)
    parameters= get_pnames(fnames[0]) 
    
    print("parameters:", parameters)
    return radical_path, fnames, concs,parameters,

def load_files(radical, folder='default'):
    
    # takes your custom data folder as optional argument,
    
    
    if folder=='default':
        filenames=glob(str(raw_dir)+'\\'+radical+'\\*charac.csv')
        concs=[]
        files=[]
        for file in filenames: 
            string= file[file.rfind('\\')+1:file.rfind('mM')]
            #print(file)
            #print(string)
            concs.append(float(string))
            files.append(file)
    else: filenames= glob(folder+'*charac.csv')
    
    return filenames,concs

def get_pnames(filename):
    # takes a single filename, e.g. filenames[0]
    
    dF=pd.read_csv(filename)
    
    pnames=list(dF.columns)
    
    return pnames


    
    
def extract_cwise(pname,concs,filenames,out=False,bl_corr=False,save=False):
    #combines values and errors, but only for one parameter at a time
    #args= locals()
    
    data_list = []
    
    
    #extract baseline -duplicate code with pname = baseline
    
    if bl_corr==True:
        
        bls=[]
        for file in filenames:
            dF = pd.read_csv(file,header=0)
            
            if ' baseline' in dF.columns:
                bls.append(dF[' baseline'].values[0])
                
            else: print('baseline value was not passed in csv. file')
                #data_list.append(np.full(len(dF), np.nan))
        
    
    for file in filenames:
        dF = pd.read_csv(file,header=0)
    
        if pname in dF.columns:
            data_list.append(dF[pname].values)
        else:
            # create NaN row with correct length
            data_list.append(np.full(len(dF), np.nan))
    
    # sanity check- this is a help for detecting mistakes in the concentrations passed from upstream 
    if len(data_list) != len(concs):
        raise ValueError(
            f"Mismatch: {len(data_list)} files but {len(concs)} concentrations" )
        print(' check if concentration detection or concs passed from upstream are correct')
   
    ex_dF=pd.DataFrame(data_list,index=concs).sort_index()  
    
    # only assign column names if matching
    if len(ex_dF.columns) == 5:
        ex_dF.columns = ['values', 'ubound', 'lbound', 'dev', 'perc']
    #___________!!!_____________  
    
    
    ### corrections 
    
    #tp90 correction
    
    if pname == ' E_max':
        ex_dF['values']=ex_dF['values']/0.9
        # It is debatable, if we apply the tp90 correction also for the standard deviation,etc. I chose not to, as I interpret the errors as instrument related and not of sample origin. 
        
        
        #baseline correction by average baseline
        if bl_corr==True:
            
            av=np.average(bls)
            ex_dF['values'] = [value * b / av for value, b in zip(ex_dF['values'], bls)]
    
        
    if save==True:    
        if pname==' P1/2': ex_dF.to_csv(process_dir+ f"\\ex_cwise_P_12.csv",sep='\t')
        elif pname !=' P_1/2':ex_dF.to_csv(process_dir+ f"\\ex_cwise_{pname}.csv",sep='\t')
    
    
    if out==True: print(ex_dF)
    
    return ex_dF
    
    
def get_value_dF(filenames,concs,row='values'): # depreciated, but in Line with old pipeline
    
    #takes: list of filenames and list of respective concentrations
    #takes values for all parameters but returns only values or  upper bound, etc. based on the row keyword
    
    data_list=[]
    for file in filenames:
        dF=pd.read_csv(file)
        if row=='values':
            data_list.append(dF.iloc[0])# takes only the first row with values
        if row=='ubound':
            data_list.append(dF.iloc[1])# takes only the second row with values
        if row=='lbound':
            data_list.append(dF.iloc[2])# takes only the third row with values    
        if row=='dev':
            data_list.append(dF.iloc[3])# takes only the fourth row with values
    
    value_dF=pd.DataFrame(data=data_list,index=concs).sort_index()
    value_dF.to_csv(process_dir+'\\value_dF.csv',sep='\t')
    
    return value_dF

