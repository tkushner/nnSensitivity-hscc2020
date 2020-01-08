## script to batch run output range for networks
## HSCC 2020
## Taisa Kushner
## taisa.kushner@colorado.edu


import csv
import tempfile
import subprocess
import os

#pull the list of glucose initial trace files from glucIC directory
path = './glucICs/'

glucIC_files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            glucIC_files.append(os.path.join(r, file))

# run output range analysis for three networks
# populates the OutputRanges directory with reachable sets for insulin doses ranging 0-11 units in 1 unit intervals
# for each input location

for IC in glucIC_files:
    #Regular
    subprocess.call(["./run_file", "0.0", "1.0", "../BGnetworks/M1_Regular_APNN.nt", IC, "./OutputRanges/M1_Regular_"+str(IC[-7:-4])+".csv"])
    #Split structure
    subprocess.call(["./run_file", "0.0", "1.0", "../BGnetworks/M2_SplitLayer_APNN.nt", IC, "./OutputRanges/M2_SplitLayer_"+str(IC[-7:-4])+".csv"])
    #weight constrained
    subprocess.call(["./run_file", "0.0", "1.0", "../BGnetworks/M3_WeightCons_APNN.nt", IC, "./OutputRanges/M3_WeightCons_"+str(IC[-7:-4])+".csv"])
