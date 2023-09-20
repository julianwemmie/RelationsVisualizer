from abc import ABC, abstractmethod
import json
from os import path
from typing import Dict, List, Set

from forceDirectedGraph import NodeBalancer
from node import Node

class Graphable(ABC):
    @abstractmethod
    def addNode(self, nodeName: str) -> None: ...

    @abstractmethod
    def removeNode(self, nodeName: str) -> None: ...

    @abstractmethod
    def addNodes(self, nodeNames: List[str]) -> None: ...

    @abstractmethod
    def removeNodes(self, nodeNames: List[str]) -> None: ...

    @abstractmethod
    def getNodeNames(self) -> List[str]: ...

    @abstractmethod
    def addRelation(self, nodeName1: str, nodeName2: str) -> None: ...

    @abstractmethod
    def removeRelation(self, nodeName1: str, nodeName2: str) -> None: ...

    @abstractmethod
    def nodeExists(self, nodeName: str) -> bool: ...

    @abstractmethod
    def nodesExist(self, nodeNames: List[str]) -> bool: ...

    @abstractmethod
    def relationExists(self, nodeName1: str, nodeName2: str) -> bool: ...

class GraphModel:
    def __init__(self, name: str, nodes: List[str], relations: List[List[str]]) -> None:
        self.name = name
        self.nodes = nodes
        self.relations = relations

class Graph(Graphable):
    def __init__(self, name = None):
        self.name = name
        self.nodes: Dict[str, Node] = {}
        self.relations: List[Set[str, str]] = []
        self.relationsMap: Dict[str, List[str]]= {}

    @classmethod
    def from_file(cls, fileName: str):
        if not path.exists(fileName):
            raise FileNotFoundError('File does not exist.')

        # deserialize JSON to GraphModel
        try:
            with open(fileName, 'r') as f:
                graphModel = json.load(f, object_hook=lambda d: GraphModel(**d))
        except:
            raise TypeError('Invalid JSON file.')
        
        graph = Graph.from_graphModel(graphModel)
        return graph
        
    @classmethod
    def from_graphModel(cls, graphModel: GraphModel):
        graph = Graph(graphModel.name)
        graph.addNodes(graphModel.nodes)
        for relation in graphModel.relations:
            graph.addRelation(relation[0], relation[1])
        return graph
    
    def to_graphModel(self):
        relations = [list(relation) for relation in self.relations] # convert sets to lists
        return GraphModel(self.name, self.getNodeNames(), relations)
    
    def to_file(self, fileName: str):
        # serialize GraphModel to JSON
        data = json.dumps(self.to_graphModel(), default=lambda o: o.__dict__, indent=2)
        
        with open(fileName, 'w') as f:
            f.write(data)

    def addNode(self, nodeName: str):
        node = Node(nodeName)
        if node.name not in self.nodes:
            self.nodes[node.name] = node
            self.relationsMap[node.name] = []
            return
        raise NameError("Node already exists")

    def removeNode(self, nodeName: str):        
        if nodeName not in self.nodes:
            raise NameError("Node does not exist.")
        
        relations = self.relationsMap[nodeName][:]
        for relation in relations:
            self.removeRelation(nodeName, relation)
        
        del self.relationsMap[nodeName]
        del self.nodes[nodeName]

    def addNodes(self, nodeNames: List[str]):
        for nodeName in nodeNames:
            self.addNode(nodeName)

    def removeNodes(self, nodeNames: List[str]):
        for nodeName in nodeNames:
            self.removeNode(nodeName)

    def addRelation(self, nodeName1, nodeName2):
        if nodeName1 not in self.nodes or nodeName2 not in self.nodes:
            raise NameError('One or more nodes does not exist.')
        
        if set((nodeName1, nodeName2)) in self.relations:
            raise NameError('Relation already exists.')
        
        self.relations.append(set((nodeName1, nodeName2)))
        self.relationsMap[nodeName1].append(nodeName2)
        self.relationsMap[nodeName2].append(nodeName1)

    def removeRelation(self, nodeName1, nodeName2):
        relation = set((nodeName1, nodeName2))
        if relation not in self.relations:
            raise NameError('One or more nodes/relation does not exist.')
        
        i = self.relations.index(relation)
        self.relations.pop(i)

        i = self.relationsMap[nodeName1].index(nodeName2)
        self.relationsMap[nodeName1].pop(i)
        
        i = self.relationsMap[nodeName2].index(nodeName1)
        self.relationsMap[nodeName2].pop(i)

    def getNodeNames(self):
        return list(self.nodes.keys())
    
    def balanceNodes(self, nodeBalancer: NodeBalancer):
        self.nodes = nodeBalancer.balance(self.nodes, self.relations, self.relationsMap)

    def nodeExists(self, nodeName):
        return nodeName in self.nodes
    
    def nodesExist(self, nodeNames):
        for nodeName in nodeNames:
            if not self.nodeExists(nodeName):
                return False
        return True
    
    def relationExists(self, nodeName1, nodeName2):
        return set((nodeName1, nodeName2)) in self.relations