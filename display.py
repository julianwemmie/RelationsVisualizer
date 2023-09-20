from abc import ABC, abstractmethod
from typing import Dict, List, Set
import turtle
import dearpygui.dearpygui as dpg

from graph import Graphable
from node import Node

class IDisplay(ABC):
    @abstractmethod
    def drawGraph(self, graph: Graphable): ...

class TurtleDisplay(IDisplay):
    def drawGraph(self, graph: Graphable):
        nodes = graph.nodes
        relations = graph.relations
        self._init_turtle()
        self._connectNodes(nodes, relations)
        self._drawNodes(nodes)
        self._drawNodeNames(nodes)
        turtle.update()
        turtle.done()

    def _init_turtle(self):
        window = turtle.Screen()
        window.title('Relation Visualizer')
        window.tracer(0)
        
        turt = turtle.Turtle()
        turt.ht()

        turtle.TurtleScreen._RUNNING = True

        self.turt = turt
        self.window = window
    
    def _drawNodes(self, nodes):
        for node in nodes.values():
            x, y = node.xPos, node.yPos
    
            self.turt.pensize(1)
            self.turt.pencolor('black')
            self.turt.ht()
            self.turt.up()

            self.turt.setpos(x,y)
            self.turt.dot(25, "white")

            self.turt.setpos(x,y - 12.5)
            self.turt.down()
            self.turt.circle(12.5)

    def _connectNodes(self, nodes, relations):
        for relation in relations:
            nodeName1, nodeName2 = relation
            node1 = nodes[nodeName1]
            node2 = nodes[nodeName2]

            self._drawLine((node1.xPos, node1.yPos), (node2.xPos, node2.yPos))

    def _drawLine(self, point1, point2):
        self.turt.pensize(1)
        oldColor = self.turt.pencolor()
        self.turt.pencolor('black')
        x1 = point1[0]
        y1 = point1[1]  
        x2 = point2[0]
        y2 = point2[1]    
        
        self.turt.ht()
        self.turt.up()    
        self.turt.setpos(x1,y1)
        self.turt.down()
        self.turt.setpos(x2,y2)
        
        self.turt.pencolor(oldColor)

    def _drawNodeNames(self, nodes, font_color = "black"):
        for node in nodes.values():
            x,y = node.xPos, node.yPos
            self.turt.pencolor(font_color)
            self.turt.ht()
            self.turt.up()   
            self.turt.setpos(x + 1, y - 8)
            self.turt.write(f'{node.name}', align='center', 
                            font=('Arial', 10, 'bold'))

BG_COLOR = (37, 37, 38, 255)
class DearPyGui(IDisplay):
    def __init__(self, width: int = 1000, height: int = 600):
        self.width = width
        self.height = height

    def _init(self):
        dpg.create_context()

        with dpg.font_registry():
            self.default_font = dpg.add_font("TEMPO.TTF", 30, default_font=True)

    def drawGraph(self, graph: Graphable):
        self._init()

        nodes = graph.nodes
        relations = graph.relations

        with dpg.window(label="RelationViz", tag="MainWindow"):
            dpg.set_global_font_scale(0.5)
            with dpg.drawlist(width=self.width, height=self.height-100):
                self._centerNodes(nodes)
                self._connectNodes(nodes, relations)
                self._drawNodes(nodes)
                self._drawNodeNames(nodes)

        self._run()

    def _centerNodes(self, nodes: Dict[str, Node]):
        for node in nodes.values():
            node.xPos += self.width / 2
            node.yPos += self.height / 2

    def _drawNodes(self, nodes: Dict[str, Node]):
        for node in nodes.values():
            x, y = node.xPos, node.yPos
            dpg.draw_circle((x, y), 12.5, color=(255, 255, 255, 255), fill=BG_COLOR, thickness=1)

    def _connectNodes(self, nodes: Dict[str, Node], relations: List[Set[str]]):
        for relation in relations:
            nodeName1, nodeName2 = relation
            node1 = nodes[nodeName1]
            node2 = nodes[nodeName2]

            dpg.draw_line((node1.xPos, node1.yPos), (node2.xPos, node2.yPos))

    def _drawNodeNames(self, nodes: Dict[str, Node]):
        dpg.bind_font(self.default_font)
        for node in nodes.values():
            x, y = node.xPos, node.yPos
            # text offset
            x -= 5
            y -= 7.5
            dpg.draw_text((x, y), node.name, color=(255, 255, 255, 255), size=20)

    def _run(self):
        dpg.create_viewport(title='RelationViz', width=self.width, height=self.height)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("MainWindow", True)
        dpg.start_dearpygui()
        dpg.destroy_context()