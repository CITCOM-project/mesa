#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 11:37:43 2021

@author: michael
"""
import networkx

from itertools import product

mutex = {
    ("sheepGrowing", "grassSaturated"),
    ("sheepShrinking", "grassSaturated"),
    ("grassShrinking", "grassSaturated"),
    ("grassShrinking", "sheepGrowing"),
    ("sheepExtinct", "grassShrinking")
    }

forbidden = {
    ("sheepExtinct", "sheepGrowing"),
    ("wolvesExtinct", "wolvesGrowing"),
    ("grassSaturated", "grassGrowing"),
    ("grassSaturated", "grassShrinking"),
    ("sheepExtinct", "sheepShrinking"),
    ("wolvesExtinct", "wolvesShrinking"),
    ("grassShrinking", "grassSaturated"),
    ("sheepGrowing", "sheepExtinct"),
    ("wolvesGrowing", "wolvesExtinct")
    }

def implies(p, q):
    return not(p) or q

def nodeOK(n1, n2, n3):
    return all([len(set(x).intersection(set([n1, n2, n3]))) < 2 for x in mutex])

def edgeOK(o, d):
    return (
        all([n not in forbidden for n in zip(o, d)])
        and implies("wolvesGrowing" in o, "sheepExtinct" not in d)
    )

def get_edge_label(g, o, d):
    if o in g and d in g[o] and 'label' in g[o][d]:
        return "("+g[o][d]['label']+")"

def compose(g1, g2, g3):
    comp = networkx.DiGraph(strict=False)
    for (s1, s2, s3) in product(g1.nodes(), g2.nodes(), g3.nodes()):
        if nodeOK(s1, s2, s3):
            comp.add_node((s1, s2, s3))
    for ((o1, o2, o3), (d1, d2, d3)) in product(comp.nodes(), comp.nodes()):
        label = []
        
        label.append(get_edge_label(g1, o1, d1))
        label.append(get_edge_label(g2, o2, d2))
        label.append(get_edge_label(g3, o3, d3))

        # print(o1, d1, get_edge_label(g1, o1, d1))        
        
        label = [x for x in label if x is not None]
        
        if ((o1, d1) in g1.edges() or (o2, d2) in g2.edges() or (o3, d3) in g3.edges()) and edgeOK((o1, o2, o3), (d1, d2, d3)):
                comp.add_edge((o1, o2, o3), (d1, d2, d3), label=" AND ".join(label))
    return comp
    
grass = networkx.DiGraph()
grass.add_edge("grassGrowing", "grassShrinking", label="sheep > grass")
grass.add_edge("grassShrinking", "grassGrowing", label="grass > sheep")
grass.add_edge("grassGrowing", "grassSaturated", label="grass = 400")
networkx.drawing.nx_agraph.write_dot(grass, "causal-spec/agents/grass.dot")

sheep = networkx.DiGraph()
sheep.add_edge("sheepGrowing", "sheepShrinking", label="sheep > grass OR wolves > sheep")
sheep.add_edge("sheepShrinking", "sheepGrowing", label="grass > sheep OR sheep > wolves")
sheep.add_edge("sheepShrinking", "sheepExtinct", label="sheep = 0")
networkx.drawing.nx_agraph.write_dot(sheep, "causal-spec/agents/sheep.dot")

wolves = networkx.DiGraph()
wolves.add_edge("wolvesGrowing", "wolvesShrinking", label="wolves > sheep")
wolves.add_edge("wolvesShrinking", "wolvesGrowing", label="sheep > wolves")
wolves.add_edge("wolvesShrinking", "wolvesExtinct", label="wolves = 0")
networkx.drawing.nx_agraph.write_dot(wolves, "causal-spec/agents/wolves.dot")


comp = compose(wolves, sheep, grass)
networkx.drawing.nx_agraph.write_dot(comp, "causal-spec/agents/wolvesSheepGrass.dot")


# grass.add_edge("init", "grassGrowing")
# sheep.add_edge("init", "sheepGrowing")
# wolves.add_edge("init", "wolvesGrowing")

# comp = networkx.algorithms.operators.all.compose_all([grass, wolves, sheep])
# networkx.drawing.nx_agraph.write_dot(comp, "causal-spec/agents/composition.dot")

