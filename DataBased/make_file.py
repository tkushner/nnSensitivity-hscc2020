## script to run all the code for HSCC2020
## HSCC 2020
## Taisa Kushner
## taisa.kushner@colorado.edu

import csv
import tempfile
import subprocess
import os

#compile the range propogation files
subprocess.call(["make", "clean"])
subprocess.call(["make"])
#batch run the output range calculcations for networks
subprocess.call(["python3", "batchRun_nnConform.py"])
#perform sensitivity analysis and plot
subprocess.call(["python3","sensitivity_analysis.py"])
