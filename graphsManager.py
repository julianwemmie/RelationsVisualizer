from typing import List

from graph import Graph

class GraphsManager:
    def __init__(self, graphs: List[Graph] = None) -> None:
        self.graphs = graphs if graphs else []
        self._currentGraph = graphs[0] if graphs else None

    def createGraph(self, name: str):
        for graph in self.graphs:
            if graph.name == name:
                raise NameError('Graph already exists')
        self.graphs.append(Graph(name))

    def deleteGraph(self, name: str):
        if len(self.graphs) == 1:
            raise NameError('Cannot delete last graph')
        for graph in self.graphs:
            if graph.name == name:
                self.graphs.remove(graph)
                self._currentGraph = self.graphs[-1]
                return
        raise NameError('Graph does not exist')
            
    @property
    def currentGraph(self):
        return self._currentGraph

    @currentGraph.setter
    def currentGraph(self, name: str):
        for graph in self.graphs:
            if graph.name == name:
                self._currentGraph = graph
                return
        raise NameError('Graph does not exist')
    
    def renameGraph(self, oldName: str, newName: str):
        for graph in self.graphs:
            if graph.name == oldName:
                graph.name = newName
                return
        raise NameError('Graph does not exist')
    
    def importGraph(self, fileName: str):
        if not fileName.endswith('.json'):
            fileName += '.json'

        graph = Graph.from_file(fileName)
        for g in self.graphs:
            if g.name == graph.name:
                raise NameError('Graph already exists')
        self.graphs.append(graph)

    def exportGraph(self, fileName: str):
        if not fileName.endswith('.json'):
            fileName += '.json'
        self.currentGraph.to_file(fileName)