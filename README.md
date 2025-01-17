# Conformance Verification for Neural Network Models of Glucose-Insulin Dynamics

Taisa Kushner, Sriram Sankaranarayanan, and Marc Breton

Contact: Taisa.Kushner@colorado.edu


## Introduction

This contains the "reproducibility" package for the paper titled
"Conformance Verification for Neural Network Models of Glucose-Insulin
Dynamics": https://dl.acm.org/doi/abs/10.1145/3365365.3382210



Inside this package the following are included:

CODE:

a) The sherlock tool for verifying the neural network is included in
   this package under directory `DataBased/src`.  See here:
   https://github.com/souradeep-111/sherlock

b) A python script that setsup an encoding of two networks in parallel
to perform monotonicity checking of neural networks, under directory
`MaxDifferenceOptimization`

c) Glue code in python3 to generate the plots included in the
paper. Note that the actual plots in the paper use Matlab. For
convenience, this repeatability package uses python3 using the
matplotlib library.

NEURAL NETWORKS:

Three neural networks are included in the directory `BGNetworks`.

These networks all have $7$ glucose inputs G(t), G(t-5),
... , G(t-30) and $7$ insulin inputs u(t), .., u(t-30). They have a
single output that represents a blood glucose level prediction
G(t+60). Three different networks are provided.

The networks use the Sherlock format documented here: https://github.com/souradeep-111/sherlock


a) M1: A network with two dense layers. This network is in the file M1_Regular_APNN.nt	

b) M2: A network with two dense layers with the first layer separated for insulin and glucose inputs. This network is in the file M2_SplitLayer_APNN.nt

c) M3: A network with same topology as M2 but has been designed so that the output is guaranteed to be "monotonic" w.r.t
to the insulin inputs.  This network is in the file  M3_WeightCons_APNN.nt




DATA:

We have included some typical BG trends that are observed in patients
in the directory `DataBased/glucoseICs` Note that we do not have the
permission to include the actual anonymized patient data that was used
in our study reported in the paper. We have a representative set that
provides the same behavior that we observed.

If the reader is interested, we can point to some data sets that can
be used as representative blood glucose profiles.  However, the user
will have to contact the provider of the data themselves and sign the
required agreements.


## REQUIREMENTS:

1. Python3 with numpy, pandas, csv, os, matplotlib and gurobipy (see
below) packages installed.

2. GUROBI library (please install version 8.1.1).  The only library
that is needed is the MILP solver Gurobi. It's free for academic
purposes and can be downloaded from here :
http://www.gurobi.com/resources/getting-started/mip-basics

- Please ensure you run the following command to install the Gurobi license:
    - `grbgetkey <license-number>`

- Please install `gurobipy` with the following:
    - Navigate to your Gurobi`<installdir>` (the directory that contains the file `setup.py`), and issue the following command:
    - `python setup.py install`

### POTENTIAL TROUBLESHOOTING

If you have a differing version of Gurobi installed and have trouble
linking libraries, please check the following:

- If you are having trouble with library linking, please add the following lines (with proper gurobi version & paths `gurobi810`, `gurobi811`, etc for `<your-gurobi-folder>`) to your `.bashrc` file:
    - `export GUROBI_HOME="/Library/<your-gurobi-folder>/mac64"`
    - `export PATH="${PATH}:${GUROBI_HOME}/bin"`
    - `export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"`
    - `export DYLD_LIBRARY_PATH=/Library/<your-gurobi-folder>/mac64/lib/`


## COMPILATION

### Running data based algorithm

a) Navigate into the `DataBased` folder

b) Modify the file Makefile.locale to set the flags HOST_ARCH and GUROBI_PATH

Note that on our machine ( 64 bit Mac OSX with Gurobi 8.1) we have the setting.

> HOST_ARCH=mac64
> GUROBI_PATH=/Library/gurobi810

The Makefile will look for Gurobi headers under

> $(GUROBI_PATH)/$(HOST_ARCH)/include

and libraries under

> $(GUROBI_PATH)/$(HOST_ARCH)/include

If you have a different version of Gurobi (8.0, 9.0, etc), please change the version in the `LIBS` line in the Makefile (`-lgurobi81`, `-lgurobi90`, etc):

>  LIBS = -lgurobi_c++ -lgurobi81 -lm -D_GLIBCXX_USE_CXX11_ABI=0 -m64 -w

c)  To run everything

> python3 make_file.py

to compile and run all the files.

### Running monotonicity verification algorithm

a) Navigate into the `MaxDifferenceOptimization` folder

b) To run everything: 
> python3 make_file.py


## EXPECTED OUTPUT ( DATA BASED ALG.)

1. Min & Max values of reachable sets of blood glucose values as insulin dose increases by 1Unit across each input location, akin to figures 3&7. These are generated for each network & named as follows, for bolus ranges 0-10 as well as 0-5.
    - M1-Regular_ranges_by_location_0-10.pdf 
    - M1-Regular_ranges_by_location_0-5.pdf
    - M2-Split_ranges_by_location_0-10.pdf
    - M2-Split_ranges_by_location_0-5.pdf
    - M3-Constrained_ranges_by_location_0-10.pdf
    - M3-Constrained_ranges_by_location_0-5.pdf
    
2. Network sensitivity plots, computed by input location, for all networks. These are shown for insulin inputs of 0-11 Units akin to figures 4, 10 and 12 in the paper, and for 0-5 Units akin to figures 5 & 11.
    - M1-Regular_sensitivity_0-10.pdf
    - M1-Regular_sensitivity_0-5.pdf
    - M2-Split_sensitivity_0-10.pdf
    - M2-Split_sensitivity_0-5.pdf
    - M3-Constrained_sensitivity_0-10.pdf
    - M3-Constrained_sensitivity_0-5.pdf

## EXPECTED OUTPUT (MONOTONICITY VERIFICATION)

Text files presenting tests for each insulin input location showing the glucose & input traces identified to result in maximum & minimum differences in predicted blood glucose values between two parallel networks. 

If the conformance property is violated, we find the "Maximum output" to be a positive value. Else, we find a zero value.

1. Results are presented for the three networks as 
    - M1_Regular.output.txt
    - M2_SplitLayer.output.txt
    - M3_WeightCons.output.txt

2. PDF files are plotted in the following files:
    - M1_Regular.PDF
    - M2_SplitLayer.PDF
    - M3_WeightCons.PDF

Note that these results will be plotted and discussed in the revised
version of the paper.




