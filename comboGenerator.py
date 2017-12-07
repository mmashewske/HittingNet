#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  comboGenerator.py
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
def comboDamage( combo, graph ):
    '''Returns the damage a combo should do
    '''
    scaling = 1
    damage = int(graph.nodes[ combo[0] ]['damage'] )
    if( graph.nodes[ combo[0] ]['cancelLevel'] == 0):
        scaling = .5
    for move in combo[1:]:
        if( int(graph.nodes[ move[1] ]['cancelLevel'] != 5 ) ):
            if( moveDamage(move,graph) >= 1000):
                damage += min(scaling,.275)*moveDamage(move,graph)
            else:
                damage += min(scaling,.2)*moveDamage(move,graph)
        else:
            if( int(graph.nodes[ move[1] ]['meter'] == -3000 ) ):
                damage += .45*moveDamage(move,graph)
            elif( int(graph.nodes[ move[1] ]['meter'] == -5000 ) ):
                damage += .55*moveDamage(move,graph)
        
    return damage
    
def moveDamage( move, graph ):
    '''Returns a move's damage.
    '''
    return int( graph.nodes[move[1]]['damage'] )

def comboMeter( combo, graph ):
    '''Returns how much meter a combo should give you.
    '''
    meter = int(graph.nodes[ combo[0] ]['meter'] )
    for move in combo[1:]:
        meter += moveMeter(move,graph)
    return meter
    
def moveMeter( move, graph ):
    '''Returns how much meter a move should give you.
    '''
    return int( graph.nodes[move[1]]['meter'] )
    
def comboMetric( combo, graph ):
    '''Returns a simple metric to evaluate a combo.
    '''
    if len(combo) == 0:
        return 0
    potentialDamage = comboDamage(combo, graph)
    potentialMeter = comboMeter(combo, graph)
        
    return comboUnbreakable(combo)*len(combo)*(potentialDamage+potentialMeter)/2
    
def comboUnbreakable( combo):
    '''Returns true if the infinite detector does not go off from the combo.
    '''
    chainStarts = []
    knockdowns = 0
    sound = 0
    for i in range(len(combo)) :
        if(i == 0):
            chainStarts.append(combo[i])
        else:
            if( combo[i][2] > 0 ):
                if( (combo[i][1] in chainStarts) and (len(chainStarts) >= 3) ):
                    return False
                    
                    pass
                chainStarts.append(combo[i][1])
            if(combo[i][2] == 2):
                if(knockdowns == 1):
                    return False
                else:
                    knockdowns+=1
            elif(combo[i][2] == 3):
                if(sound == 1):
                    return False
                    pass
                else:
                    sound+=1
    return True

def soundStunEffect( soundUsed, move ):
    '''Returns the sound stun effect of a move.
    Currently unused
    '''
    if soundUsed:
        return move['onhit'].replace('"','').split()[2]
    else:
        return move['onhit'].replace('"','').split()[1]
        

'''def generateComboDefunct( network, minMeter, maxLength, seed, window ):
    combo = [seed]
    knockdown = 0
    while len(combo) < maxLength:
        if len(combo) > 1:
            clique = (x for x in network[0].edges(data='weight') if x[0] == combo[len(combo)-1][1] and x[2] < 2)
        else:
            clique = (x for x in network[0].edges(data='weight') if x[0] == combo[0] and x[2] < 2)
        print(combo)
        for q in clique:
            #print( q )
            if (q[0] == combo[len(combo)-1][0]) and len(combo) > 1:
                
                potentialDamage = comboDamage(combo, network[1]) + moveDamage( q[1], network[1]) - moveDamage( combo[len(combo)-1][1], network[1])
                currentDamage = comboDamage( combo, network[1])
                potentialMeter = comboMeter(combo, network[1]) + moveMeter( q[1], network[1]) - moveMeter( combo[len(combo)-1][1], network[1])
                currentMeter = comboMeter( combo, network[1])
                currentMetric = math.sqrt( pow(currentDamage,2) + pow(currentMeter,2) )
                potentialMetric = math.sqrt( pow(potentialDamage,2) + pow(currentMeter,2) )
                
                if (potentialMeter > currentMeter):
                    combo[len(combo)-1] = q
                    #print("thing")
            else:
                combo.append(q)
                #print("thing2")
    return combo
'''


def generateCombo(network, minMeter, maxLength, seed, window):
    combo = [seed]
    clique = list(x for x in network.edges(data='weight') if x[0] == combo[0])
    random.shuffle(clique)
    for q in clique[0: (math.floor(window*len(clique))-1 if window > 0 else 1)]:
        potential = generateComboHelper(network, minMeter, maxLength, [seed,q], window)
        if (comboMetric(potential, network) > comboMetric( combo, network)) and (len(combo)<maxLength) and (comboMeter(potential,network) > minMeter) and ( len(combo) < maxLength):
            combo = potential
    return combo

def generateComboHelper( network, minMeter, maxLength, inputCombo, window ):
    combo = inputCombo[:]
    if(len(combo)==maxLength):
        return combo
    clique = list(x for x in network.edges(data='weight') if x[0] == combo[len(combo)-1][1])
    random.shuffle(clique)
    for q in clique[0: (math.floor(window*len(clique))-1 if window > 0 else 1)]:
        potentialInput = inputCombo[:]
        potentialInput.append(q)
        potential = generateComboHelper(network, minMeter, maxLength, potentialInput, window)
        if (comboMetric(potential, network) > comboMetric( combo, network)) and (comboMeter(potential,network) > minMeter) and (len(combo) < maxLength) and comboUnbreakable(combo):
            combo = potential
    return combo
    

def printCombo( combo, graph ):
    out = graph.nodes[combo[0]]['command']
    for move in combo[1:]:
        if move[2] == 0:
            if graphMake.commandType(graph.nodes[move[0]]['command']) > 2:
                out += (" xx "+graph.nodes[move[1]]['command'])
            else:
                out += (" > "+graph.nodes[move[1]]['command'])
        else:
            out += (", "+graph.nodes[move[1]]['command'])
    print(out)

def main(args):
    graph = graphMake.makeGraph()
    seed = random.randint(0,len(graph)-1)
    combo = generateCombo( graph, -500, 7, seed, 1)
    print(combo)
    printCombo(combo, graph)
    return 0

if __name__ == '__main__':
    import sys
    import networkx as nx
    import graphMake
    import random
    import math
    sys.exit(main(sys.argv))
