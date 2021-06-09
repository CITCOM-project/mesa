#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 15:52:29 2021

@author: michael
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import json
from math import log

counts = {
    'wolves': [],
    'sheep': [],
    'grass': [],
    }

fig, axs = plt.subplots(nrows=5, ncols=1, figsize=(10, 20))
[grassPlot, sheepPlot, wolvesPlot, run1, energyPlot] = axs

for d in os.listdir("runs"):
    if d == 'stats':
        continue
    with open(f"runs/{d}/config.json") as f:
        config = json.loads("".join(f.readlines()))
        if config['grass']:
            continue

    runinfo = pd.read_csv(f"runs/{d}/results.csv")

    grass = runinfo['Grass']
    sheep = runinfo['Sheep']
    wolves = runinfo['Wolves']
    wolfEnergy = [(x) if x > 0 else 0 for x in runinfo['WolfEnergy']]
    sheepEnergy = [(x) if x > 0 else 0 for x in runinfo['SheepEnergy']]
    
    grassPlot.plot(range(len(grass)), grass, color="green")
    sheepPlot.plot(range(len(sheep)), sheep, color="blue")
    wolvesPlot.plot(range(len(wolves)), wolves, color="gray")
    
    # energyPlot.plot(wolfEnergy, sheepEnergy, color="gray")
    energyPlot.plot(range(len(wolfEnergy)), wolfEnergy, color="gray")
    energyPlot.plot(range(len(sheepEnergy)), sheepEnergy, color="blue")

    # if runinfo.iloc[-1]['Wolves'] > 1000:
    #     # print(d)
    #     # print(runinfo.iloc[-1])
    #     if d == "run-9":
    #         run1.plot(range(len(grass)), grass, color="green", label="Grass")
    #         run1.plot(range(len(sheep)), sheep, color="blue", label="Sheep")
    #         run1.plot(range(len(wolves)), wolves, color="gray", label="Wolves")
    # run1.legend()

    counts['wolves'].append((runinfo.iloc[0]['Wolves'], runinfo.iloc[-1]['Wolves']))
    counts['sheep'].append((runinfo.iloc[0]['Sheep'], runinfo.iloc[-1]['Sheep']))
    counts['grass'].append((runinfo.iloc[0]['Grass'], runinfo.iloc[-1]['Grass']))

run1.scatter([x[0] for x in counts['wolves']], [x[1] for x in counts['wolves']], color="gray")
run1.scatter([x[0] for x in counts['sheep']], [x[1] for x in counts['sheep']], color="blue")

grassPlot.set_title("Grass")
sheepPlot.set_title("Sheep")
wolvesPlot.set_title("Wolves")
run1.set_title("Example run")
energyPlot.set_title("Energy")

for ax in axs[:-1]:
    ax.set_xlabel("Time step")
    ax.set_ylabel("Number of individuals")


run1.set_xlabel("Starting individuals")
run1.set_ylabel("Ending individuals")

energyPlot.set_xlabel("Wolf Energy")
energyPlot.set_ylabel("Sheep Energy")

# for k in counts:
#     counts[k] = sorted(list(set(counts[k])))
#     prev = counts[k][0]
#     newcounts = [prev]

#     for v in counts[k][1:]:
#         if v > prev*1.2:
#             newcounts.append(v)
#             prev = v
#     counts[k] = newcounts

#     print(k, counts[k])

plt.tight_layout()
# plt.savefig("stats.svg")
