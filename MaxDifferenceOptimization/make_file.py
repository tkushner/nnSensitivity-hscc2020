## Script to run all code performing monotonicity checking using two parallel
## networks
## HSCC 2020
## Taisa Kushner, Sriram Sankaranarayanan,  Marc Breton
## taisa.kushner@colorado.edu

import csv
import tempfile
import subprocess
import os

subprocess.call(["python3", "src/IGModelConformanceTesting.py", "../BGnetworks/M1_Regular_APNN.nt","M1_Regular"])
subprocess.call(["python3", "src/IGModelConformanceTesting.py", "../BGnetworks/M2_SplitLayer_APNN.nt","M2_SplitLayer"])
subprocess.call(["python3", "src/IGModelConformanceTesting.py", "../BGnetworks/M3_WeightCons_APNN.nt","M3_WeightCons"])
