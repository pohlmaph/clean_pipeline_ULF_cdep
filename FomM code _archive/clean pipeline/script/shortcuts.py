# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 11:15:40 2026

@author: marsg
"""

radical_path, fnames, concs,parameters=ex.load_single_file(radical='4-Amino-14N-TEMPO_3_26')
ex.extract_cwise(' x1',concs,fnames,out=True)