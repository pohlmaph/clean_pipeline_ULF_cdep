# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 16:11:24 2025

@author: marsg
"""

#imports 

import numpy as np
from matplotlib.pyplot import subplots
import pandas
from glob import glob
from scipy.optimize import curve_fit

#user defined params

#color list (to be unified with values for color blind people) 
colors=['darkblue','blue','purple','orange','green','lightgreen','brown']


#%% E_max vs c plot
filenames= glob('*Emax_dict_ABS.npy') # import all npy files containing E_max vs C  as dictionary. 

Fig,axe=subplots(figsize=(16,9))
i=0

#iterate through files and plot. 
for file in filenames:
    #Radical_name=file[:file.find('_')]# reset later
    
    dict1=np.load(file,allow_pickle=True).item()
    #print(dict1)
    
    xdata=dict1.keys()
    ydata=dict1.values()
    axe.plot(xdata,ydata, label= file,marker='o',color=colors[i])
    i=i+1
    
axe.set_ylabel('E_max',fontsize=12)
axe.set_xlabel('concentration in mM',fontsize=12)
axe.legend(fontsize=12)
    
#%% Ratio plot
# plots the ratio of Ethe enhancement at optiomal concentration  vs. E(2mM)
ratio_filenames= glob('*_ratio_dict.npy')
Fig2,axe2=subplots(figsize=(16,9))

i=0
for file in ratio_filenames:
    pos=file.find('_')
    Radical_name=file[:pos]
    
    dict2=np.load(file,allow_pickle=True).item()
    #print(dict2)
    
    xdata=dict2.keys()
    ydata=dict2.values()
    axe2.plot(xdata,ydata, label= Radical_name, color=colors[i])
    i=i+1
axe2.set_ylabel('Ratio of E_opt vs. E(2mM)',fontsize=12)
axe2.set_xlabel('Power',fontsize=12)
axe2.legend(fontsize=12)

Fig2.suptitle('Ratio of E_opt vs. E(2mM)')
Fig2.tight_layout()

#%% E-CP max line plot

max_filenames= glob('*_Max_dict_ABS.npy')
Fig3,axe3=subplots(figsize=(16,9))

fp_list= []
fp=2.00
Radical_names=[]
for file in max_filenames:
    pos=file.find('E-CP')
    Radical_name=file[:pos]# reset later
    
    dict3=np.load(file,allow_pickle=True).item()
    #print(dict2)
    
    xdata=list(dict3.keys())
    ydata=list(np.round(list(dict3.values()),3))
    #print(ydata)
    axe3.plot(xdata,ydata, label= Radical_name)
    
    fp_list.append(xdata[ydata.index(fp)])
    Radical_names.append(Radical_name)
axe3.set_ylabel('Power',fontsize=12)
#axe3.set_ylim(0,10)
axe3.set_xlabel('concentration in mM',fontsize=12)
axe3.legend(fontsize=12)


Fig3.suptitle('Maxima of E(C,P) from E-CP contour plot')

Fig_bar,axe_bar=subplots(figsize=(16,9))

Fig_bar.suptitle('Optimal concentration at fixed power of P= '+str(fp)+' W')
axe_bar.set_ylabel('concentration in mM')

bar_dF= pandas.DataFrame(data=fp_list,index=Radical_names,columns=['fp_list'])
bar_dF=bar_dF.sort_values('fp_list')
axe_bar.bar(bar_dF.index, bar_dF['fp_list'], color= colors)

#%% fixed power plot

Powers=[1,1.5,2,10]
fp_filenames= glob('*_fp_dF.csv')
Fig4,axe4=subplots(2,2,figsize=(16,9))
axes4=axe4.reshape(-1)
Fig_Pimg, axe_Pimg= subplots(figsize=(8,4))
Fig_fp_bar,axe_fp_bar=subplots(figsize=(8,4))
fp_dF_list=[]
templist=[]
heights=[]


i=0
for file in fp_filenames:
    pos=file.find('_')
    Radical_name=file[:pos]# reset later
    templist.append(Radical_name)
    dF=pandas.read_csv(file,index_col='Unnamed: 0')
    fp_dF_list.append(dF)
   
    
    concs=dF.columns.to_list()
    concs=[float(s) for s in concs]
    
    for j in range(4):
        #print(concs)
        ydata=dF.iloc[j]
        #print(ydata)
        axes4[j].plot(concs,ydata,label=Radical_name,color=colors[i])
        
        axes4[j].set_title(str(Powers[j])+' W')
        axes4[j].set_ylabel('|1-E|',fontsize=12)
        axes4[j].set_xlabel('concentration in mM')
        
        
        if j==2:
            
            axe_Pimg.plot(concs,ydata,label=Radical_name,color=colors[i])
            axe_Pimg.set_ylabel('|1-E|',fontsize=12)
            axe_Pimg.set_xlabel('concentration in mM')
            
            heights.append(ydata[concs.index(2.0)])
            #axe_fp_bar.barh(Radical_name,ydata[concs.index(2.0)])
            Fig_fp_bar.suptitle('Enhancement at 2mM and 2W')
            axe_fp_bar.set_xlabel('|1-E|',fontsize=12)
            
            
        j=j+1
    i=i+1

fp_bar_dF=pandas.DataFrame(data=heights, index=templist,columns=['widths']).sort_values('widths')
axe_fp_bar.barh(fp_bar_dF.index, fp_bar_dF['widths'],color=colors)
#axe_fp_bar.axhline('TEMPO',color='red')
axes4[2].legend()
axe_Pimg.legend()

Fig4.suptitle('Comparison of Radicals at fixed powers')
Fig_Pimg.suptitle('Comparison of Radicals at a fixed power of 2W ')



# sort alphabetically. only affects later iterations
name_dict_fp= sorted(dict(zip(templist,fp_dF_list)).items())
fp_dF_list=[item[1] for item in name_dict_fp] #overwrites with alphabetically sorted
templist=[item[0] for item in name_dict_fp] #overwrites with alphabetically sorted

#%%param plot A-C
vdF_filenames=glob('*value_dF.csv')

value_dF_list= []
names=[]
hb_lists=[]

FigA,axeA=subplots(2,3,figsize=(16,9))
FigA.suptitle('Radical_comp|parameter plot')
axesA= axeA.reshape(-1)
FigB,axeB=subplots(2,3,figsize=(16,9))
FigB.suptitle('Radical_comp |parameter plot')
axesB= axeB.reshape(-1)
FigC,axeC=subplots(2,3,figsize=(16,9))
FigC.suptitle('Radical_comp |parameter plot')
axesC= axeC.reshape(-1)

Fig_hb,axe_hb= subplots(2,2, figsize=(16,9))
axe_hb= axe_hb.reshape(-1)

Fig_hb2,axe_hb2= subplots(2,2, figsize=(16,9))
axe_hb2= axe_hb2.reshape(-1)

hb_plot_params=['|E_max|',' P1/2',' b1']
k=0
for file in vdF_filenames:
    dF=pandas.read_csv(file, index_col=0)
    #print(dF)
    
    name=file[:file.find('_value_dF')]
    names.append(name)
    dF['1/T1']=1/dF[' T1']
    dF['1/T2']=1/dF[' T2']
    dF['r1']=  1/(dF[' T1']*list(dF.index))
    
    
    value_dF_list.append(dF)
    
    columns=dF.columns    
    pnames=list(['|E_max|','1/T1','1/T2','t_hyp'])+list(columns[4:])
    #print(columns)
   
    
     
    
    hb_list=[]
    
    i=0

    for i in range(len(hb_plot_params)): 
         axe_hb[i].plot(dF[hb_plot_params[i]],marker='o',color=colors[k],label=name)
         axe_hb[i].set_title(hb_plot_params[i])
         axe_hb[i].set_xlabel('concentration')
         
         hb_list.append(dF[hb_plot_params[i]].loc[2.00])
         
         
         
         # axe_hb2[i].barh(names,dF[hb_plot_params[i]].loc[2.00],color=colors[k])
         # #axe_hb2[i].set_title(hb_plot_params[i])
         # axe_hb2[i].set_xlabel(hb_plot_params[i])
         i=i+1
    hb_list.append(r1s[k])                                          #comment out here for start up         <-----
    print(hb_list)
    hb_lists.append(hb_list) 
    
         
    i=0
    for i in range(len(pnames)):
        #print(i)
        if i==4:
            
            def lin_func(x,m,c):
                y=m*x+c
                return y
                               
            params, pcov= curve_fit(lin_func,dF[pnames[i]].index,dF[pnames[i]])
            axesA[i].plot(np.linspace(0,15),lin_func(np.linspace(0,15),*params),color=colors[k])
            print(name,np.sqrt(np.diag(pcov)))
            p12c_list.append(params[0])
            
        if i<6: 
            axesA[i].plot(dF[pnames[i]],marker='o',color=colors[k],label=name)
            axesA[i].set_title(pnames[i])
            axesA[i].set_xlabel('concentration')
            
        elif i<12:
            axesB[i-6].plot(dF[pnames[i]],marker='o',label=name)
            axesB[i-6].set_title(pnames[i])
            axesB[i-6].set_xlabel('concentration')
        elif i<18:
            axesC[i-12].plot(dF[pnames[i]],marker='o',label=name)
            axesC[i-12].set_title(pnames[i])
            axesC[i-12].set_xlabel('concentration')
        else:   break
    k=k+1

hb_dF= pandas.DataFrame(data=hb_lists, columns=hb_plot_params+['r1'], index= names)
i=0
for c in hb_dF.columns:
    axe_hb2[i].barh(names,hb_dF[c],color=colors)
    axe_hb2[i].set_title(c)
    i=i+1
Fig_hb2.tight_layout()    
name_dict_vdF= sorted(dict(zip(names,value_dF_list)).items())
value_dF_list=[item[1] for item in name_dict_vdF] #overwrites with alphabetically sorted
names= [item[0] for item in name_dict_vdF] #overwrites with alphabetically sorted

axesA[0].legend()
axesB[0].legend()
axesC[0].legend()

#%% extract 2mM values

E_2mM= [dF['|E_max|'].loc[2.00] for dF in value_dF_list]
P12_2mM= [dF[' P1/2'].loc[2.00] for dF in value_dF_list]

Fig6,axe6=subplots(1,2,figsize=(16,9))

axe6[0].barh(names,E_2mM)
axe6[1].barh(names,P12_2mM)

axe6[0].set_xlabel('E_max')
axe6[1].set_xlabel(' P_1/2')
Fig6.suptitle('Values at 2mM')
i=0
for name in names:
    axe6[0].text(25,names[i],np.round(E_2mM[i],3))
    axe6[1].text(2,names[i],np.round(P12_2mM[i],3))
    i=i+1

Fig6.tight_layout()



#%% Francks theory

Fig_theory,axe_theory = subplots(1,3,figsize=(16,7))

def leakage_factor(T1,T10):
    f=1-T1/T10
    return f

def linfit(c,a,b):
    y=a*c+b
    return(y)

def E_max_interpol(c,S,b,):
    E_max= -S*(1-np.exp(-b*c))
    return E_max
    

i=0
Figx, axex =subplots()
Fig_int,axe_int= subplots(figsize=(16,9))
#Fig_int.suptitle(Radical_name+' E_max interpolation')

lfs=[]
lfs_int=[] 

r1s=[]
for dF in value_dF_list:
    
    #1/T1 interpolation for obtaining T_10
    axex.plot(dF.index,dF['1/T1'],label=names[i])
    params= curve_fit(linfit,dF.index,dF['1/T1'])[0]
    r1=params[0]
    r1s.append(r1)
    T1_0 =1/params[1]
    axex.plot(dF.index,linfit(dF.index, *params),color='red',linestyle='dashed')
    
    #calculating and plotting the experimental leakage factor
    lf= leakage_factor(dF[' T1'],T1_0)
    lfs.append(lf)
    
    axe_theory[0].plot(dF.index,lf,label=names[i],color=colors[i])
    
    #calculating and plotting the interpolated leakage factor
    
    xdata= np.linspace(dF.index[0],dF.index[-1])
    T1s=  1/linfit(xdata,*params)
    
    lf_int= leakage_factor(T1s,T1_0)
    lfs_int.append(lf_int)
    axe_theory[0].plot(xdata,lf_int,color=colors[i])
    
    #axe labels
    axe_theory[0].set_title('Leakage factor')
    axe_theory[0].set_xlabel('concentration in mM')
    
    
    
    # interpolate E_max 
    
    Emax_int_params,int_sdv= curve_fit(E_max_interpol, list(dF.index),dF[' E_max'],p0=[160,1])
    
    if i==2: Emax_int_params,int_sdv= curve_fit(E_max_interpol, list(dF.index)[:5],dF[' E_max'][:4],p0=[160,1])
    else: pass
        
    
    xdata= np.linspace(dF.index[0],dF.index[-1])
    
    ydata=E_max_interpol(xdata,*Emax_int_params)
    axe_int.plot(dF[' E_max'], color=colors[i])
    axe_int.plot(xdata,ydata,color=colors[i])

    axe_int.set_ylabel(r'Enhancement($\epsilon$)')
    axe_int.set_xlabel('Concentration')
    
    #calculate and plot smax*zeta factor using experimental data( i.e. df[' E_max'])
    
    smaxzeta=(dF[' E_max']-1)/(-lf*638.891)
    
    axe_theory[1].plot(dF.index,smaxzeta,label=names[i],color=colors[i],marker='o')
    
    #calculate and plot smax*zeta factor using interpolated data( i.e. xdata/ydata)
    smaxzeta_int=(ydata-1)/(-lf_int*638.891)
    
    axe_theory[1].plot(xdata,smaxzeta_int,color=colors[i])
    
    axe_theory[1].set_title(r'$s_{max}\cdot\zeta$')
    axe_theory[1].set_xlabel('concentration in mM')
    axe_theory[0].legend()
    
    max_idx=np.argmax(smaxzeta_int)
    axe_theory[1].vlines(xdata[max_idx],0,smaxzeta_int[max_idx],color=colors[i])
    i=i+1
    
    
i=0    
fp_values=list([fp_dF.iloc[3] for fp_dF in fp_dF_list])    
for element in fp_values:
    denominator= [item*638.891 for item in lfs[i]]
    szeta_2W =(element-1)/denominator
    
    print(szeta_2W)
    axe_theory[2].plot([float(value) for value in list(szeta_2W.index)],list(szeta_2W), label=templist[i],color=colors[i])
    # somehow index is not number based, maybe string. x axis is not sorted by value during when plotting against index directly.
    axe_theory[2].set_title(r'$s_{2W}\cdot\zeta$')
    axe_theory[2].set_xlabel('concentration in mM')
    i=i+1
#%% coupling constants
Fig_cc,axe_cc=subplots(1,2,figsize=(16,9))
cc_list=[]

i=0
for dF in value_dF_list:
    if' x3' in list(dF.columns):
        
        
        ccs=dF[' x3']-dF[' x1']
        cc_list.append(ccs)
        axe_cc[0].plot(ccs,label=names[i])
        axe_cc[1].plot((dF[' x3']-dF[' x1'])/2+dF[' x1'])
        i=i+1
    else: 
        print('skipped ' + names[i]+ ' at index ' + str(i))
        # column ' x3' was replaced somewhen in "external" value_dF creation
        i=i+1
axe_cc[0].legend()
axe_cc[0].set_title('coupling constant = x3-x1')
axe_cc[0].set_xlabel('concentration')
axe_cc[0].set_ylabel('coupling constant x3-x1 in a.u.') 


axe_cc[1].set_title('center position')
axe_cc[1].set_xlabel('concentration')
axe_cc[1].set_ylabel('center poisition in a.u.') 


#%% spider plots


Fig_spider,axe_spider= subplots(2,2,figsize=(14,14),subplot_kw={'projection': 'polar'}) 
axes_spider=axe_spider.reshape(-1)
Fig_spider.suptitle('individual parameter values normalized to TEMPO',fontsize=25)


Fig_spider_2,axe_spider_2= subplots(figsize=(10,10),subplot_kw={'projection': 'polar'}) 
Fig_spider_2.suptitle('Parameter values normalized to TEMPO ',fontsize=25)


from math import pi

polygons= list(hb_dF.columns)# polygons representing one parameter
N = len(hb_dF.index)
labels=list(hb_dF.index)
short_labels=['NH2-14','NH2-15N', 'Hydroxy', 'Oxo-14N','Oxo-15N', 'TEMPO']

angles= [2*pi*n/N for n in np.linspace(0,N,N,endpoint=False)]
angles += angles[:1] 

par_names=['E_max', 'P_1/2','linewidth', 'longitudinal relaxivity']
spider_colors=['#eba750','#a740bc','#408dbc','#40bcaa' ]

i=0
hb_dF_norm= hb_dF/hb_dF.iloc[-1]

print('raw')
print(hb_dF)
print("normalized to TEMPO: ")
print(hb_dF_norm) 

for polygon in polygons:
    values= list(hb_dF[polygon])
    values.append(hb_dF[polygon].iloc[0])# duplicate first item to close the circle (specialty of polar plots )
    values=[value/values[-2] for value in values]
    
    # Erste Achse nach oben
    # axes_spider[i].set_theta_offset(pi / 2)
    # axes_spider[i].set_theta_direction(-1)
    
    axes_spider[i].plot(angles,values,linewidth=4,color=spider_colors[i])
    
    axes_spider[i].set_title(par_names[i], fontsize=24, color=spider_colors[i],pad=40)
    
    if i==0:# no difference applied currently
        axes_spider[0].set_thetagrids([angle*(360/(2*pi))for angle in angles][:-1],short_labels,fontsize=20)
        axes_spider[0].tick_params(axis='x', pad=20) 
        
    else:
        axes_spider[i].set_thetagrids([angle*(360/(2*pi))for angle in angles][:-1],short_labels,fontsize=20)
        #axes_spider[i].set_xticklabels([])
        axes_spider[i].tick_params(axis='x', pad=20) 
        
    labels_obj = axes_spider[i].get_xticklabels()
    # 1st label left-aligned
    labels_obj[0].set_horizontalalignment('left')
    # 4th label right-aligned
    labels_obj[3].set_horizontalalignment('right')


    # all in one plot
    values_norm= [value/values[-2] for value in values]
    axe_spider_2.plot(angles,values_norm, label=par_names[i],linewidth=3, color=spider_colors[i])
    axe_spider_2.set_thetagrids([angle*(360/(2*pi))for angle in angles][:-1],labels,fontsize=20)
    axe_spider_2.tick_params(axis='x', pad=40) 
    
    labels_obj = axe_spider_2.get_xticklabels()
    # 1st label left-aligned
    labels_obj[0].set_horizontalalignment('left')
    # 4th label right-aligned
    labels_obj[3].set_horizontalalignment('right')
    
    pos0 = labels_obj[0].get_position()
    labels_obj[0].set_position((pos0[0], pos0[1] + 0.03))  # outward shift
    i=i+1
    
    pos3 = labels_obj[3].get_position()
    labels_obj[3].set_position((pos3[0], pos3[1] + 0.03))  # outward shift


#labels= labels.append(' ')

# Get all radial grid lines

radial_grids = axe_spider_2.yaxis.get_gridlines()

# Find the gridline corresponding to r = 1
# (gridline order corresponds to tick order)
r_ticks = axe_spider_2.get_yticks()

for tick_value, gridline in zip(r_ticks, radial_grids):
    if np.isclose(tick_value, 1.0):          # the ring at r = 1
        #gridline.set_color('black')
        gridline.set_linewidth(3)
        break

    
Fig_spider.tight_layout()
axe_spider_2.legend(loc=(0.95,0),fontsize=15)



    
#%% Savefigs
# Fig.savefig('plots/Radical_comparison_E_max')
# Fig.savefig('plots/Radical_comparison_ratioplot')
# Fig3.savefig('plots/Radical_comparison_E-CP_max')
# Fig4.savefig('plots/Radical_comparison_fixed_power plot')
# Figbar.savefig('plots/Radical_comparison_bar_plot')
# Fig_cc.savefig('plots/Radical_comparison_coupling constants+center')
# Fig_theory.savefig('plots/Radical_comparison_Franck_Theory')    

# overwrite saved plots only execute with caution 
# maybe enter datetime to filename to prevent overwriting