#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 15:49:08 2021

@author: michael
"""
import pygraphviz

agents = ['sheep', 'wolves']

grass = False

if grass:
    agents.append('grass')

g = pygraphviz.AGraph(strict=False, directed=True, rankdir="LR", newrank=True)

time = 5

def locations(agent, time):
    return f"{agent}Locations_t{time}"

def num(agent, time):
    return f"num{agent.capitalize()}_t{time}"

g.add_edge("initialSheep", locations("sheep", 0))
g.add_edge("initialWolves", locations("wolves", 0))

for t in range(time):
    c = g.add_subgraph(name=f"cluster_{t}", label=f"t{t}", pencolor="transparent" if t == 0 else "black")
    l = c.add_subgraph(name=f"locations_{t}", rank='same')
    n = c.add_subgraph(name=f"num_{t}", rank='same')
    
    for a in agents:
        # c.add_node(num(a, t))
        l.add_node(locations(a, t))
        n.add_node(num(a, t))

        g.add_edge(locations(a, t), num(a, t))
        
        if t < time-1:
            if a == 'grass':
                g.add_edge("grassRegrowthTime", locations(a, t+1))
            else:
                g.add_edge(locations(a, t), locations(a, t+1), style="dotted")
                g.add_edge(f"{a}Reproduce", locations(a, t+1))
                g.add_edge(f"{a}GainFromFood", locations(a, t+1))



for t in range(time-1):
    g.add_edge(locations("wolves", t), locations("sheep", t+1))
    g.add_edge(locations("sheep", t), locations("wolves", t+1))
    if grass:
        g.add_edge(locations("grass", t), locations("sheep", t+1))


g.write(f"zigzag-{len(agents)}-agents.dot")