# Conformance Verification for Neural Network Models of Glucose-Insulin Dynamics

Taisa Kushner, Sriram Sankaranarayanan, and Marc Breton

Contact: Taisa.Kushner@colorado.edu


## Introduction

This contains the "reproducibility" package for the paper titled
"Conformance Verification for Neural Network Models of Glucose-Insulin
Dynamics" conditionally accepted to HSCC 2020.

Reviewer Note: the paper was accepted conditionally on better formalization of the algorithms
presented in this paper. As part of it, we have split our contribution into two algorithms: "data-based"
verification that uses glucose profiles from patients as historical glucose values and "formal monotonicity checking"
that uses two parallel copies of the network to encode monotonicity checking into MILP.


Inside this package the following are included:

CODE:
a) The sherlock tool for verifying the neural network is included in this package under directory `DataBased/src`.
   See here: https://github.com/souradeep-111/sherlock

b) A python script that setsup an encoding of two networks in parallel to perform monotonicity checking of neural networks,
under directory `MaxDifferenceOptimization`

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

We have included some typical BG trends that are observed in patients in the directory `DataBased/glucoseICs`
Note that we do not have the permission to include the actual anonymized patient data that was used
in our study reported in the paper. We have a representative set that provides the same behavior that we observed.

If the reader is interested, we can point to some data sets that can
be used as representative blood glucose profiles.  However, the user
will have to contact the provider of the data themselves and sign the
required agreements.


REQUIREMENTS:

- Basic: python3 with numpy, pandas, csv, os and matplotlib package installed.

- GUROBI library (preferably latest version installed).
The only library that is needed is the MILP solver Gurobi. It's free
for academic purposes and can be downloaded from here :
http://www.gurobi.com/resources/getting-started/mip-basics





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


c)  To run everything

> python3 make_file.py

to compile and run all the files.

### Running monotonicity verification algorithm

a) Navigate into the `MaxDifferenceOptimization` folder

b) To run everything: 
> python3 make_file.py


## EXPECTED OUTPUT ( DATA BASED ALG.)

1. Min & Max values of reachable sets of blood glucose values as insulin dose increases by 1Unit across each input location. Akin to figures 3 & 7 in the paper. These are generated for each network & named as follows.
    - M1-Regular_4_ranges_by_location.pdf 
    - M2-Split_4_ranges_by_location.pdf
    - M3-Constrained_4_ranges_by_location.pdf
    
2. Network sensitivity plots, computed by input location. These are shown for insulin inputs of 0-11 Units akin to figures 4, 10 and 12 in the paper. 
    - M1-Regular_sensitivity.pdf
    - M2-Split_sensitivity.pdf
    - M3-Constrained_sensitivity.pdf

## EXPECTED OUTPUT (MONOTONICITY VERIFICATION)

Text files presenting tests for each insulin input location showing the glucose & input traces identified to result in maximum & minimum differences in predicted blood glucose values between two parallel networks. 

If the conformance property is violated, we find the "Maximum output" to be a positive value. Else, we find a zero value.

1. Results are presented for the three networks as 
    - M1_Regular.output.txt
    - M2_SplitLayer.output.txt
    - M3_WeightCons.output.txt






