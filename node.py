
from platform import node
import numpy as np

class Node():

    node_names = [] 
    edge_weights = {}

    def __init__(self, name):
        self.name = name
        self.edges = set()
        self.xy = np.array([0,0], dtype = np.float64)
        self.node_names.append(name)
        
    def __str__(self):
        return str(f'{self.name}: {sorted([edge.name for edge in self.edges])}')
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.edges)
    
    def __lt__(self, otherNode):
        if len(self) < len(otherNode):
            return True
        return False
    
    def __le__(self, otherNode):
        if len(self) <= len(otherNode):
            return True
        return False    
    
    def __gt__(self, otherNode):
        if len(otherNode) < len(self):
            return True
        return False 
    
    def __ge__(self, otherNode):
        if len(otherNode) <= len(self):
            return True
        return False    
    
    def connect(self, otherNodes):
        if isinstance(otherNodes, list):
            for otherNode in otherNodes:
                self.edges.add(otherNode)
                otherNode.edges.add(self)
        else:
            self.edges.add(otherNodes)
            otherNodes.edges.add(self)            
        
    def related(self, otherNode):
        if otherNode in self.edges:
            return True
        return False
    
    def disconnect(self, otherNode):
        if isinstance(otherNode, Node):
            self.edges.remove(otherNode)
            otherNode.edges.remove(self)
        else:
            raise TypeError('Can only disconnect node class')

    @classmethod
    def removeNode(cls, node):
        cls.node_names.remove(node.name)

    @classmethod
    def addWeight(cls, node1, node2, weight):
        # sort relations to avoid duplicates
        relation = sorted([node1.name, node2.name])
        relation = tuple(relation)

        cls.edge_weights[relation] = weight

    @classmethod
    def removeRelation(cls, node1, node2):
        relation = sorted([node1.name, node2.name])
        relation = tuple(relation)

        del cls.edge_weights[relation]