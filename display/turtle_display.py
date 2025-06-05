from typing import Dict
import turtle

from .interface import IDisplay
from graph import Graphable
from node import Node

class TurtleDisplay(IDisplay):
    def drawGraph(self, graph: Graphable) -> None:
        nodes = graph.nodes
        relations = graph.relations
        self._init_turtle()
        self._connectNodes(nodes, relations)
        self._drawNodes(nodes)
        self._drawNodeNames(nodes)
        turtle.update()
        turtle.done()

    def _init_turtle(self) -> None:
        window = turtle.Screen()
        window.title('Relation Visualizer')
        window.tracer(0)

        turt = turtle.Turtle()
        turt.ht()

        turtle.TurtleScreen._RUNNING = True

        self.turt = turt
        self.window = window

    def _drawNodes(self, nodes: Dict[str, Node]) -> None:
        for node in nodes.values():
            x, y = node.xPos, node.yPos

            self.turt.pensize(1)
            self.turt.pencolor('black')
            self.turt.ht()
            self.turt.up()

            self.turt.setpos(x, y)
            self.turt.dot(25, "white")

            self.turt.setpos(x, y - 12.5)
            self.turt.down()
            self.turt.circle(12.5)

    def _connectNodes(self, nodes: Dict[str, Node], relations) -> None:
        for relation in relations:
            nodeName1, nodeName2 = relation
            node1 = nodes[nodeName1]
            node2 = nodes[nodeName2]

            self._drawLine((node1.xPos, node1.yPos), (node2.xPos, node2.yPos))

    def _drawLine(self, point1, point2) -> None:
        self.turt.pensize(1)
        oldColor = self.turt.pencolor()
        self.turt.pencolor('black')
        x1 = point1[0]
        y1 = point1[1]
        x2 = point2[0]
        y2 = point2[1]

        self.turt.ht()
        self.turt.up()
        self.turt.setpos(x1, y1)
        self.turt.down()
        self.turt.setpos(x2, y2)

        self.turt.pencolor(oldColor)

    def _drawNodeNames(self, nodes: Dict[str, Node], font_color: str = "black") -> None:
        for node in nodes.values():
            x, y = node.xPos, node.yPos
            self.turt.pencolor(font_color)
            self.turt.ht()
            self.turt.up()
            self.turt.setpos(x + 1, y - 8)
            self.turt.write(f'{node.name}', align='center', font=('Arial', 10, 'bold'))
