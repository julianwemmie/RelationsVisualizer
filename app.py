
import os, time
import display
from node import Node

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    nodes = []

    while True:
        clearScreen()
        print('''\
Relations Visualizer
    1. create graph
    2. edit/view current nodes
    3. edit/view current relations''')

        selection = input(' > ')
    
        menu_options = [drawGraph, editNodes, editRelations]

        if selection.isnumeric():
            selection = int(selection)
            if 1 <= selection <= len(menu_options):
                menu_options[selection - 1](nodes)
            else:
                print("Invalid Menu Selection")
                time.sleep(1)
        else:
            print("\nInvalid Selection")
            time.sleep(1)

def drawGraph(nodes):
    print('...')
    display.drawGraph(nodes)

def editNodes(nodes):
    while True:
        print('''\
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
            viewNodes(nodes)
        elif selection == '-a':
            addNodes(nodes, entry[3:])
        elif selection == '-r':
            removeNodes(nodes, entry[3:])
        elif selection == '-e':
            return
        else:
            print('Invalid entry\n')

def editRelations(nodes):
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
            viewRelations(nodes)
        elif selection == '-a':
            addRelation(nodes, entry[3:])
        elif selection == '-r':
            removeRelation(nodes, entry[3:])
        elif selection == '-e':
            return
        else:
            print('Invalid entry\n')
            
def viewNodes(nodes: list):
    if not len(nodes):
        print('Currently (0) nodes.\n')
    else:
        print(f'Currently ({len(nodes)}) nodes:')
        print(f'    -{", ".join(sorted([node.name for node in nodes]))}')
        print()

def addNodes(nodes: list, toAdd: str):
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
        nodes.append(Node(node))  
        addedNodes.append(node)
        
    print(f'Successfully added node(s): {", ".join(addedNodes)} \n')

def removeNodes(nodes: list, toRemove: str):
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
            
def viewRelations(nodes):
    if not len(nodes):
        print('No nodes defined.\n')
        return
    else:
        print('Node: [Relations]')
        for node in sorted(nodes):
            print(node)

def addRelation(nodes: list, toAdd):
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

def removeRelation(nodes: list, toRemove):
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
    
if __name__ == '__main__':
    main()