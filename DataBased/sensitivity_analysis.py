#perform sensitivity analysis for the output from batchRun_nnConform
import numpy as np
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt

#parse and import the the files from batchRun_nnConform
path = './OutputRanges/'

reg_files = [] #regular
split_files = [] #split network structure
cons_files = [] #weight constrained

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            if 'Regular' in file:
                reg_files.append(os.path.join(r,file))
            elif 'SplitLayer' in file:
                split_files.append(os.path.join(r,file))
            elif 'WeightCons' in file:
                cons_files.append(os.path.join(r,file))
            else:
                print('improper file name found: '+str(os.path.join(r,file)))

reg_files.sort()
split_files.sort()
cons_files.sort()

reg_data = []
reg_sens_low = []
reg_sens_high = []
for file in reg_files:
    _reg_data = pd.read_csv(file,header=None)
    _lows = _reg_data.iloc[:,0:19:2]
    _highs = _reg_data.iloc[:,1:20:2]
    reg_data.append(_reg_data)
    reg_sens_low.append(_lows.diff(axis=1).dropna(axis=1))
    reg_sens_high.append(_highs.diff(axis=1).dropna(axis=1))

split_data = []
split_sens_low = []
split_sens_high = []
for file in split_files:
    _split_data = pd.read_csv(file,header=None)
    _lows = _split_data.iloc[:,0:19:2]
    _highs = _split_data.iloc[:,1:20:2]
    split_data.append(_split_data)
    split_sens_low.append(_lows.diff(axis=1).dropna(axis=1))
    split_sens_high.append(_highs.diff(axis=1).dropna(axis=1))

cons_data = []
cons_sens_low = []
cons_sens_high = []
for file in cons_files:
    _cons_data = pd.read_csv(file,header=None)
    _lows = _cons_data.iloc[:,0:19:2]
    _highs = _cons_data.iloc[:,1:20:2]
    cons_data.append(_cons_data)
    cons_sens_low.append(_lows.diff(axis=1).dropna(axis=1))
    cons_sens_high.append(_highs.diff(axis=1).dropna(axis=1))

reg_low_big = pd.concat(reg_sens_low,axis=1)
reg_high_big = pd.concat(reg_sens_high,axis=1)
reg_frame = pd.concat([reg_low_big, reg_high_big],axis=1)

split_low_big = pd.concat(split_sens_low,axis=1)
split_high_big = pd.concat(split_sens_high,axis=1)
split_frame = pd.concat([split_low_big,split_high_big],axis=1)

cons_low_big = pd.concat(cons_sens_low,axis=1)
cons_high_big = pd.concat(cons_sens_high,axis=1)
cons_frame = pd.concat([cons_low_big,cons_high_big],axis=1)

def PlotRanges(df_lst, netname, IDX,range_max):
    #get and plot the means for a specific index location
    df = df_lst[IDX]
    MAX=range_max*2
    df_l = df.iloc[:,0:MAX:2]
    df_h = df.iloc[:,1:MAX:2]

    fig = plt.figure(dpi=300)
    #subplot each input location
    for idx in df_l.index:
        lows = df_l.iloc[idx,:].reset_index(drop=True)
        highs = df_h.iloc[idx,:].reset_index(drop=True)
        lows.index += 1
        highs.index += 1
        df_sub = pd.concat([lows,highs],axis=1)
        df_sub.columns = ['low','high']
        ax_num = fig.add_subplot(240+idx+1)
        df_sub.plot(ax=ax_num,marker='o')
        ax_num.set_xlim([0,range_max])
        plt.gca().legend_.remove()

    plt.savefig(netname+'_ranges_by_location_0-'+str(range_max)+'.pdf')


def PlotSensitivity(df, netname, printVal,range_max):
    #split positive and negative sensitivities
    MAX=range_max*2
    df_pos = df[df>0]
    df_pos=df_pos.iloc[:,df_pos.columns<=MAX] #pull insulin ranges desired
    df_neg = df[df<=0]
    df_neg=df_neg.iloc[:,df_neg.columns<=MAX]

    # print the values, if desired (printVal = True)
    if printVal:
        print('---'+netname+' total mean neg---')
        print(df_neg.mean(axis=1,skipna=True))
        print('--std--')
        print(df_neg.std(axis=1,skipna=True))

        print('---'+netname+' total mean pos---')
        print(df_pos.mean(axis=1,skipna=True))
        print('--std--')
        print(df_pos.std(axis=1,skipna=True))

    #plot means for positive and negative sensitivities, save as pdf
    df_mean = pd.concat([df_neg.mean(axis=1,skipna=True),df_pos.mean(axis=1,skipna=True)],axis=1)
    df_mean.columns=['Negative','Positive']
    df_mean.plot(kind='bar',stacked=True)
    plt.ylabel('mean change (mg/dL)/unit')
    plt.xlabel('look back time')
    plt.title(netname+' network sensitivity 0-'+str(range_max))
    t_names = ['-30','-25','-20','-15','-10','-5','0']
    locs, labels = plt.xticks()
    plt.xticks(locs,t_names,rotation='horizontal')
    plt.gca().legend_.remove()
    plt.savefig(netname+'_sensitivity_0-'+str(range_max)+'.pdf')

#create pdf plots for the three networks
PlotSensitivity(reg_frame,'M1-Regular',False,10)
PlotSensitivity(split_frame,'M2-Split',False,10)
PlotSensitivity(cons_frame,'M3-Constrained',False,10)

# and for insulin ranges 0-5 only
PlotSensitivity(reg_frame,'M1-Regular',False,5)
PlotSensitivity(split_frame,'M2-Split',False,5)
PlotSensitivity(cons_frame,'M3-Constrained',False,5)

#create a pdf plot for the random selected ranges by location plots
PlotRanges(reg_data,'M1-Regular',0,10)
PlotRanges(split_data,'M2-Split',0,10)
PlotRanges(cons_data,'M3-Constrained',0,10)

PlotRanges(reg_data,'M1-Regular',0,5)
PlotRanges(split_data,'M2-Split',0,5)
PlotRanges(cons_data,'M3-Constrained',0,5)
