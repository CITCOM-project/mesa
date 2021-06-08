#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 09:35:29 2021

@author: michael
"""
import networkx
import pygraphviz
import json

def nodeinfo(n, description="", domain="", direct=False):
    return {'id': str(n), 'description': description, 'domain': domain, 'direct': direct}

def paths_to(graph, target):
    newgraph = networkx.DiGraph(graph.edges())
    to_go = []
    for node in newgraph.nodes():
        if list(networkx.algorithms.simple_paths.all_simple_paths(graph, node, target)) == []:
            to_go.append(node)
    to_go.remove(target)
    for node in to_go:
        newgraph.remove_node(node)
    return newgraph

def causal_graph_for(node):
    networkx.drawing.nx_agraph.write_dot(paths_to(graph, node), f"{node}.dot")

# Read the graph in - for some reason networkx can't do it on its own...
dot = pygraphviz.AGraph("agents.dot")
graph = networkx.DiGraph(dot.edges())

# Check for cycles
cycles = list(networkx.algorithms.cycles.simple_cycles(graph))

if cycles == []:
    print("No cycles :)")
else:
    print("No cycling alowed!\n  "+"\n  ".join(cycles))


# Check for orphan nodes
orphanNodes = [node for node in graph.nodes() if len(graph.out_edges(node)) == 0 and len(graph.in_edges(node)) == 0]

if orphanNodes == []:
    print("No orphan nodes :)")
else:
    print("Orphan nodes:\n  "+"\n  ".join(orphanNodes))


print("")

inputs = [node for node in graph.nodes() if len(graph.in_edges(node)) == 0]
print("INPUTS:\n  "+"\n  ".join(inputs))

outputs = [node for node in graph.nodes() if node not in inputs]
print("OUTPUTS:\n  "+"\n  ".join(outputs))

variables = {'inputs': [nodeinfo(n) for n in inputs], 'outputs': [nodeinfo(n) for n in outputs]}

with open("variables_.json", 'w') as f:
    print(json.dumps(variables, indent=2), file=f)

causal_graph_for("model_wolfExtinction")

