
import math
import numpy as np
from random import randint
from config import fdg_weights

c1 = fdg_weights['c1']
c2 = fdg_weights['c2']
c3 = fdg_weights['c3']
c4 = fdg_weights['c4']
c5 = fdg_weights['c5']

def spring_force(node, otherNode):
    dist = math.dist(node, otherNode)
    F = c1 * math.log10(dist/c2)
    return getForceVec(node, otherNode, F)

def repulsive_force(node, otherNode):
    dist = math.dist(node, otherNode)
    F = -1 * c3 / (dist**2)
    return getForceVec(node, otherNode, F)

def getForceVec(start, end, force):
    node = end - start
    angle = math.atan(node[1] / node[0])
    forceVec = (force * math.cos(angle)), (force * math.sin(angle))
    forceVec = np.array(forceVec)
    if node[0] < 0 and node[1] >= 0:
        forceVec *= -1
    if node[1] < 0 and node[0] < 0:
        forceVec *= -1
    return forceVec   

def randomPos(nodes, dim):
    for node in nodes:
        a = randint(-dim, dim)
        b = randint(-dim, dim)
        node.xy = np.array([a,b], dtype = np.float64)

def limit(t):
    if t == 0:
        t = 1
    return c5/(t)

def do_FDG(nodes, t = 0):   
    F = {}
    
    for node in nodes:
        F[node.name] = np.array([0,0], dtype = np.float64)
        for otherNode in nodes:
            if node == otherNode:
                continue
            if node.related(otherNode):
                F[node.name] += spring_force(node.xy, otherNode.xy)
            elif not len(node.edges):
                F[node.name] += c4 * repulsive_force(node.xy, otherNode.xy)
            else:
                F[node.name] += limit(t) * repulsive_force(node.xy, otherNode.xy)
    for node in nodes:
        node.xy += F[node.name]
        
def apply_fdg(nodes: list, iterations: int):
    randomPos(nodes, 100)

    for i in range(iterations):
        do_FDG(nodes, i)