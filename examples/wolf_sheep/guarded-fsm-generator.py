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

def state(a):
    if a > 0:
        return "Rising"
    if a == 0:
        return "Static"
    if a < 0:
        return "Falling"
    return "INIT"

runs = []

for d in os.listdir("runs"):
    if d == 'stats':
        continue
    
    if "2-agent" in d:
        continue
    
    runinfo = pd.read_csv(f"runs/{d}/results.csv")

    grass = runinfo['Grass'].rolling(15).mean()
    sheep = runinfo['Sheep'].rolling(15).mean()
    wolves = runinfo['Wolves'].rolling(15).mean()
    
    # Get the differences
    grassStates = ["grass"+state(x) for x in grass.diff()]
    sheepStates = ["sheep"+state(x) for x in sheep.diff()]
    wolvesStates = ["wolves"+state(x) for x in wolves.diff()]
    
    assert(len(grassStates) == len(sheepStates) and len(sheepStates) == len(wolvesStates))

    runs.append([x[0] for x in groupby(zip(grassStates, sheepStates, wolvesStates))][1:])
    
fsm = networkx.DiGraph()

labels = set()

guards = {
    'sheepStatic -> sheepFalling': None,
    'sheepStatic -> sheepRising': None,
    'wolvesRising -> wolvesStatic': None,
    'sheepFalling -> sheepRising': "sheep > grass /\ wolves < sheep",
    'grassRising -> grassFalling': "sheep > grass",
    'grassStatic -> grassRising': None,
    'wolvesStatic -> wolvesRising': None,
    'wolvesStatic -> wolvesFalling': None,
    'sheepRising -> sheepFalling': "wolves > sheep \/ sheep > grass",
    'wolvesRising -> wolvesFalling': "wolves > sheep",
    'grassStatic -> grassFalling': None,
    'grassFalling -> grassRising': "grassEating < grassRegrowth",
    'wolvesFalling -> wolvesStatic': "wolves = 0",
    'grassRising -> grassStatic': "grass = 400",
    'wolvesFalling -> wolvesRising': "sheep > wolves",
    'sheepFalling -> sheepStatic': "sheep = 0",
    'grassFalling -> grassStatic': None,
    'sheepRising -> sheepStatic': None
}

for run in runs:
    for first, second in zip(run, run[1:]):
        label=[f"{a} -> {b}" for a, b in zip(first, second) if a != b]
        
        for l in label:
            labels.add(l)
        
        label = [guards[g] for g in label]
        
        if all([l is not None for l in label]):
            fsm.add_edge(first, second, label=", ".join(label))

networkx.drawing.nx_agraph.write_dot(fsm, "causal-spec/guarded-fsm.dot")

print(labels)