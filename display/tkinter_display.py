from typing import Dict, List, Set

from .interface import IDisplay
from graph import Graphable
from node import Node

class TkinterDisplay(IDisplay):
    def __init__(self, width: int = 800, height: int = 600) -> None:
        self.width = width
        self.height = height

    def drawGraph(self, graph: Graphable) -> None:
        import tkinter as tk

        nodes = graph.nodes
        relations = graph.relations

        self._centerNodes(nodes)

        root = tk.Tk()
        root.title("RelationViz")
        canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white")
        canvas.pack(fill="both", expand=True)

        self._connectNodes(canvas, nodes, relations)
        self._drawNodes(canvas, nodes)
        self._drawNodeNames(canvas, nodes)

        root.mainloop()

    def _centerNodes(self, nodes: Dict[str, Node]) -> None:
        for node in nodes.values():
            node.xPos += self.width / 2
            node.yPos += self.height / 2

    def _drawNodes(self, canvas, nodes: Dict[str, Node]) -> None:
        for node in nodes.values():
            x, y = node.xPos, node.yPos
            r = 12.5
            canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", outline="black")

    def _connectNodes(self, canvas, nodes: Dict[str, Node], relations: List[Set[str]]) -> None:
        for relation in relations:
            nodeName1, nodeName2 = relation
            node1 = nodes[nodeName1]
            node2 = nodes[nodeName2]
            canvas.create_line(node1.xPos, node1.yPos, node2.xPos, node2.yPos, fill="black")

    def _drawNodeNames(self, canvas, nodes: Dict[str, Node]) -> None:
        for node in nodes.values():
            x, y = node.xPos, node.yPos
            canvas.create_text(x, y, text=node.name, fill="black", font=("Arial", 10, "bold"))
