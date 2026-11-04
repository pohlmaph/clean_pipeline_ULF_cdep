# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 16:47:22 2026

@author: marsg
"""
import bin_extraction as ex
import processing_functions as prc

def get_T10s(radicals):
    
    op=[]
    print('T1_0')
    print('_____________________')
    
    for radical in radicals:
        #print(radical)
        fnames,conc_ul=ex.load_files(radical)
        
        ex_dF= ex.extract_cwise(' T1',conc_ul,fnames,out=False)
        concs=list(ex_dF.index)
        
        T1s=ex_dF['values']
        T1_0= prc.get_r(radical,concs,ex_dF['values'])[1]
        print(radical, T1_0, T1s[2.0],sep='\t')
        
        
        op.append(T1_0)

        