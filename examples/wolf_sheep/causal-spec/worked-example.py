#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 15:49:08 2021

@author: michael

What is the causal effect of sheep birth rate on the final wolf population in
the two agent model (i.e. with model.grass = False)?

Model params:
    initial_sheep=randint(0, 100),
    initial_wolves=randint(0, 50),
    
    sheep_reproduce=random(),
    wolf_reproduce=random(),
    wolf_gain_from_food=randint(1, 50)
"""
import pygraphviz

agents = ['sheep', 'wolves']

g = pygraphviz.AGraph(strict=False, directed=True, rankdir="LR", newrank=True)

time = 3

def num(agent, time):
    return f"num{agent.capitalize()}_t{time}"

def gainFromFood(agent, time):
    return f"{agent}GainFromFood_t{time}"

def reproduce(agent, time):
    return f"{a}Reproduce_t{time}"

for t in range(time):
    c = g.add_subgraph(name=f"cluster_{t}", label=f"t{t}", pencolor="transparent" if t == 0 else "black")
    n = c.add_subgraph(name=f"num_{t}", rank='same')
    
    for a in agents:
        n.add_node(num(a, t))
        n.add_node(reproduce(a, t))
        n.add_node(gainFromFood("wolves", t))

        if t < time - 1:
            g.add_edge(num(a, t), num(a, t+1))
            g.add_edge(reproduce(a, t), num(a, t+1))
            g.add_edge(reproduce(a, t), reproduce(a, t+1))
    
    if t < time - 1:
        g.add_edge(num("sheep", t), num("wolves", t+1))
        g.add_edge(num("wolves", t), num("sheep", t+1))
        g.add_edge(gainFromFood("wolves", t), num("wolves", t+1))
        g.add_edge(gainFromFood("wolves", t), gainFromFood("wolves", t+1))


g.write(f"wolf-sheep-{len(agents)}-agents-{time}-timesteps.dot")