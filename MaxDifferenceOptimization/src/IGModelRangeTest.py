from NetworkGurobiEncoder import GurobiEncoder
from NeuralNetwork import NeuralNetwork, read_network_from_sherlock_file
from gurobipy import *
import random
import sys


# This function simply allows the inputs of a single insulin-glucose network to
# vary and computes the possible range of outputs.
def computeOutputRangeForMDL(filename: str):
    net = read_network_from_sherlock_file(filename)
    print('Read Network: %s' % filename)
    assert( net.get_num_inputs() == 14)
    # According to Taisa:
    # inputs from left to right are glucose (t-30min up to t), followed by insulin:
    #
    # [ G(t-30), G(t-25), G(t-20), G(t-15), G(t-10), G(t-5), G(t),
    #    I(t-30), I(t-25), I(t-20), I(t-15), I(t-10), I(t-5), I(t) ]
    grb_model = Model('test0_nn_model')
    grb_model.setParam('OutputFlag', False)
    enc = GurobiEncoder()
    (inp_vars, out_vars, all_vars) = enc.encode(grb_model, net, 'test0')
    for j in range(7):
        grb_model.addConstr(inp_vars[j], GRB.LESS_EQUAL, LinExpr(180))
        grb_model.addConstr(inp_vars[j], GRB.GREATER_EQUAL, LinExpr(70))
        if j < 6:
            grb_model.addConstr(inp_vars[j+1] - inp_vars[j], GRB.LESS_EQUAL, LinExpr(10))
            grb_model.addConstr(inp_vars[j] - inp_vars[j+1], GRB.LESS_EQUAL, LinExpr(10))
    for j in range(7, 14):
        grb_model.addConstr(inp_vars[j], GRB.LESS_EQUAL, LinExpr(10.0))
        grb_model.addConstr(inp_vars[j], GRB.GREATER_EQUAL, LinExpr(0.0))
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
        computeOutputRangeForMDL(sys.argv[1])

