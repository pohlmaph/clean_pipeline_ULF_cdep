# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 08:32:24 2026

@author: marsg
"""

spider_colors=['#eba750','#a740bc','#408dbc','#40bcaa','blue','red','green','purple' ]

prc_params = ['r1','r2','r1bar','r2bar',' P1/2','cc','smaxzeta']

short_labels= ['NH2-14','NH2-15N','Oxo-14N','Oxo-15N', 'TEMPO','Hydroxy']
#abbreviations= ['A','A-15','O','O-15N','H','OH'] 

def gen_short_labels(radicals,old=False):
    
    name_dict= {'Amino-14N-TEMPO_3_26': 'A-14',
                'Amino-14N-TEMPO_old': 'A-14o',
                'Oxo-15N-TEMPO_3_26': 'O-15',
                'Oxo-15N-TEMPO_old': 'O-15o',
                'Hydroxy-14N-TEMPO': 'OH-14N',
                'Oxo-14N-TEMPO': 'O-14',
                'Oxo71':'Oxo71',
                'TEMPO-14N':'H-14',
                'TEMPO-15N':'H-14',
                'Carboxy-14N-Proxyl':'cp-14'}
                
                
    
    short_labels=[]
    for radical in radicals:
        for name in name_dict:
            if name in radical:
                if old ==False and name.find('old')!=-1: break
                short_labels.append(name_dict[name])
                    
                break
        else:
            print(
                "Could not generate abbreviation from radical names - "
                "please check your naming to match the built-in dictionary "
                "or define custom short_labels"
            )
    return short_labels


def gen_abbreviations(radicals,old=False):
    
    name_dict= {'Amino-14N-TEMPO_3_26': 'A-14',
                'Amino-14N-TEMPO_old': 'A-14o',
                'Oxo-15N-TEMPO_3_26': 'O-15',
                'Oxo-15N-TEMPO_old': 'O-15o',
                'Hydroxy-14N-TEMPO': 'OH-14N',
                'Oxo-14N-TEMPO': 'O-14',
                'Oxo71':'Oxo71',
                'TEMPO-14N':'H-14',
                'TEMPO-15N':'H-14',
                'Carboxy-14N-Proxyl':'cp-14'}

    abbreviations = []
    
    for radical in radicals:
        for name in name_dict:
            if name in radical:
                if old ==False and name.find('old')!=-1: break
                abbreviations.append(name_dict[name])
                break
        else:
            print(
                "Could not generate abbreviation from radical names - "
                "please check your naming to match the built-in dictionary "
                "or define custom short_labels"
            )
            
    return abbreviations