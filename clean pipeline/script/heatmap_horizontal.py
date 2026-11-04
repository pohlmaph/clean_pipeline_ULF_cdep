import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import bin_extraction as ex
import processing_functions as prc

#generate the dataFrame for plotting

def generate_dF(radicals,short_labels,sel_params=[' E_max', ' P1/2',' b1', ' T1'],  norm_to= -1):
    
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
            
            #!!!!update!!!!!                        <-------------------------------!-!--!--!----------------------------------------------
            #exception until r1 is correctly implemented  
            if param==' T1': values_abs.append(1/(ex_dF['values'].loc[2.0]))
                
            else: values_abs.append(ex_dF['values'].loc[2.0])
            
            
            k=k+1
        
        
        
        values_norm=[value/values_abs[norm_to] for value in values_abs]
        dF_norm[param]=values_norm
        dF_abs[param]=values_abs
        i=i+1
    return dF_abs,dF_norm


def plot_mosaic_heatmap(df_abs, df_norm, absolute=False, cmap="coolwarm",
                        figsize=(8, 5), show_values=True, fmt=".3g",
                        vmin=0.8, vmax=1.2):
    """
    Plot a mosaic-style heatmap with parameters on the y-axis
    and radicals on the x-axis.

    The input DataFrames are expected to have:
        rows    = radicals
        columns = parameters

    They are transposed for plotting, but the correspondence
    between each radical, parameter, and value is preserved.
    """

    # ---------------------------------------------------------
    # Check input dimensions
    # ---------------------------------------------------------
    if df_norm.shape != (6, 4):
        raise ValueError(
            "df_norm must have exactly 6 rows and 4 columns."
        )

    if df_abs.shape != (6, 4):
        raise ValueError(
            "df_abs must have exactly 6 rows and 4 columns."
        )

    # ---------------------------------------------------------
    # Transpose for plotting
    #
    # Input:
    #     rows    = radicals
    #     columns = parameters
    #
    # Plot:
    #     rows    = parameters
    #     columns = radicals
    # ---------------------------------------------------------
    df_norm_plot = df_norm.T
    df_abs_plot = df_abs.T

    # ---------------------------------------------------------
    # Create figure
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=figsize)

    if absolute is False:
        fig.suptitle(
            'Parameter values normalized to TEMPO',
            x=0.65,
            ha='center'
        )
    else:
        fig.suptitle(
            'Absolute parameter values',
            x=0.65,
            ha='center'
        )

    # ---------------------------------------------------------
    # Draw heatmap
    # ---------------------------------------------------------
    im = ax.imshow(
        df_norm_plot.values,
        cmap=cmap,
        aspect="equal",
        vmin=vmin,
        vmax=vmax
    )

    # ---------------------------------------------------------
    # Axis labels
    # ---------------------------------------------------------
    ax.set_xticks(np.arange(df_norm_plot.shape[1]))
    ax.set_xticklabels(
        df_norm_plot.columns,
        fontsize=11
    )

    ax.set_yticks(np.arange(df_norm_plot.shape[0]))
    ax.set_yticklabels(
        df_norm_plot.index,
        fontsize=11
    )

    ax.set_xlabel("Radicals", fontsize=13)
    ax.set_ylabel("Parameters", fontsize=13)

    # ---------------------------------------------------------
    # White grid / mosaic effect
    # ---------------------------------------------------------
    ax.set_xticks(
        np.arange(-0.5, df_norm_plot.shape[1], 1),
        minor=True
    )

    ax.set_yticks(
        np.arange(-0.5, df_norm_plot.shape[0], 1),
        minor=True
    )

    ax.grid(
        which="minor",
        color="white",
        linewidth=3
    )

    ax.tick_params(
        which="minor",
        bottom=False,
        left=False
    )

    # ---------------------------------------------------------
    # Annotate cells
    # ---------------------------------------------------------
    if show_values:

        for i in range(df_norm_plot.shape[0]):
            for j in range(df_norm_plot.shape[1]):

                # -------------------------------------------------
                # Normalized heatmap
                # -------------------------------------------------
                if absolute is False:

                    ax.text(
                        j,
                        i,
                        format(
                            df_norm_plot.iloc[i, j],
                            fmt
                        ),
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=10,
                        fontweight="bold"
                    )

                # -------------------------------------------------
                # Absolute heatmap
                #
                # Two values are shown:
                #   upper  = normalized value
                #   lower  = absolute value
                # -------------------------------------------------
                else:

                    # Normalized value
                    ax.text(
                        j,
                        i + 0.15,
                        format(
                            df_norm_plot.iloc[i, j],
                            ".3g"
                        ),
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=7
                    )

                    # -------------------------------------------------
                    # Select formatting based on PARAMETER,
                    # not radical.
                    #
                    # i corresponds to the parameter because
                    # df_abs_plot is transposed.
                    # -------------------------------------------------
                    parameter = df_abs_plot.index[i]

                    if parameter == " E_max":
                        abs_fmt = ".3e"

                    elif parameter == " P1/2":
                        abs_fmt = ".3e"

                    elif parameter == " b1":
                        abs_fmt = ".3g"

                    elif parameter == " T1":
                        abs_fmt = ".3e"

                    else:
                        abs_fmt = ".3g"

                    # Absolute value
                    ax.text(
                        j,
                        i - 0.15,
                        format(
                            df_abs_plot.iloc[i, j],
                            abs_fmt
                        ),
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=7,
                        fontweight="bold"
                    )

    # ---------------------------------------------------------
    # Colorbar
    # ---------------------------------------------------------
    cbar = plt.colorbar(im, ax=ax)

    cbar.set_label(
        "colour value relative to TEMPO"
    )

    # ---------------------------------------------------------
    # Final layout
    # ---------------------------------------------------------
    plt.tight_layout()
    plt.show()

