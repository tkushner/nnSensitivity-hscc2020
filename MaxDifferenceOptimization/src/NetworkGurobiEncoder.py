from NeuralNetwork import NeuralNetwork
from NetworkNode import NetworkNode
from gurobipy import *


class GurobiEncoder:

    def __init__(self):
        pass

    def encode_for_node(self, mdl: Model, node_ref: NetworkNode, pref: str, all_vars):
        vy = mdl.addVar(lb=-GRB.INFINITY,vtype=GRB.CONTINUOUS, name="%s_y_%d" % (pref, node_ref.get_id()))
        node_id = node_ref.get_id()
        if node_id in all_vars:
            vz = all_vars[node_id]
        else:
            vz = mdl.addVar(lb=0.0, vtype=GRB.CONTINUOUS, name="%s_z_%d" % (pref, node_ref.get_id()))
            all_vars[node_id] = vz
        # Now add the constraints
        coeff_list = [-1.0]
        var_list = [vz]
        for (w, prev_node) in node_ref.get_incoming():
            coeff_list.append(w)
            prev_node_id = prev_node.get_id()
            assert (prev_node_id in all_vars)
            var_list.append(all_vars[prev_node_id])
        lExpr = LinExpr(node_ref.get_bias())
        lExpr.addTerms(coeff_list, var_list)
        mdl.addConstr(lExpr, GRB.EQUAL, vy)  # vy = sum(wi, previ) + biasj - vz
      #  mdl.addConstr(vz, GRB.GREATER_EQUAL, LinExpr(0))  # vz >= 0
        mdl.addConstr(vy, GRB.LESS_EQUAL, LinExpr(0))  # sum(wi, previ) + biasj <= vz
        # Now add the SOS1 constraint that says that y  __|__ z
        mdl.addSOS(GRB.SOS_TYPE1, [vy, vz])

    def encode(self, mdl: Model, net: NeuralNetwork, pref: str):
        # Iterate through the network inputs
        input_vars = []
        output_vars = []
        all_vars = {}
        input_nodes = net.get_input_nodes()
        for iNode in input_nodes:
            v = mdl.addVar(lb = -GRB.INFINITY, vtype=GRB.CONTINUOUS, name="%s_x_%d" % (pref, iNode.get_id()))
            input_vars.append(v)
            all_vars[iNode.get_id()] = v
        output_nodes = net.get_output_nodes()
        for oNode in output_nodes:
            vz = mdl.addVar(lb = 0.0, vtype=GRB.CONTINUOUS, name="%s_z_%d" % (pref, oNode.get_id()))
            output_vars.append(vz)
            all_vars[oNode.get_id()] = vz
        # Iterate through each layer and encode
        for layer_id in range(net.num_hidden_layers()):
            n_nodes_in_layer = net.get_num_nodes_in_hidden_layer(layer_id)
            for node_idx in range(n_nodes_in_layer):
                node_ref = net.get_hidden_layer_node(layer_id, node_idx)
                # Add two variables for each node_ref
                self.encode_for_node(mdl, node_ref, pref, all_vars)
        # Do the same for the output layer
        for node_ref in output_nodes:
            self.encode_for_node(mdl, node_ref, pref, all_vars)
        return input_vars, output_vars, all_vars



