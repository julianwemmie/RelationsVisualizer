
import turtle
import fdg
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
    turt.dot(20, "white")
    turt.setpos(x,y - 10)
    turt.down()
    turt.circle(10)
    
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
    
def printNames(turt, nodes, font_color = "black"):
    for node in nodes:
        x,y = node.xy
        turt.pencolor(font_color)
        turt.ht()
        turt.up()   
        turt.setpos(x + 1, y - 8)
        turt.write(f'{node.name}', align='center', 
                         font=('Arial', 10, 'bold')) 
                         
def drawGraph(nodes):
    turt, window = init_turtle()

    # turtle screen quits after turtle.done, so need to reinitialize
    turtle.TurtleScreen._RUNNING = True

    fdg.apply_fdg(nodes, fdg_iterations)
    connectNodes(turt, nodes, line_color)
    drawNodes(turt, nodes, node_color)
    printNames(turt, nodes, font_color)
    

    window.update()
    turtle.done() 