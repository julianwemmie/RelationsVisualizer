
import os, time
import display
from node import Node

# TODO: no need for Node.node_names since made nodes into dict. need to remove Node.node_name functionality

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    nodes = {}

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
    display.drawGraph(nodes.values())

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
    -w | edit relation weight
            '-w a,b,5 --> sets relation weight to 5
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
        elif selection == '-w':
            editRelationWeight(nodes, entry[3:])
        elif selection == '-e':
            return
        else:
            print('Invalid entry\n')
            
def viewNodes(nodes):
    print(f'Currently ({len(nodes)}) nodes:')
    if len(nodes):
        print(f'    -{", ".join(sorted(Node.node_names))}')
    print()

def addNodes(nodes, toAdd):
    if not len(toAdd):
        print('Specify nodes to add. Ex: "-a a,b,c"\n')
        return

    addedNodes = []
    for node in toAdd.strip().split(','):
        if node == '':
            continue
        if node in nodes.keys():
            print(f'Node already exists: {node}')
            continue
        nodes[node] = Node(node)
        addedNodes.append(node)
        
    print(f'Successfully added node(s): {", ".join(addedNodes)} \n')

def removeNodes(nodes, toRemove):
    if not len(toRemove):
        print('Specify nodes to remove. Ex: "-r a,b,c"\n')
        return
    
    removed = []
    for node in toRemove.strip().split(','):
        if node in nodes.keys():
            removed.append(nodes[node])
            del nodes[node]
                
    for node in removed:
        Node.removeNode(node)
        for edge in node.edges:
            edge.edges.remove(node)
            
    print(f'Successfully removed node(s): {", ".join([node.name for node in removed])}\n')
            
def viewRelations(nodes):
    if len(Node.edge_weights) == 0:
        print('No relations defined.\n')
        return
    else:
        print('Relation | Weight')
        for relation in Node.edge_weights.items():
            node1 = relation[0][0]
            node2 = relation[0][1]
            weight = relation[1]

            print(f'{node1} <-> {node2} | {weight}')

def addRelation(nodes, toAdd):
    # TODO: doesn't catch already existing relations
    if len(toAdd) < 3:
            print('Specify relations to add. Ex: "-a a,b"\n')
            return    

    toAdd = toAdd.strip().split(',')
    for node in toAdd:
        if node == '':
            continue
        if node not in Node.node_names:
            print('One or more nodes does not exist. \n')
            return

    node1 = toAdd[0]
    node2 = toAdd[1]

    # get node object from dictionary
    node1 = nodes[node1]
    node2 = nodes[node2]

    node1.connect(node2)
    Node.addWeight(node1, node2, 0)

    print(f'Successfully added relation: {node1.name}, {node2.name}\n')

def removeRelation(nodes, toRemove):
    if len(toRemove) < 3:
            print('Specify relations to remove. Ex: "-a a,b"\n')
            return    
        
    toRemove = toRemove.strip().split(',')

    for node in toRemove:
        if node not in Node.node_names:
            print('One or more nodes does not exist. \n')
            return   
        
    node1 = toRemove[0]
    node2 = toRemove[1]

    # get node object from dictionary
    node1 = nodes[node1]
    node2 = nodes[node2]

    node1.disconnect(node2)
    Node.removeRelation(node1, node2)

    print(f'Successfully removed relation: {node1.name}, {node2.name}\n')

def editRelationWeight(nodes, toEdit):
    if len(toEdit.strip()) < 5:
        print("Invalid Input\n")
        return

    try:
        node1, node2, weight = toEdit.split(',')
    except ValueError:
        print('Invalid Input\n')
        return

    if node1 == node2:
        print('Node cannot relate to itself\n')
        return

    if (node1 or node2) not in Node.node_names:
        print('One or more nodes does not exist\n')
        return

    if not weight.isnumeric():
        print('Weight must be an integer\n')
        return

    weight = int(weight)

    node1 = nodes[node1]
    node2 = nodes[node2]

    try:
        Node.addWeight(node1, node2, weight)
    except IndexError:
        print("Relation does not exist\n")
        return
    
if __name__ == '__main__':
    main()