# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 08:32:24 2026

@author: marsg

"""
import matplotlib.pyplot as plt
#%% standard user input lists 
prc_params = ['r1','r2','r1bar','r2bar',' P1/2','cc','smaxzeta']
#%% colors 


#getting default maptlotlib colors as filling material
prop_cycle = plt.rcParams['axes.prop_cycle']
mpl_colors = prop_cycle.by_key()['color']

#defining some colors that are projector-proof and accessible for color-blind people -> publication ready
spider_colors=['#eba750','#a740bc','#408dbc','#40bcaa','grey','black']+mpl_colors


# A typical problem is that the number of radicals exceeds the number of colors, typically resulting in an index error during plotting
#print(len(radicals))
#print(len(spider_colors))





#%% labels

# standard labels are too long for bar_plots and spider_plots
#->  this method matches custom short_labels for all radicals
#gen_abbreviations originally contained shorter labels. Should be inactive.
# gen_short_labels and gen_abbreviations are currently identical, as there was no need anymore . 


short_labels= ['NH2-14','NH2-15N','Oxo-14N','Oxo-15N', 'TEMPO','Hydroxy']
#abbreviations= ['A','A-15','O','O-15N','H','OH'] 

# old =True keyword is deprecated as skipping radicals causes follow-up problems. if True, it has no effect. 

def gen_short_labels(radicals,old=True):
    
    name_dict= {'Amino-14N-TEMPO_3_26': 'A-14',
                'Amino-14N-TEMPO_old': 'A-14o',
                '4-Amino-15N-TEMPO_old':'A-15o',
                'Oxo-15N-TEMPO_3_26': 'O-15',
                'Oxo-15N-TEMPO_old': 'O-15o',
                '4-Hydroxy-14N-TEMPO_old':'OH-14o',
                '4-Oxo-14N-TEMPO_old':'O-14o',
                'Hydroxy-14N-TEMPO': 'OH-14N',
                'Oxo-14N-TEMPO': 'O-14',
                'Oxo71':'Oxo71',
                'TEMPO-14N':'H-14',
                'TEMPO-14N_old': 'H-14o',
                'TEMPO-15N':'H-14',
                'Carboxy-14N-Proxyl':'cp-14',
                '4-Amino-15N-TEMPO':'A-15',
                '4-Hydroxy-15N-TEMPO':'OH-15',
                
                
                }
                
                
    
    short_labels=[]
    for radical in radicals:
        for name in name_dict:
            if name in radical:
                if old ==False and name.find('old')!=-1: break
                short_labels.append(name_dict[name])
                    
                break
        else:
            print(
                f"Could not generate abbreviation from radical name {radical} - "
                "please check your naming to match the built-in dictionary "
                "or define custom short_labels"
            )
    return short_labels


def gen_abbreviations(radicals,old=True):
    
    name_dict= {'Amino-14N-TEMPO_3_26': 'A-14',
                'Amino-14N-TEMPO_old': 'A-14o',
                '4-Amino-15N-TEMPO_old':'A-15o',
                'Oxo-15N-TEMPO_3_26': 'O-15',
                'Oxo-15N-TEMPO_old': 'O-15o',
                '4-Hydroxy-14N-TEMPO_old':'OH-14o',
                '4-Oxo-14N-TEMPO_old':'O-14o',
                'Hydroxy-14N-TEMPO': 'OH-14N',
                'Oxo-14N-TEMPO': 'O-14',
                'Oxo71':'Oxo71',
                'TEMPO-14N':'H-14',
                'TEMPO-14N_old': 'H-14o',
                'TEMPO-15N':'H-14',
                'Carboxy-14N-Proxyl':'cp-14',
                '4-Amino-15N-TEMPO':'A-15',
                '4-Hydroxy-15N-TEMPO':'OH-15',
                
                
                }

    abbreviations = []
    
    for radical in radicals:
        for name in name_dict:
            if name in radical:
                if old ==False and name.find('old')!=-1: break
                abbreviations.append(name_dict[name])
                break
        else:
            print(
                f"Could not generate abbreviation from radical name {radical} - "
                "please check your naming to match the built-in dictionary "
                "or define custom short_labels"
            )
            
    return abbreviations