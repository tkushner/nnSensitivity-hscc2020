# Conformance Verification for Neural Network Models of Glucose-Insulin Dynamics

Taisa Kushner, Sriram Sankaranarayanan, and Marc Breton

Contact: Taisa.Kushner@colorado.edu


## Introduction

This contains the "reproducibility" package for the paper titled
"Conformance Verification for Neural Network Models of Glucose-Insulin
Dynamics" conditionally accepted to HSCC 2020.

Inside this package the following are included:

CODE:

a) The sherlock tool for verifying the neural network is included in this package under directory src.
   See here: https://github.com/souradeep-111/sherlock

b) A python script that setsup an encoding of two networks in parallel
to perform monotonicity checking.

c) Glue code in python3 to generate the plots included in the
paper. Note that the actual plots in the paper use matlab. For
convenience, this repeatability package uses python3 using the
matplotlib library.

NEURAL NETWORKS:

Three neural networks are included in the directory BGNetworks.

These networks all have $5$ glucose inputs G(t), G(t-5),
... , G(t-25) and $5$ insulin inputs u(t), .., u(t-25). They have a
single output that represents a blood glucose level prediction
G(t+30). Three different networks are provided.

The networks use the Sherlock format documented here: https://github.com/souradeep-111/sherlock


a) M1: A network with two dense layers. This network is in the file Regular_APNN.nt	

b) M2: A network with two dense layers with the first layer separated for insulin and glucose inputs. This network is in the file SplitLayer_APNN.nt

c) M3: A network with same topology as M2 but has been designed so that the output is guaranteed to be "monotonic" w.r.t
to the insulin inputs.  This network is in the file  WeightCons_APNN.nt




DATA:

We have included some typical BG trends that are observed in patients in the directory glucoseICs
Note that we do not have the permission to include the actual anonymized patient data that was used
in our study reported in the paper. We have a representative set that provides the same behavior that we observed.

If the reader is interested, we can point to some data sets that can
be used as representative blood glucose profiles.  However, the user
will have to contact the provider of the data themselves and sign the
required agreements.


REQUIREMENTS:

- Basic: python3 with numpy, pandas, csv and matplotlib package installed.

- GUROBI library (preferably latest version installed).
The only library that is needed is the MILP solver Gurobi. It's free
for academic purposes and can be downloaded from here :
http://www.gurobi.com/resources/getting-started/mip-basics


## COMPILATION


a) Modify the file Makefile.locale to set the flags HOST_ARCH and GUROBI_PATH

Note that on our machine ( 64 bit Mac OSX with Gurobi 8.1) we have the setting.

> HOST_ARCH=mac64
> GUROBI_PATH=/Library/gurobi810

The Makefile will look for Gurobi headers under

> $(GUROBI_PATH)/$(HOST_ARCH)/include

and libraries under

> $(GUROBI_PATH)/$(HOST_ARCH)/include


b)  To run everything

> python3 make_file.py

to compile and run all the files.


## RUNNING

See COMPILATION instructions above.


## EXPECTED OUTPUT

M1-Regular_4_ranges_by_location.pdf - This file ... 
M1-Regular_sensitivity.pdf
M2-Split_4_ranges_by_location.pdf
M2-Split_sensitivity.pdf
M3-Constrained_4_ranges_by_location.pdf
M3-Constrained_sensitivity.pdf

