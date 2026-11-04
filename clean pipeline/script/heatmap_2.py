# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 15:38:35 2026

@author: marsg
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import bin_extraction as ex
import processing_functions as prc

def generate_dF(radicals, short_labels, sel_params=[' E_max', ' P1/2', ' b1', ' T1', ' T2'], 
                norm_to=-1, exclude_rules=None, target_conc=2.0):
    """
    Generate absolute and normalized DataFrames dynamically.
    
    Parameters
    ----------
    exclude_rules : dict, optional
        Mapping of radical names to fit exclusion options, 
        e.g., {'4-Hydroxy-14N-TEMPO_old': -1}
    target_conc : float
        Concentration index value to extract for general parameters.
    """
    if exclude_rules is None:
        exclude_rules = {}

    dF_abs = pd.DataFrame(index=short_labels)
    dF_norm = pd.DataFrame(index=short_labels)
    
    for param in sel_params:
        values_abs = []
        
        for radical in radicals:
            fnames, conc = ex.load_files(radical)
            ex_dF = ex.extract_cwise(param, conc, fnames, out=False)
            concs = list(ex_dF.index)
            
            # Dynamic exclusion rule lookup
            exclude_val = exclude_rules.get(radical, None)
            
            if param in [' T1', ' T2']: 
                r_val, _, _ = prc.get_r(radical, concs, ex_dF['values'], plot=False, exclude=exclude_val)
                values_abs.append(r_val)
            else: 
                values_abs.append(ex_dF['values'].loc[target_conc])
        
        # Scale dynamically based on norm_to index
        baseline_val = values_abs[norm_to]
        values_norm = [value / baseline_val for value in values_abs]
        
        dF_norm[param] = values_norm
        dF_abs[param] = values_abs
        
    return dF_abs, dF_norm



def plot_mosaic_heatmap(
    df_abs,
    df_norm,
    absolute=False,
    cmap="coolwarm",
    figsize=None,
    show_values=True,
    fmt_norm=".3g",
    fmt_abs=".3g",
    par_names=None,
    vmin=0.8,
    vmax=1.2,
    norm_y_offset=0.18,
    abs_y_offset=-0.12,
    norm_fontsize=7,
    abs_fontsize=8
):
    """
    Plot a scalable mosaic-style heatmap.

    Parameters
    ----------
    df_abs : pandas.DataFrame
        DataFrame containing absolute parameter values.

    df_norm : pandas.DataFrame
        DataFrame containing normalized parameter values.
        Must have the same shape/index/columns as df_abs.

    absolute : bool
        If False, plot normalized values.
        If True, plot absolute values with normalized values
        shown above/below them.

    cmap : str
        Matplotlib colormap.

    figsize : tuple or None
        Figure size. If None, it is determined automatically
        from the DataFrame dimensions.

    show_values : bool
        Whether to show values inside cells.

    fmt_norm : str
        Format string for normalized values.

    fmt_abs : str
        Format string for absolute values.

    par_names : list or None
        Labels for the x-axis. If None, df_norm.columns are used.

    vmin, vmax : float
        Limits of the heatmap colour scale.

    norm_y_offset : float
        Vertical position of normalized annotation.

    abs_y_offset : float
        Vertical position of absolute annotation.

    norm_fontsize : int
        Font size of normalized values.

    abs_fontsize : int
        Font size of absolute values.
    """

    # ---------------------------------------------------------
    # Check DataFrames
    # ---------------------------------------------------------

    if df_abs.shape != df_norm.shape:
        raise ValueError(
            "df_abs and df_norm must have the same shape."
        )

    if not df_abs.index.equals(df_norm.index):
        raise ValueError(
            "df_abs and df_norm must have the same row labels."
        )

    if not df_abs.columns.equals(df_norm.columns):
        raise ValueError(
            "df_abs and df_norm must have the same column labels."
        )
        
    

    # ---------------------------------------------------------
    # Get dimensions dynamically
    # ---------------------------------------------------------

    n_rows, n_cols = df_norm.shape

    # ---------------------------------------------------------
    # Automatic figure size
    # ---------------------------------------------------------

    if figsize is None:

        # Scale approximately with number of columns/rows
        figsize = (
            max(6, n_cols * 1.25),
            max(4, n_rows * 1.0)
        )

    fig, ax = plt.subplots(figsize=figsize)

    # ---------------------------------------------------------
    # Title
    # ---------------------------------------------------------

    if absolute:
        fig.suptitle(
            "Experimental parameter values at 2 mM",
            x=0.45,
            ha="center"
        )
    else:
        fig.suptitle(
            "parameter values normalized to TEMPO",
            x=0.45,
            ha="center"
        )

    # ---------------------------------------------------------
    # Select data for heatmap
    # ---------------------------------------------------------

    if absolute:
        heatmap_data = df_norm
    else:
        heatmap_data = df_norm

    # ---------------------------------------------------------
    # Draw heatmap
    # ---------------------------------------------------------

    im = ax.imshow(
        heatmap_data.values,
        cmap=cmap,
        aspect="equal",
        vmin=vmin,
        vmax=vmax
    )

    # ---------------------------------------------------------
    # X-axis
    # ---------------------------------------------------------

    ax.set_xticks(np.arange(n_cols))

    if par_names is None:
        x_labels = df_norm.columns
    else:

        if len(par_names) != n_cols:
            raise ValueError(
                f"par_names contains {len(par_names)} labels, "
                f"but the DataFrame has {n_cols} columns."
            )

        x_labels = par_names

    ax.set_xticklabels(
        x_labels,
        fontsize=11
    )

    # ---------------------------------------------------------
    # Y-axis
    # ---------------------------------------------------------

    ax.set_yticks(np.arange(n_rows))

    ax.set_yticklabels(
        df_norm.index,
        fontsize=11
    )

    # ax.set_ylabel(
    #     "Radicals",
    #     fontsize=13,
        
    # )

    ax.set_xlabel(
        "Parameters",
        fontsize=13
    )

    # ---------------------------------------------------------
    # Mosaic grid
    # ---------------------------------------------------------

    ax.set_xticks(
        np.arange(-0.5, n_cols, 1),
        minor=True
    )

    ax.set_yticks(
        np.arange(-0.5, n_rows, 1),
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
    # Make sure the complete matrix is visible
    # ---------------------------------------------------------

    ax.set_xlim(
        -0.5,
        n_cols - 0.5
    )

    ax.set_ylim(
        n_rows - 0.5,
        -0.5
    )

    # ---------------------------------------------------------
    # Annotations
    # ---------------------------------------------------------

    if show_values:

        for i in range(n_rows):

            for j in range(n_cols):

                # ---------------------------------------------
                # Normalized plot
                # ---------------------------------------------

                if not absolute:

                    ax.text(
                        j,
                        i,
                        format(
                            df_norm.iloc[i, j],
                            fmt_norm
                        ),
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=norm_fontsize,
                        fontweight="bold"
                    )

                # ---------------------------------------------
                # Absolute plot
                # ---------------------------------------------

                else:

                    # Normalized value
                    ax.text(
                        j,
                        i + norm_y_offset,
                        format(
                            df_norm.iloc[i, j],
                            fmt_norm
                        ),
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=norm_fontsize
                    )

                    # Absolute value
                    ax.text(
                        j,
                        i + abs_y_offset,
                        format(
                            df_abs.iloc[i, j],
                            fmt_abs
                        ),
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=abs_fontsize,
                        fontweight="bold"
                    )

    # ---------------------------------------------------------
    # Colorbar
    # ---------------------------------------------------------

    cbar = plt.colorbar(
        im,
        ax=ax
    )

    cbar.set_label(
        "colour value relative to TEMPO"
    )

    # ---------------------------------------------------------
    # Layout
    # ---------------------------------------------------------

    #plt.tight_layout()

    plt.show()

    return fig, ax

