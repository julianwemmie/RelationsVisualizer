
import os, turtle
from display import init_turtle, connectNodes, drawNodes, printName
import node as n
from force_directed_graph import do_FDG, randomPos

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def mainMenu():
    while True:
        clearScreen()
        print('''\
Relations Visualizer
    1. create graph
    2. edit/view current nodes
    3. edit/view current relations''')
    
        selection = input(' > ')
        if selection == '1':
            drawGraph()
        elif selection == '2':
            editNodes()
        elif selection == '3':
            editRelations()
        elif selection == 'exit':
            return
        else:
            print('Invalid Input\n')

def drawGraph():
    turt, window = init_turtle()
    turtle.TurtleScreen._RUNNING = True
    randomPos(nodes, 100)

    t = 0
    for i in range(stop):
        do_FDG(nodes, t)
        t += 1
        
    connectNodes(turt, nodes, 'red')
    drawNodes(turt, nodes, 'black')
    printName(turt, nodes)
    window.update()
    turtle.done()

def editNodes():
    while True:
        print('''\2
---------------------------
Edit/View Nodes:
    -v | view current nodes
    -a | add node(s)
            '-a a,b,c' --> adds nodes a, b, and c
    -r | remove node(s)
            '-r a,b,c' --> removes nodes a, b, and c (if exist)
    -e | exit
    ''')
    
        entry = input(' > ')
        selection = entry[:2]
        
        if selection == '-v':
            viewNodes()
        elif selection == '-a':
            addNodes(entry[3:])
        elif selection == '-r':
            removeNodes(entry[3:])
        elif selection == '-e':
            return
        else:
            print('Invalid entry\n')
            
def viewNodes():
    if not len(nodes):
        print('Currently (0) nodes.\n')
    else:
        print(f'Currently ({len(nodes)}) nodes:')
        print(f'    -{", ".join(sorted([node.name for node in nodes]))}')
        print()

def addNodes(toAdd):
    global nodes
    if not len(toAdd):
        print('Specify nodes to add. Ex: "-a a,b,c"\n')
        return

    addedNodes = []
    for node in toAdd.split(','):
        if node == '':
            continue
        if node in [node.name for node in nodes]:
            print(f'Node already exists: {node}')
            continue
        nodes.append(n.Node(node))  
        addedNodes.append(node)
        
    print(f'Successfully added node(s): {", ".join(addedNodes)} \n')

def removeNodes(toRemove):
    global nodes
    if not len(toRemove):
        print('Specify nodes to remove. Ex: "-r a,b,c"\n')
        return
    
    removed = []
    for node in toRemove.split(','):
        for existingNode in nodes:
            if node == existingNode.name:
                nodes.remove(existingNode)
                removed.append(existingNode)
                
    for node in removed:
        for edge in node.edges:
            edge.edges.remove(node)
            
    print(f'Successfully removed node(s): {", ".join([node.name for node in removed])}\n')

def editRelations():
    while True:
        print('''\
---------------------------
Edit/View Relations:
    -v | view current relations
    -a | add relation
            '-a a,b' --> adds relation between a and b
    -r | remove relation
            '-r a,b' --> removes relation bewteen a and b (if exists)
    -e | exit
    ''')
        
        entry = input(' > ')
        selection = entry[:2]
        
        if selection == '-v':
            viewRelations()
        elif selection == '-a':
            addRelation(entry[3:])
        elif selection == '-r':
            removeRelation(entry[3:])
        elif selection == '-e':
            return
        else:
            print('Invalid entry\n')
            
def viewRelations():
    if not len(nodes):
        print('No nodes defined.\n')
        return
    else:
        print('Node: [Relations]')
        for node in sorted(nodes):
            print(node)

def addRelation(toAdd):
    if len(toAdd) < 3:
            print('Specify relations to add. Ex: "-a a,b"\n')
            return    
    toAdd = toAdd.split(',')
    for node in toAdd:
        if node not in [node.name for node in nodes]:
            print('One or more nodes does not exist. \n')
            return
    for node in nodes:
        if node.name == toAdd[0]:
            toAdd[0] = node
        if node.name == toAdd[1]:
            toAdd[1] = node
    toAdd[0].connect(toAdd[1])
    print(f'Successfully added relation: {toAdd[0].name}, {toAdd[1].name}\n')

def removeRelation(toRemove):
    if len(toRemove) < 3:
            print('Specify relations to remove. Ex: "-a a,b"\n')
            return    
        
    toRemove = toRemove.split(',')

    for node in toRemove:
        if node not in [node.name for node in nodes]:
            print('One or more nodes does not exist. \n')
            return   
        
    for node in nodes:
        if node.name == toRemove[0]:
            toRemove[0] = node
        if node.name == toRemove[1]:
            toRemove[1] = node
    toRemove[0].disconnect(toRemove[1])
    print(f'Successfully removed relation: {toRemove[0].name}, {toRemove[1].name}\n')
    
def pathAlgorthims():
    pass

def main():
    global c1, c2, c3, c4, c5, nodes, stop
    c1, c2, c3, c4, c5 = 80, 100, 1000, 0.05, 1000
    nodes = []
    stop = 100   
    mainMenu()

if __name__ == '__main__':
    main()