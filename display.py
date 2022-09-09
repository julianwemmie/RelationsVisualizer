
import turtle
import fdg
from config import fdg_iterations as iter_fdg
from config import node_color, line_color

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

def drawNode(turt, xy, color):
    x, y = xy
    
    turt.ht()
    turt.up()
    turt.setpos(x,y)
    turt.dot(7.5, color)
    
def connectNodes(turt, nodes, color = 'black'):
    for node in nodes:
        for otherNode in nodes:
            if node.related(otherNode):
                drawLine(turt, node.xy, otherNode.xy, color)
    
def drawLine(turt, point1, point2, color = 'black'):
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
    
def printName(turt, nodes):
    for node in nodes:
        turt.ht()
        turt.up()   
        turt.setpos(node.xy[0], node.xy[1]+10)
        turt.write(f'{node.name}', align='center', 
                         font=('Arial', 10, 'bold')) 
                         
def drawGraph(nodes):
    turt, window = init_turtle()

    # turtle screen quits after turtle.done, so need to reinitialize
    turtle.TurtleScreen._RUNNING = True

    fdg.apply_fdg(nodes, iter_fdg)
    connectNodes(turt, nodes, line_color)
    drawNodes(turt, nodes, node_color)
    printName(turt, nodes)

    window.update()
    turtle.done() 