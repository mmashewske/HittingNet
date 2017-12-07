#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  graphMake.py
#  
#  Copyright 2017 Matthew Mashewske <matthew@matthew-W65-67SJ>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys
import networkx as nx
from random import choice

def isSpecial(command):
    '''Checks if special specific move inputs are in a command input.
    '''
    specials = "qbhgwzscdn"
    if any(buttons in command for buttons in list(specials) ):
        #print(command)
        return True
    return False

def isBlockbuster(command):
    '''Checks if blockbuster specific command inputs are in a move input.
    '''
    blockbusters = ["i+o", "j+k"]
    if any(buttons in command for buttons in blockbusters ):
        return True
    return False

def commandType(command):
    '''Takes a string representing a command input and returns an integer representing its type.
    '''
    if isBlockbuster(command):
        return 5
    elif isSpecial(command):
        return 4
    elif 'p' in command or 'l' in command:
        return 3
    elif 'o' in command or 'k' in command:
        return 2
    elif "(i+j)" in command:
        return 0
    return 1

def isLink(move1, move2):
    '''Checks if the startup frames of move2 are less than the on-hit frames of move1.
    '''
    val1 = move1['onhit'].split()[0].replace('"','')
    val2 = int(move2['startup'].split()[0].replace('"',''))
    
    try:
        return int(val1) > val2
    except:
        if(val1 == "s"):
            return 0
        elif(val1 == "o"):
            return 3
        else:
            return 2
    
def makeGraph():
    '''
    Each row is a separate move
    Each move is a parent feature on the graph, has start up frames, damage, and type (normal, special, blockbuster)
    Each parent feature has microfeatures representing 
    '''
    rows = open('bigband.csv','r').read().split('\n')[1:]
    graph = nx.DiGraph()
    nodeDict = {}
    for row in rows:
        values = row.lower().split(',')
        if len(values) < 12:
            continue
            
        #print(len(values))
        graph.add_node(len(graph), command = values[0], damage=values[1], meter=values[2], startup=values[4], onhit=values[9],cancelLevel=commandType(values[0]))
    for node in graph.nodes():
        for otherNode in graph.nodes():
            if not (otherNode == node):
                if graph.nodes[node]['cancelLevel'] < graph.nodes[otherNode]['cancelLevel']:
                    graph.add_edge(node, otherNode, weight=0)
                link = isLink(graph.nodes[node],graph.nodes[otherNode])
                if link and graph.nodes[node]['cancelLevel'] != 0:
                    graph.add_edge(node, otherNode, weight=int(link))
    random_node = choice(graph.nodes())
    #print(random_node)
    return graph
