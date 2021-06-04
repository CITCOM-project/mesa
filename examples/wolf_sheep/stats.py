#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 15:52:29 2021

@author: michael
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

counts = {
    'start_wolves': [],
    'end_wolves': [],
    'start_sheep': [],
    'end_sheep': [],
    'start_grass': [],
    'end_grass': []
    }

fig, [grassPlot, sheepPlot, wolvesPlot, run1] = plt.subplots(nrows=4, ncols=1, figsize=(8, 16))
    

for d in os.listdir("runs"):
    runinfo = pd.read_csv(f"runs/{d}/results.csv")
    
    grass = runinfo['Grass']
    sheep = runinfo['Sheep']
    wolves = runinfo['Wolves']
    
    grassPlot.plot(range(len(grass)), grass, color="green")
    sheepPlot.plot(range(len(sheep)), sheep, color="blue")
    wolvesPlot.plot(range(len(wolves)), wolves, color="gray")
    
    if runinfo.iloc[-1]['Wolves'] > 1000:
        print(d)
        print(runinfo.iloc[-1])
        if d == "run-9":
            run1.plot(range(len(grass)), grass, color="green")
            run1.plot(range(len(sheep)), sheep, color="blue")
            run1.plot(range(len(wolves)), wolves, color="gray")
    
    counts['start_wolves'].append(runinfo.iloc[0]['Wolves'])
    counts['end_wolves'].append(runinfo.iloc[-1]['Wolves'])
    counts['start_sheep'].append(runinfo.iloc[0]['Sheep'])
    counts['end_sheep'].append(runinfo.iloc[-1]['Sheep'])
    counts['start_grass'].append(runinfo.iloc[0]['Grass'])
    counts['end_grass'].append(runinfo.iloc[-1]['Grass'])

for k in counts:
    counts[k] = sorted(list(set(counts[k])))
    prev = counts[k][0]
    newcounts = [prev]
    
    for v in counts[k][1:]:
        if v > prev*1.2:
            newcounts.append(v)
            prev = v
    counts[k] = newcounts
        
    print(k, counts[k])    