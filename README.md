# Verify NN Dynamics
Taisa Kushner, Sriram Sankaranarayanan, Marc Breton

Verification of neural network dynamics for blood glucose prediction.
Assert: insulin inc -> glucose dec
Uses output range analysis via Sherlock and works for feedforward nets with ReLU activation fns. 

Supply the network weights, biases, structure based on Sherlock format.
Supply initialization vector for BG values.

Default range for basal doses: 0-0.05 U/5min
Default noise on BG values: +/- 5%


Verification of neural network dynamics using output range analysis. 
Feedforward nets with ReLU activation fns.


The only library that is needed is the MILP solver Gurobi. It's free
for academic purposes and can be downloaded from here :
http://www.gurobi.com/resources/getting-started/mip-basics


## Instructions to Compile

Please modify the file Makefile.locale to help find Gurobi.

For a Mac with Gurobi 8.1: 

> HOST_ARCH=mac64
> GUROBI_PATH=/Library/gurobi810

You should feel free to modify these two variables. The Makefile will look for Gurobi headers under

> $(GUROBI_PATH)/$(HOST_ARCH)/include

and libraries under

> $(GUROBI_PATH)/$(HOST_ARCH)/include


Once these are set, you should type

> python3 make_file.py

to compile and run all the files.

