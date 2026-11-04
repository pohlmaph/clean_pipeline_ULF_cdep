# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 16:04:42 2026

@author: marsg
"""
#created with ChatGPT

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import bin_extraction as ex
import processing_functions as prc

#generate the dataFrame for plotting

def generate_dF(radicals,short_labels,sel_params=[' E_max', ' P1/2',' b1', ' T1',' T2'],  norm_to= -1):
    
    par_names=[r'$\mathrm{E_{max}}$', r'$\mathrm{P_{1/2}}$','linewidth', 'longitudinal relaxivity']

    dF_abs=pd.DataFrame(index=short_labels)
    dF_norm=pd.DataFrame(index=short_labels)
    i=0
    for param in sel_params:
        k=0
        values_abs=[]
        
        for radical in radicals:
            
            
            fnames,conc=ex.load_files(radical)
            
            
            ex_dF= ex.extract_cwise(param,conc,fnames,out=False)
            concs=list(ex_dF.index)# This overwrites concs with the sorted list matching the dataframe order.
            
            
            
            if param==' T1': 
                
                
                if radical=='4-Hydroxy-14N-TEMPO_old': 
                    r1,T1_0,perc= prc.get_r(radical,concs,ex_dF['values'],plot=True,exclude=-1)
                else:    
                    r1,T1_0,perc= prc.get_r(radical,concs,ex_dF['values'],plot=True,exclude= None)
                #print(radical, prc.get_r.fit_report)
                
                values_abs.append(r1)
                
            elif param==' T2': 
                
                
                if radical=='4-Hydroxy-14N-TEMPO_old': 
                    r2,T2_0,perc= prc.get_r(radical,concs,ex_dF['values'],plot=True,exclude=-1)
                else:    
                    r2,T2_0,perc= prc.get_r(radical,concs,ex_dF['values'],plot=True,exclude= None)
                #print(radical, prc.get_r.fit_report)
                
                values_abs.append(r2)
                
            else: values_abs.append(ex_dF['values'].loc[2.0])
            
            
            k=k+1
        
        
        
        values_norm=[value/values_abs[norm_to] for value in values_abs]
        dF_norm[param]=values_norm
        dF_abs[param]=values_abs
        i=i+1
    return dF_abs,dF_norm
        

def plot_mosaic_heatmap(df_abs,df_norm,absolute=False, cmap="coolwarm", figsize=(8, 5),
                        show_values=True, fmt=".3g",par_names=[r'$\mathrm{E_{max}}$',r'$\mathrm{P_{1/2}}$','b1',r'$\mathrm{r_1}$',r'$\mathrm{r_2}$'],
                        vmin=0.8, vmax=1.2):
    """
    Plot a 6x4 mosaic-style heatmap.

    Parameters
    ----------
    df : pandas.DataFrame
        Shape (4, 6)
        Rows = Parameters
        Columns = Radicals
    cmap : str
        Matplotlib colormap.
    figsize : tuple
        Figure size.
    show_values : bool
        Whether to display values inside each tile.
    fmt : str
        Number formatting.
    vmin, vmax : float
        Color scale limits.
    """
    print(df_abs)
    print(df_norm)
    # if df_norm.shape != (6, 5):
    #     raise ValueError("DataFrame must have exactly 6 rows and 5 columns.")

    n_rows, n_cols = df_norm.shape
    if figsize is None:
        # Dynamically scale figure size to match matrix aspect ratio
        figsize = (max(6, n_cols * 1.5), max(4, n_rows * 0.8))

    fig, ax = plt.subplots(figsize=figsize)
    if absolute==False:
        fig.suptitle(' parameter values normalized to TEMPO',x=0.65, ha='center')
    if absolute==True:
        fig.suptitle('absolute parameter values',x=0.65, ha='center')
    
    # Draw heatmap
    im = ax.imshow(df_norm.values,
                   cmap=cmap,
                   aspect="equal",
                   vmin=vmin,
                   vmax=vmax,
                   )

    # Axis labels
    ax.set_xticks(np.arange(df_norm.shape[1]))
    ax.set_xticklabels(par_names, fontsize=11)

    ax.set_yticks(np.arange(df_norm.shape[0]))
    ax.set_yticklabels(df_norm.index, fontsize=11)

    ax.set_ylabel("Radicals", fontsize=13)
    ax.set_xlabel("Parameters", fontsize=13)

    # White grid to create mosaic effect
    # Dynamic Grid Boundaries (fixes cropped end-columns)
    ax.set_xticks(np.arange(-0.5, n_cols + 1, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n_rows + 1, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.set_xlim(-0.5, num_cols - 0.5)
    ax.set_ylim(num_rows - 0.5, -0.5)

    # Annotate cells
    
    
    if show_values and absolute==False:
        for i in range(df_norm.shape[0]): # [i,j]-> [rows,columns]
            for j in range(df_norm.shape[1]):
                ax.text(j, i,
                        format(df_norm.iloc[i, j], fmt),
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=10,
                        fontweight="bold")
                
    if show_values and absolute==True:
        for i in range(df_abs.shape[0]):
            fmt='.3g'
            for j in range(df_abs.shape[1]):
                
                ax.text(j, i+0.2,
                        format(df_norm.iloc[i, j], fmt),
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=6,
                        #fontweight="bold"
                        )
                
                
                if j== 3: fmt='.3g'
                else: fmt= '.3g'
                ax.text(j, i-0.1,
                        format(df_abs.iloc[i, j], fmt),
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=7,
                        fontweight="bold")
                
                


    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("colour value relative to TEMPO")

    plt.tight_layout()
    plt.show()
    
# # Example data
# radicals = ["R1", "R2", "R3", "R4", "R5", "R6"]
# parameters = ["Parameter 1", "Parameter 2", "Parameter 3", "Parameter 4"]

# np.random.seed(1)

# df = pd.DataFrame(
#     np.random.rand(4, 6),
#     index=parameters,
#     columns=radicals
# )

# plot_mosaic_heatmap(df, cmap="RdYlGn")