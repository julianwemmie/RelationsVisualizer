import turtle
import fdg
import path_algorithms
from node import Node
from config import display_config

fdg_iterations = display_config["fdg_iterations"]
line_color = display_config["line_color"]
node_color = display_config["node_color"]
font_color = display_config["font_color"]

def init_turtle():
    window = turtle.Screen()
    window.title('Relation Visualizer')
    window.tracer(0)
    
    turt = turtle.Turtle()
    turt.ht()  
    return turt, window
    
def drawNodes(turt, nodes, color):
    for node in nodes:
        drawNode(turt, node.xy, color)

def drawNode(turt, xy, color = "black"):
    x, y = xy
    
    turt.pensize(1)
    turt.pencolor(color)
    turt.ht()
    turt.up()

    turt.setpos(x,y)
    turt.dot(25, "white")

    turt.setpos(x,y - 12.5)
    turt.down()
    turt.circle(12.5)
    
def connectNodes(turt, nodes, color = 'black'):
    for node in nodes:
        for otherNode in nodes:
            if node.related(otherNode):
                drawLine(turt, node.xy, otherNode.xy, color)
    
def drawLine(turt, point1, point2, color = 'black'):
    turt.pensize(1)
    oldColor = turt.pencolor()
    turt.pencolor(color)
    x1 = point1[0]
    y1 = point1[1]  
    x2 = point2[0]
    y2 = point2[1]    
    
    turt.ht()
    turt.up()    
    turt.setpos(x1,y1)
    turt.down()
    turt.setpos(x2,y2)
    
    turt.pencolor(oldColor)
    
def printNames(turt, nodes, font_color = "black"):
    for node in nodes:
        x,y = node.xy
        turt.pencolor(font_color)
        turt.ht()
        turt.up()   
        turt.setpos(x + 1, y - 8)
        turt.write(f'{node.name}', align='center', 
                         font=('Arial', 10, 'bold'))

def printWeights(turt, nodes, font_color = 'black'):
    for relation in Node.edge_weights.items():
        node1, node2 = relation[0]
        node1 = nodes.get(node1)
        node2 = nodes.get(node2)

        x1, y1 = node1.xy
        x2, y2 = node2.xy

        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2


        turt.pencolor(font_color)
        turt.ht()
        turt.up()

        turt.setpos((mid_x, mid_y))
        turt.dot(20, 'lightgrey')

        turt.setpos((mid_x + 1, mid_y - 8))
        turt.write(f'{relation[1]}', align='center', 
                         font=('Arial', 10, 'bold'))

def printDijkstra(turt, nodes, endpoints):
    start, stop = endpoints

    start = nodes[start]
    stop = nodes[stop]

    shortest_path, cost = path_algorithms.dijkstra(nodes, start, stop)

    # get shortest path xy coordinates
    shortest_path_xy = []
    for node in shortest_path:
        node = nodes[node]
        shortest_path_xy.append(node.xy)


    # draw shortest path
    turt.ht()
    turt.pensize(5)
    turt.color('red')
    turt.up()
    turt.setpos(shortest_path_xy[0])
    for xy in shortest_path_xy:
        turt.down()
        turt.setpos(xy)
    turt.up()

                         
def drawGraph(nodes, weights = False, algo = None, *args):
    turt, window = init_turtle()

    # turtle screen quits after turtle.done, so need to reinitialize
    turtle.TurtleScreen._RUNNING = True

    node_objects = nodes.values()

    fdg.apply_fdg(node_objects, fdg_iterations)
    connectNodes(turt, node_objects, line_color)
    if algo == 'dijkstra':
        printDijkstra(turt, nodes, args[0])
    drawNodes(turt, node_objects, node_color)
    printNames(turt, node_objects, font_color)
    if weights == True:
        printWeights(turt, nodes, font_color)
    
    window.update()
    turtle.done() 