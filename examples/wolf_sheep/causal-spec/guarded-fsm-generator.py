#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 15:52:29 2021

@author: michael
"""

import os
import pandas as pd
from itertools import groupby
import networkx

num_agents = 2

def state(a, da, agent):
    if a==0:
        return agent+"Extinct"
    if da > 0:
        return agent+"Rising"
    if da < 0:
        return agent+"Falling"
    if agent == "grass" and a == 400:
        return "grassSaturated"
    
    if da == 0 and a > 0:
        return None
    raise ValueError(f"No case match for {agent} ({a}, {da}).")

def fiddle(s):
    grass, sheep, wolves = s
    
    if "Extinct" in sheep and "Rising" in wolves:
        wolves = "wolvesFalling"
    if "Extinct" in sheep and "Falling" in grass:
        grass = "grassRising"
        
    return grass, sheep, wolves

def legalEdge(origin, dest):
    g1, s1, w1 = origin
    g2, s2, w2 = dest
    
    if "Rising" in s1 and "Extinct" in s2:
        return False
    if "Rising" in w1 and "Extinct" in w2:
        return False
    
    return True

runs = []

for d in os.listdir("runs"):
    if d == 'stats':
        continue
    
    if f"{num_agents}-agent" not in d:
        continue
    
    runinfo = pd.read_csv(f"runs/{d}/results.csv")

    grass = runinfo['Grass']
    sheep = runinfo['Sheep']
    wolves = runinfo['Wolves']
    
    run = list(zip(zip(grass, grass.diff()), zip(sheep, sheep.diff()), zip(wolves, wolves.diff())))[1:]
    run = [(state(g, ng, "grass"), state(s, ns, "sheep"), state(w, nw, "wolves")) for ((g, ng), (s, ns), (w, nw)) in run]
    run = [fiddle(x) for x in run if None not in x]
    
    runs.append([x[0] for x in groupby(run)][1:])
    
fsm = networkx.DiGraph()

guards = {
    ('grassFalling', 'grassRising'): "grass > sheep",
    ('grassRising', 'grassFalling'): "grass < sheep",
    ('sheepRising', 'sheepRising'): None,
    ('sheepRising', 'sheepFalling'): "(grass < sheep) OR (sheep < wolves)",
    ('wolvesRising', 'wolvesRising'): None,
    ('grassRising', 'grassRising'): None,
    ('grassFalling', 'grassFalling'): None,
    ('wolvesRising', 'wolvesFalling'): "sheep < wolves",
    ('wolvesFalling', 'wolvesRising'): "sheep > wolves",
    ('wolvesExtinct', 'wolvesExtinct'): None,
    ('sheepFalling', 'sheepRising'): "(sheep > wolves) AND (grass > sheep)",
    ('sheepFalling', 'sheepFalling'): None,
    ('sheepFalling', 'sheepExtinct'): "sheep = 0",
    ('grassRising', 'grassSaturated'): "grass = 400",
    ('sheepExtinct', 'sheepExtinct'): None,
    ('wolvesFalling', 'wolvesFalling'): None,
    ('grassSaturated', 'grassSaturated'): None,
    ('wolvesFalling', 'wolvesExtinct'): "wolves = 0"
}

states = set()

for run in runs:
    for first, second in zip(run, run[1:]):
        if legalEdge(first, second):
            if num_agents == 2:
                first = first[1:]
                second = second[1:]
            fsm.add_edge(first, second, label=" AND ".join([f"({guards[ae]})" for ae in zip(first, second) if guards[ae] is not None]))
            states.add(first)
            states.add(second)

for state in states:
    print(state)

networkx.drawing.nx_agraph.write_dot(fsm, f"causal-spec/agents/guarded-fsm-{num_agents}-agent.dot")

