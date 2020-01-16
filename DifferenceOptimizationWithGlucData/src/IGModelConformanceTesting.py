from NetworkGurobiEncoder import GurobiEncoder
from NeuralNetwork import NeuralNetwork, read_network_from_sherlock_file
from gurobipy import *
import sys
from io import TextIOWrapper
from PlotResults import plotResults
from typing import List
import os,glob

# IGModelConformanceTesting
# This module implements functions for conformance tests
# as proposed in Kushner, Sankaranarayanan, Breton paper.


class ConformanceTestParams:
    basalInsulinMin = 0
    basalInsulinMax = 0.1
    bolusInsulinMin = 0
    bolusInsulinMax = 5.0
    insulinDelta = 0.1 # How much can insulin infusion vary between copies


def conformanceTestModels(net: NeuralNetwork, insulinVaryIdx: int, outFile: TextIOWrapper, glucValues: List[float]):
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
    assert(len(glucValues) == 7)
    # Add constraints on the glucose
    for j in range(7):
        grb_model.addConstr(inp_vars1[j], GRB.EQUAL, glucValues[j])
        # Set the two copies of the input variables to be equal
        grb_model.addConstr(inp_vars2[j], GRB.EQUAL, glucValues[j])

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
    print('\t Minimizing output:', file=outFile)
    grb_model.optimize()
    print('\t Minimum output = ', grb_model.objVal, file=outFile)
    minOut = grb_model.objVal
    grb_model.setObjective(out_vars2[0] - out_vars1[0], GRB.MAXIMIZE)
    inputs1 = []
    inputs2 = []
    for j in range(7):
        v1 = inp_vars1[j]
        v2 = inp_vars2[j]
        print('\t\t Gluc.(t - %d): %f , %f  (Same)' % (30 - 5 * j, v1.x, v2.x), file=outFile)
        inputs1.append(v1.x)
        inputs2.append(v2.x)
    for j in range(7, 14):
        v1 = inp_vars1[j]
        v2 = inp_vars2[j]
        if j == insulinVaryIdx:
            print('\t\t Ins(t - %d): %f , %f  <~~~ (Different)' % (65 - 5 * j, v1.x, v2.x), file=outFile)
        else:
            print('\t\tIns(t - %d): %f , %f  (Same)' % (65 - 5 * j, v1.x, v2.x), file=outFile)
        inputs1.append(v1.x)
        inputs2.append(v2.x)
    print('\t\t Predicted Gluc. Values: %f, %f' % (out_vars1[0].x, out_vars2[0].x), file=outFile)
    print('\t Confirming the results by evaluating the network:', file=outFile)
    outs1 = net.eval_network(inputs1)
    outs2 = net.eval_network(inputs2)
    print('\t Network Eval. results: %f, %f' % (outs1[0], outs2[0]), file=outFile)
    print('\t ------------------------------------------------------', file=outFile)
    print('\t Maximizing output:', file=outFile)
    grb_model.optimize()
    inputs1 = []
    inputs2 = []
    print('\t Maximum output = ', grb_model.objVal, file=outFile)
    for j in range(7):
        v1 = inp_vars1[j]
        v2 = inp_vars2[j]
        inputs1.append(v1.x)
        inputs2.append(v2.x)
        print('\t\t Gluc.(t - %d): %f , %f (Same)' % (30 - 5 * j, v1.x, v2.x), file=outFile)
    for j in range(7, 14):
        v1 = inp_vars1[j]
        v2 = inp_vars2[j]
        inputs1.append(v1.x)
        inputs2.append(v2.x)
        if j == insulinVaryIdx:
            print('\t\t Ins(t - %d): %f , %f  <~~~ (Different)' % (65 - 5 * j, v1.x, v2.x), file=outFile)
        else:
            print('\t\t Ins(t - %d): %f , %f  (Same)' % (65 - 5 * j, v1.x, v2.x), file=outFile)
    print('\t\t Predicted Gluc. Values: %f, %f' %(out_vars1[0].x, out_vars2[0].x), file=outFile)
    print('\t\t Confirming the results by evaluating the network:', file=outFile)
    outs1 = net.eval_network(inputs1)
    outs2 = net.eval_network(inputs2)
    print('\t\t Network Eval. results: %f, %f' % (outs1[0], outs2[0]), file=outFile)
    maxOut = grb_model.objVal
    return (minOut, maxOut)


def processIGFile(filestem: str, csvFileList, outfileStem: str):
    net = read_network_from_sherlock_file(filestem+'.nt')
    print('Read Network: %s.nt' % filestem)
    resultHi={}
    resultLo={}
    assert (net.get_num_inputs() == 14)
    outFileName = outfileStem+'.output.txt'
    outFile = open(outFileName, 'w')
    for csvFileName in csvFileList:
        print('Processing %s' % csvFileName, file=outFile)
        csvFile = open(csvFileName, 'r', encoding='utf-8-sig')
        glucValues = []
        for line in csvFile:
            line = line.strip()
            #print(line)
            if (line != ''):
                glucValues.append(float(line))
        csvFile.close()
        
        for j in range(7, 14):
            print('\t ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', file=outFile)
            print('\t Testing insulin input # %d @ time t - %d ' % (j - 6, 65 - 5 * j), file=outFile)
            print('\t Testing insulin input # %d @ time t - %d ' % (j - 6, 65 - 5 * j))
            (l,u) = conformanceTestModels(net, j, outFile, glucValues)
            k = j - 7
            if k in resultHi:
                resultHi[k] = max(resultHi[k], u)
            else:
                resultHi[k] = u
            if k in resultLo:
                resultLo[k] = min(resultLo[k],l)
            else:
                resultLo[k] = l
    plotResults(resultLo, resultHi,  outfileStem)
    outFile.close()

if __name__ == '__main__':
    if len(sys.argv) <= 3:
        print('Usage: %s <name of file to test> <output file name> <directory for csv files>' % sys.argv[0])
    else:
        fileStem = os.path.splitext(sys.argv[1])[0]
        outFile = sys.argv[2]
        csvDir = sys.argv[3]
        csvFiles = glob.glob(csvDir+'/*.csv')
        print('CSV Files:', csvFiles)
        processIGFile(fileStem,  csvFiles, outFile)
