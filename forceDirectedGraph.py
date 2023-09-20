from typing import List, Set, Dict
from abc import ABC, abstractmethod
import math
import random

from node import Node

c1 = 80
c2 = 100
c3 = 1000
c4 = 0.05
c5 = 1000

class NodeBalancer(ABC):
    @abstractmethod
    def balance(self, nodes: List[Node], relations: List[Set[str]], relationsMap: Dict[str, List[str]]) -> List[Node]: ...

class ForceDirectedGraph(NodeBalancer):
    def balance(self, nodes: List[Node], relations: List[Set[str]], relationsMap: Dict[str, List[str]]) -> List[Node]:
        self.nodes = nodes
        self.relations = relations
        self.relationsMap = relationsMap
        self._applyFDG()
        return self.nodes
    
    def _springForce(self, node, otherNode):
        dist = math.dist(node, otherNode)
        F = c1 * math.log10(dist/c2)
        return self._getForceVec(node, otherNode, F)
    
    def _repulsiveForce(self, node, otherNode):
        dist = math.dist(node, otherNode)
        F = -1 * c3 / (dist**2)
        return self._getForceVec(node, otherNode, F)
    
    def _getForceVec(self, start, end, force):
        dx, dy = end[0] - start[0], end[1] - start[1]

        # check for divison by zero
        if dx == 0:
            dx += 0.01

        angle = math.atan(dy / dx)
        forceVec = [force * math.cos(angle), force * math.sin(angle)]
        if dx < 0 and dy >= 0:
            forceVec[0] *= -1
            forceVec[1] *= -1
        if dy < 0 and dx < 0:
            forceVec[0] *= -1
            forceVec[1] *= -1
        return forceVec
    
    def _setNodesRandomPos(self, dim):
        for node in self.nodes.values():
            node.xPos = random.randint(-dim, dim)
            node.yPos = random.randint(-dim, dim)

    def _limit(self, t):
        if t == 0:
            t = 1
        return c5/(t)
    
    def _doFDG(self, t = 0):   
        F = {}
        for nodeName, node in self.nodes.items():
            F[nodeName] = [0,0]
            for otherNodeName, otherNode in self.nodes.items():
                if node == otherNode:
                    continue
                x1, y1 = node.xPos, node.yPos
                x2, y2 = otherNode.xPos, otherNode.yPos
                if set((nodeName, otherNodeName)) in self.relations:
                    dx, dy = self._springForce((x1, y1), (x2, y2))
                elif len(self.relationsMap[nodeName]) == 0:
                    dx, dy = self._repulsiveForce((x1, y1), (x2, y2))
                    dx, dy = c4 * dx, c4 * dy
                else:
                    dx, dy = self._repulsiveForce((x1, y1), (x2, y2))
                    limit = self._limit(t)
                    dx, dy = limit * dx, limit * dy
                F[nodeName][0] += dx
                F[nodeName][1] += dy
        for nodeName, node in self.nodes.items():
            node.xPos += F[nodeName][0]
            node.yPos += F[nodeName][1]

    def _applyFDG(self, iterations: int = 100):
        self._setNodesRandomPos(100)

        for i in range(iterations):
            self._doFDG(i)