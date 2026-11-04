# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 23:53:18 2026

@author: marsg
"""

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from matplotlib.pyplot import subplots
pio.renderers.default='browser'

from pandas import DataFrame

import bin_extraction as ex
import fixed_P_plot as fpp
import processing_functions as prc 
# Function designed for handling 2D meshgrid input only. Credits to ChatGPT
def E(c, p,E_max_dF,P_12_dF):
    # Initialize the result array
    E_values = np.zeros_like(c, dtype=float)
    
        
    #designed for meshgrid input: Assumes that c values are redundant along on axis.
    #reverse engineering: regenerates the array which was used to create the meshgrid,so it can be used for iterating
    c=c[0,:] 
    p=p[:,0]
    
    #print(c,p) #helps to check input data
    
    # Loop over each combination of c and p in the result array
    
    for i in range(len(c)):
        for j in range(len(p)):
            concentration = c[i]
            #print(concentration)
            power = p[j]
            
            # Extract values for the given concentration
            E_max = E_max_dF['values'].loc[concentration]
            P_12 = P_12_dF['values'].loc[concentration]
            
            #print(E_max)
            #print(P_12)
            # print('p=', power)
            # print('i:', i)
            # print('j:',j)
            # print('_')
            
            # Calculate Enhancement 
            E_values[j, i] = abs(fpp.Enhancement(power, E_max, P_12))
    
    return E_values

def E_int(C, P, radical):
    # Initialize the result array
    E_values = np.zeros_like(C, dtype=float)
    #E_values=E_values.reshape(20,4)
        
    #designed for meshgrid input: Assumes that c values are redundant along on axis.
    #reverse engineering: regenerates the array which was used to create the meshgrid,so it can be used for iterating
    meshC=C[0,:] 
    meshP=P[:,0]
    
    #keep outside the loop, otherwise it keeps the kernel busy for a while
    # get interpolated E_max and P_1/2 values
    E_max_params = fpp.E_max_int(radical,plot=False)[0]
    P_12_params =  fpp.P_12_int(radical,plot=False)
    
    #print(c,p) #helps to check input data
    
    # Loop over each combination of c and p in the result array
    
    for i in range(len(meshC)):
        for j in range(len(meshP)):
            concentration = meshC[i]
            #print(concentration)
            power = meshP[j]
            
            # get interpolated E_max and P_1/2 values
           
            E_max= fpp.E_max_int.func(concentration,*E_max_params)
            P_12= prc.lin_fit.lin_func(concentration,*P_12_params)
            #print(E_max)
            #print(P_12)
            # print('p=', power)
            # print('i:', i)
            # print('j:',j)
            # print('_')
            
            # Calculate Enhancement 
            E_values[j, i] = abs(fpp.Enhancement(power, E_max, P_12))
    
    return E_values

def e(c,p,E_max_dF,P_12_dF):
     E_max= E_max_dF['values'].loc[c]
     P_12= P_12_dF['values'].loc[c]
     E = fpp.Enhancement(p,E_max,P_12)    
     return E



def ECP_plot(radical,ax=None):
    
    fnames,conc=ex.load_files(radical)

    # experimental data
    E_max_dF= ex.extract_cwise(' E_max',conc,fnames,out=False,bl_corr='on') # careful: baseline mode conditions are not applied
    P_12_dF=  ex.extract_cwise(' P1/2',conc,fnames,out=False)
    
    concs=list(E_max_dF.index)
    
    c= concs 
    p= np.arange(0,50,1)
    
    C,P =np.meshgrid(c,p)
    Z=E(C,P,E_max_dF,P_12_dF)

    
    
        # --- 2. YOUR PLOTLY CODE ---
    fig = go.Figure()
    
    #Add the scattered experimental data points
    fig.add_trace(go.Scatter3d(
      x=C.ravel(), y=P.ravel(), z=Z.ravel(),
      # colorscale='RdBu',
      #opacity=0.9,
     name='experimental data',
     mode='markers',
     marker=dict(color='red',size=4)
     ))
    # showscale=True,
    #   contours={
    #       "x": {"show": True, "color": "black", "highlight": False},
    #        "y": {"show": True, "color": "black", "highlight": False}
    #   }
    #______________________________________________________________________
   
    #***add the interpolated surface***
    
    c=np.linspace(0,10,501)# include last item (+1) or set endpoint=False to get even concentrations
    p= np.arange(0,50,0.1)
    C,P =np.meshgrid(c,p)
    
    Z=E_int(C,P,radical)
    
    fig.add_trace(go.Surface(x=C,y=P,z=Z,
                                colorscale='rdbu_r',
                                name='interpolated curve',
                                opacity=0.9,
                                showscale=True,
                                contours={
                                "x": {"show": True, "color": "black", "highlight": False},
                                "y": {"show": True, "color": "black", "highlight": False}
                                }
                               ))
    #%% max_iterator
    #determine the maximum in C-direction, ie. at fixed P (min of E(C))
    #in addition pulls out the E(2mM) values 
    
    xdata=[]
    ydata=[]
    max_idx=[]
    Ratio=[]
    E_opt=[]
    E_2mM=[]
    for i in range(Z.shape[0]):
        # if E[i,0] >=E_max[-1]*0.95: # no border in this plot
        #     pass
        #else:
        sl=Z[i,:]# slice containing one row at fixed power. 
        ydata.append(P[i,0]) # y of optimum line 
        m=np.argmax(sl)      # find x index of optimum and store in list
        max_idx.append(m)       
        #print(sl)
        xdata.append(C[0,m]) #then translate index into value and store
        
        e_opt= sl[m] # accessing order correct? 
        #print(list(C[0,:]))
        e_2mM= sl[list(C[0,:]).index(2.0)] #if this line raises an error, this is likely because the meshgrid input c contains uneven values. make sure a clean 2.0 is in there   
        ratio= (e_opt/e_2mM)
        Ratio.append(ratio)
        E_opt.append(e_opt)
        E_2mM.append(e_2mM)

    
    if ax==None:
        Fig_ratio,axe_ratio= subplots(figsize=(16,9))
        axe_ratio.plot(p,Ratio)
        axe_ratio.axvline(2)
        axe_ratio.set_xlabel('Power in W')
        axe_ratio.set_ylabel(r'$ \frac{E_{opt}}{E(2mM)}$')
        #ratio_dict=dict(zip(p,Ratio))
    #np.save(Radical_name+'_ratio_dict',ratio_dict)
    else:
        
        ax.plot(p,Ratio)
        
    E_CP_dF=DataFrame(data=[xdata,ydata,max_idx,Ratio,E_opt,E_2mM,p])
    
    #%%
  
    xdata=xdata
    ydata=ydata
    zdata=E_opt
    
    # Add the 3D Green Line
    fig.add_trace(go.Scatter3d(x=xdata, y=ydata, z=zdata,
                               mode='lines',
                               line=dict(color='green', width=6),
                               name='Optimum of E at fixed P'
    ))
    
    # Set Labels, Title, and Initial Camera Angle
    fig.update_layout(
        title=f"{radical} | interpolated_E-CP-3D-plot",
        scene=dict(
            xaxis_title='Concentration',
            yaxis_title='Power',
            zaxis_title='Enhancement',
            camera=dict(
                eye=dict(x=-1.5, y=-1.5, z=1.2)
            )
        ),
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=50)
    )
    
    # Render the plot
    fig.show()
        