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

reg_sens_low = []
reg_sens_high = []
for file in reg_files:
    _reg_data = pd.read_csv(file,header=None)
    _lows = _reg_data.iloc[:,0:19:2]
    _highs = _reg_data.iloc[:,1:20:2]
    reg_sens_low.append(_lows.diff(axis=1).dropna(axis=1))
    reg_sens_high.append(_highs.diff(axis=1).dropna(axis=1))

split_sens_low = []
split_sens_high = []
for file in split_files:
    _split_data = pd.read_csv(file,header=None)
    _lows = _split_data.iloc[:,0:19:2]
    _highs = _split_data.iloc[:,1:20:2]
    split_sens_low.append(_lows.diff(axis=1).dropna(axis=1))
    split_sens_high.append(_highs.diff(axis=1).dropna(axis=1))

cons_sens_low = []
cons_sens_high = []
for file in cons_files:
    _cons_data = pd.read_csv(file,header=None)
    _lows = _cons_data.iloc[:,0:19:2]
    _highs = _cons_data.iloc[:,1:20:2]
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

# pull those that have positive sensitivity versus negative
reg_frame_pos = reg_frame[reg_frame>0]
reg_frame_neg = reg_frame[reg_frame<=0]

split_frame_pos = split_frame[split_frame>0]
split_frame_neg = split_frame[split_frame<=0]

cons_frame_pos = cons_frame[cons_frame>0]
cons_frame_neg = cons_frame[cons_frame<=0]

print('---Reg total mean pos---')
print(reg_frame_pos.mean(axis=1,skipna=True))
print('--std--')
print(reg_frame_pos.std(axis=1,skipna=True))

print('---Reg total mean neg---')
print(reg_frame_neg.mean(axis=1,skipna=True))
print('--std--')
print(reg_frame_neg.std(axis=1,skipna=True))

print('---Split total mean pos---')
print(split_frame_pos.mean(axis=1,skipna=True))
print('--std--')
print(split_frame_pos.std(axis=1,skipna=True))

print('---Split total mean neg---')
print(split_frame_neg.mean(axis=1,skipna=True))
print('--std--')
print(split_frame_neg.std(axis=1,skipna=True))

print('---Cons total mean pos---')
print(cons_frame_pos.mean(axis=1,skipna=True))
print('--std--')
print(cons_frame_pos.std(axis=1,skipna=True))

print('---Cons total mean neg---')
print(cons_frame_neg.mean(axis=1,skipna=True))
print('--std--')
print(cons_frame_neg.std(axis=1,skipna=True))


# now make plots
plt.close('all')

#cons plot
cons_frame_neg.mean(axis=1,skipna=True).plot(kind='bar')
plt.ylabel('mean change (mg/dL)/unit')
plt.xlabel('look back time')
t_names = ['-30','-25','-20','-15','-10','-5','0']
locs, labels = plt.xticks()
plt.xticks(locs,t_names,rotation='horizontal')
plt.show()
