#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:09:48 2021

@author: michael
"""
from wolf_sheep.model import WolfSheep

from random import randint
from random import random
from random import choice

import json
import os

def run(
    height=20,
    width=20,
    initial_sheep=100,
    initial_wolves=50,
    sheep_reproduce=0.04,
    wolf_reproduce=0.05,
    wolf_gain_from_food=20,
    grass=False,
    grass_regrowth_time=30,
    sheep_gain_from_food=4,
    step_count=300,
    infodir="runs",
    configfile="config.json",
    statsfile="results.csv"
    ):
    
    params = {
        "height": height,
        "width": width,
        "initial_sheep": initial_sheep,
        "initial_wolves": initial_wolves,
        "sheep_reproduce": sheep_reproduce,
        "wolf_reproduce": wolf_reproduce,
        "wolf_gain_from_food": wolf_gain_from_food,
        "grass": grass,
        "grass_regrowth_time": grass_regrowth_time,
        "sheep_gain_from_food": sheep_gain_from_food
        }
    
    with open(f"{infodir}/{configfile}", 'w') as f:
        print(json.dumps(params, indent=2), file=f)
    
    model = WolfSheep(
        height=height,
        width=width,
        initial_sheep=initial_sheep,
        initial_wolves=initial_wolves,
        sheep_reproduce=sheep_reproduce,
        wolf_reproduce=wolf_reproduce,
        wolf_gain_from_food=wolf_gain_from_food,
        grass=grass,
        grass_regrowth_time=grass_regrowth_time,
        sheep_gain_from_food=sheep_gain_from_food
        )

    for i in range(step_count):
        grass, sheep, wolves = model.get_counts()
        
        # if sheep > 10000 or wolves > 10000:
        #     break
            
        print(f"  step {i}")
        model.step()
        stats = model.datacollector.get_model_vars_dataframe()
        stats.to_csv(f"{infodir}/{statsfile}")

for i in range(10):
    print("RUN", i)
    rundir = f"run-2-agent-300-steps-{i}"
    if not os.path.exists(f"runs/{rundir}"):
        os.mkdir(f"runs/{rundir}")
    
    run(
        initial_sheep=randint(0, 100),
        initial_wolves=randint(0, 50),
        sheep_reproduce=random(),
        wolf_reproduce=random(),
        wolf_gain_from_food=randint(1, 50),
        grass=False,
        grass_regrowth_time=randint(1, 50),
        sheep_gain_from_food=randint(1, 10),
        step_count=300,
        infodir=f"runs/{rundir}"
    )