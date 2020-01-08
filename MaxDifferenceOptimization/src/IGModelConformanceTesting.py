from NetworkGurobiEncoder import GurobiEncoder
from NeuralNetwork import NeuralNetwork, read_network_from_sherlock_file
from gurobipy import *
import sys
from io import TextIOWrapper
import os

# IGModelConformanceTesting
# This module implements functions for conformance tests
# as proposed in Kushner, Sankaranarayanan, Breton paper.


class ConformanceTestParams:
    basalInsulinMin = 0
    basalInsulinMax = 0.1
    bolusInsulinMin = 0
    bolusInsulinMax = 1.0
    bgMin = 70
    bgMax = 300
    bgFiveMinuteDifference = 25  # Controls how much we BG can change in 5 minutes
    insulinDelta = 0.1 # How much can insulin infusion vary between copies


def conformanceTestModels(net: NeuralNetwork, insulinVaryIdx: int, outFile: TextIOWrapper):
    assert(7 <= insulinVaryIdx < 14)
    # Run a conformance test with insulin varying at index insulinVaryIdx
    enc = GurobiEncoder()
    grb_model = Model('test0_nn_model%d' % insulinVaryIdx)
    #grb_model.setParam('OutputFlag', False)
    # Make two parallel encodings of the network
    (inp_vars1, out_vars1, all_vars1) = enc.encode(grb_model, net,
                                                   'c%d_1' % insulinVaryIdx)
    (inp_vars2, out_vars2, all_vars2) = enc.encode(grb_model, net,
                                                   'c%d_2' % insulinVaryIdx)
    # Add constraints on the glucose
    for j in range(7):
        grb_model.addConstr(inp_vars1[j], GRB.LESS_EQUAL, LinExpr(ConformanceTestParams.bgMax))
        grb_model.addConstr(inp_vars1[j], GRB.GREATER_EQUAL, LinExpr(ConformanceTestParams.bgMin))
        if j < 6:
            grb_model.addConstr(inp_vars1[j+1] - inp_vars1[j], GRB.LESS_EQUAL, LinExpr(ConformanceTestParams.bgFiveMinuteDifference))
            grb_model.addConstr(inp_vars1[j] - inp_vars1[j+1], GRB.LESS_EQUAL, LinExpr(ConformanceTestParams.bgFiveMinuteDifference))
        # Set the two copies of the input variables to be equal
        grb_model.addConstr(inp_vars1[j], GRB.EQUAL, inp_vars2[j])

    # Add constraints on the insulin
    for j in range(7, 14):
        if j == insulinVaryIdx:
            # Add limits on bolus insulin
            grb_model.addConstr(inp_vars1[j], GRB.LESS_EQUAL, LinExpr(ConformanceTestParams.bolusInsulinMax))
            grb_model.addConstr(inp_vars1[j], GRB.GREATER_EQUAL, LinExpr(ConformanceTestParams.bolusInsulinMin))
            # Add how much the insulin values can differ
            grb_model.addConstr(inp_vars2[j] - inp_vars1[j], GRB.LESS_EQUAL, LinExpr(ConformanceTestParams.insulinDelta))
            grb_model.addConstr(inp_vars2[j] - inp_vars1[j], GRB.GREATER_EQUAL, LinExpr(0))
        else:
            # Add limits on basal insulin
            grb_model.addConstr(inp_vars1[j], GRB.LESS_EQUAL, LinExpr(ConformanceTestParams.basalInsulinMax))
            grb_model.addConstr(inp_vars1[j], GRB.GREATER_EQUAL, LinExpr(ConformanceTestParams.basalInsulinMin))
            # Set the two copies of the input variables to be equal
            grb_model.addConstr(inp_vars1[j], GRB.EQUAL, inp_vars2[j])
    grb_model.setObjective(out_vars2[0] - out_vars1[0], GRB.MINIMIZE)
    print('Minimizing output:', file=outFile)
    grb_model.optimize()
    print('Minimum output = ', grb_model.objVal, file=outFile)
    grb_model.setObjective(out_vars2[0] - out_vars1[0], GRB.MAXIMIZE)
    inputs1 = []
    inputs2 = []
    for j in range(7):
        v1 = inp_vars1[j]
        v2 = inp_vars2[j]
        print('Gluc.(t - %d): %f , %f  (Same)' % (30 - 5 * j, v1.x, v2.x), file=outFile)
        inputs1.append(v1.x)
        inputs2.append(v2.x)
    for j in range(7, 14):
        v1 = inp_vars1[j]
        v2 = inp_vars2[j]
        if j == insulinVaryIdx:
            print('Ins(t - %d): %f , %f  <~~~ (Different)' % (65 - 5 * j, v1.x, v2.x), file=outFile)
        else:
            print('Ins(t - %d): %f , %f  (Same)' % (65 - 5 * j, v1.x, v2.x), file=outFile)
        inputs1.append(v1.x)
        inputs2.append(v2.x)
    print('Predicted Gluc. Values: %f, %f' % (out_vars1[0].x, out_vars2[0].x), file=outFile)
    print('Confirming the results by evaluating the network:', file=outFile)
    outs1 = net.eval_network(inputs1)
    outs2 = net.eval_network(inputs2)
    print('Network Eval. results: %f, %f' % (outs1[0], outs2[0]), file=outFile)
    print('------------------------------------------------------', file=outFile)
    print('Maximizing output:', file=outFile)
    grb_model.optimize()
    inputs1 = []
    inputs2 = []
    print('Maximum output = ', grb_model.objVal, file=outFile)
    for j in range(7):
        v1 = inp_vars1[j]
        v2 = inp_vars2[j]
        inputs1.append(v1.x)
        inputs2.append(v2.x)
        print('Gluc.(t - %d): %f , %f (Same)' % (30 - 5 * j, v1.x, v2.x), file=outFile)
    for j in range(7, 14):
        v1 = inp_vars1[j]
        v2 = inp_vars2[j]
        inputs1.append(v1.x)
        inputs2.append(v2.x)
        if j == insulinVaryIdx:
            print('Ins(t - %d): %f , %f  <~~~ (Different)' % (65 - 5 * j, v1.x, v2.x), file=outFile)
        else:
            print('Ins(t - %d): %f , %f  (Same)' % (65 - 5 * j, v1.x, v2.x), file=outFile)
    print('Predicted Gluc. Values: %f, %f' %(out_vars1[0].x, out_vars2[0].x), file=outFile)
    print('Confirming the results by evaluating the network:', file=outFile)
    outs1 = net.eval_network(inputs1)
    outs2 = net.eval_network(inputs2)
    print('Network Eval. results: %f, %f' % (outs1[0], outs2[0]), file=outFile)


def processIGFile(filestem: str, outfileStem: str):
    net = read_network_from_sherlock_file(filestem+'.nt')
    print('Read Network: %s.nt' % filestem)
    assert (net.get_num_inputs() == 14)
    outFileName = outfileStem+'.output.txt'
    outFile = open(outFileName, 'w')
    for j in range(7, 14):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', file=outFile)
        print('Testing insulin input # %d @ time t - %d ' % (j - 6, 65 - 5 * j), file=outFile)
        print('Testing insulin input # %d @ time t - %d ' % (j - 6, 65 - 5 * j))
        print('Outputs dumped to file: %s' % outFileName)
        conformanceTestModels(net, j, outFile)
    outFile.close()

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print('Usage: %s <name of file to test> <output file name>' % sys.argv[0])
    else:
        fileStem = os.path.splitext(sys.argv[1])[0]
        outFile = sys.argv[2]
        processIGFile(fileStem, outFile)
