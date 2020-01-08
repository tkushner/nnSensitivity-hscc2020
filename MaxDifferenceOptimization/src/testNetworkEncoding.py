from NetworkGurobiEncoder import GurobiEncoder
from NeuralNetwork import NeuralNetwork, read_network_from_sherlock_file
from gurobipy import *
import random
import sys

def testSimpleNN(filename: str):
    net = read_network_from_sherlock_file(filename)
    print('Read Network: %s' % filename)
    # minSoFar = float('inf')
    # maxSoFar = 0.0
    # for j in range(10000):
    #     inps = [random.uniform(0.0, 1.0) for i in range(net.get_num_inputs())]
    #     outs = net.eval_network(inps)
    #     output_val = outs[0]
    #     if output_val < minSoFar:
    #         minSoFar = output_val
    #     if output_val > maxSoFar:
    #         maxSoFar = output_val
    #
    # print('Range obtained from 10^4 simulations: [%f, %f]' % (minSoFar, maxSoFar))

    grb_model = Model('test0_nn_model')
    grb_model.setParam('OutputFlag', False)
    enc = GurobiEncoder()
    (inp_vars, out_vars, all_vars) = enc.encode(grb_model, net, 'test0')
    for iVar in inp_vars:
        grb_model.addConstr(iVar, GRB.LESS_EQUAL, LinExpr(1.0))
        grb_model.addConstr(iVar, GRB.GREATER_EQUAL, LinExpr(0.0))

    grb_model.setObjective(out_vars[0], GRB.MINIMIZE)
    print('Minimizing output:')
    grb_model.optimize()
    print('Minimum output = ', grb_model.objVal)
    minimizing_sol = []
    for v in inp_vars:
        print('%s %f' % (v.varName, v.x))
        minimizing_sol.append(v.x)
    output_vals = net.eval_network(minimizing_sol)
    print('Value obtained from evaluating network: %f' % output_vals[0])

    grb_model.setObjective(out_vars[0], GRB.MAXIMIZE)
    print('Maximizing output:')
    grb_model.optimize()
    print('Maximum output = ', grb_model.objVal)
    maximizing_sol = []
    for v in inp_vars:
        print('%s %f' % (v.varName, v.x))
        maximizing_sol.append(v.x)
    output_vals = net.eval_network(maximizing_sol)
    print('Value obtained from evaluating network: %f' % output_vals[0])



if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage: %s <name of file to test>' % sys.argv[0])
    else:
        testSimpleNN(sys.argv[1])
