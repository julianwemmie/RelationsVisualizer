
import numpy as np

class Node():

    node_names = [] 
    edge_weights = []

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
        for relation in cls.edge_weights:
            if relation[0] == set([node1, node2]):
                relation[1] = weight
                return
        if not node1.related(node2):
            raise IndexError("Relation does not exist")
        cls.edge_weights.append([set([node1, node2]), weight])

    @classmethod
    def removeRelation(cls, node1, node2):
        relation_index = 0
        for relation in cls.edge_weights:
            if relation[0] == set([node1, node2]):
                relation_index = cls.edge_weights.index(relation)
        del cls.edge_weights[relation_index]