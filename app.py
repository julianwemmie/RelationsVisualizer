import typing as t

from graphsManager import GraphsManager
from display import IDisplay, TurtleDisplay, DearPyGui
from forceDirectedGraph import ForceDirectedGraph as FDG, NodeBalancer
from helpers import clearScreen, parseArguments

class App:
    def __init__(self, display: IDisplay, nodeBalancer: NodeBalancer, graphsManager: GraphsManager, defaultGraphName: str = 'untitled') -> None:
        self.display = display
        self.nodeBalancer = nodeBalancer
        self.graphsManager = graphsManager
        self.graphsManager.createGraph(defaultGraphName)
        self.graphsManager.currentGraph = defaultGraphName

    def mainMenu(self):
        clearScreen()
        while True:
            print(
'''
1. Display Graph
2. Edit Nodes
3. Edit Relations
4. Select/Edit Graphs
5. Import/Export Graphs
6. Exit
''')
        
            userInput = input(' > ')
            userInput = userInput.strip()

            if not userInput or len(userInput) > 1:
                print("Invalid input.")
                continue

            userInput = userInput[0]

            if userInput == '1':
                self.displayGraph()
            elif userInput == '2':
                self.editNodes()
            elif userInput == '3':
                self.editRelations()
            elif userInput == '4':
                self.editGraphs()
            elif userInput == '5':
                self.importExportGraphs()
            elif userInput == '6':
                break
            else:
                print('Invalid selection.')
        
    def editNodes(self):
        while True:
            print(
'''
-l              : List Nodes
-a [nodeName]   : Add Node
-r [nodeName]   : Remove Node
-e              : Exit to main menu
''')
            
            userInput = input(' > ')
            userInput = parseArguments(userInput)

            currentGraph = self.graphsManager.currentGraph

            if not userInput:
                print('Invalid input')
                continue
            
            if userInput[0] == '-l':
                nodes = currentGraph.getNodeNames()
                print(nodes)

            elif userInput[0] == '-a' and len(userInput) >= 2:
                nodeNames = userInput[1:]
                try:
                    currentGraph.addNodes(nodeNames)
                    print(f'Added node(s): {nodeNames}')
                except NameError as e:
                    print(e)

            elif userInput[0] == '-r' and len(userInput) >= 2:
                nodeNames = userInput[1:]
                try:
                    currentGraph.removeNodes(nodeNames)
                    print(f'Removed node(s): {nodeNames}')
                except NameError as e:
                    print(e)
                
            elif userInput[0] == '-e':
                clearScreen()
                break

            else:
                print('Invalid input or missing arguments')

    def editRelations(self):
        while True:
            print(
'''
-l                          : List Relations
-a [nodeName], [nodeName]   : Add Relation
-r [nodeName], [nodeName]   : Remove Relation
-e                          : Exit to main menu
''')
            userInput = input(' > ')
            userInput = parseArguments(userInput)

            currentGraph = self.graphsManager.currentGraph

            if not userInput:
                print('Invalid input')
                continue

            if userInput[0] == '-l':
                relationsMap = currentGraph.relationsMap
                print('Relations')
                for name, related in relationsMap.items():
                    print(f'   {name}: {", ".join(related)}')

            elif userInput[0] == '-a' and len(userInput) >= 3:
                node1, node2 = userInput[1], userInput[2]
                try:
                    currentGraph.addRelation(node1, node2)
                    print(f'Added relation: {node1}, {node2}')
                except NameError as e:
                    print(e)

            elif userInput[0] == '-r' and len(userInput) >= 3:
                node1, node2 = userInput[1], userInput[2]
                try:
                    currentGraph.removeRelation(node1, node2)
                    print(f'Removed relation: {node1}, {node2}')
                except NameError as e:
                    print(e)

            elif userInput[0] == '-e':
                break

            else:
                print('Invalid input or missing arguments')

    def editGraphs(self):
        while True:
            print('Graphs:')
            for graph in self.graphsManager.graphs:
                if graph == self.graphsManager.currentGraph:
                    print(f'   [{graph.name}]')
                else:
                    print(f'    {graph.name}')
            print(
'''
-s [graphName]                 : Select graph
-a [graphName]                 : Add a new graph
-r [graphName]                 : Remove a graph
-n [originalName], [newName]   : Rename graph
-e                              : Exit to main menu
'''
            )

            userInput = input(' > ')
            userInput = parseArguments(userInput)

            if not userInput:
                print('Invalid input')
                continue

            if userInput[0] == '-s' and len(userInput) == 2:
                graphName = userInput[1]
                try:
                    self.graphsManager.currentGraph = graphName
                except NameError as e:
                    print(e)

            elif userInput[0] == '-a' and len(userInput) >= 2:
                graphName = userInput[1]
                try:
                    self.graphsManager.createGraph(graphName)
                    print(f'Added graph: {graphName}')
                except NameError as e:
                    print(e)

            elif userInput[0] == '-r' and len(userInput) >= 2:
                graphName = userInput[1]
                try:
                    self.graphsManager.deleteGraph(graphName)
                    print(f'Removed graph: {graphName}')
                except NameError as e:
                    print(e)
                    
            elif userInput[0] == '-n' and len(userInput) == 3:
                originalName, newName = userInput[1], userInput[2]
                try:
                    self.graphsManager.renameGraph(originalName, newName)
                    print(f'Renamed graph: {originalName} -> {newName}')
                except NameError as e:
                    print(e)

            elif userInput[0] == '-e':
                break

            else:
                print('Invalid input or missing arguments')

    def displayGraph(self):
        currentGraph = self.graphsManager.currentGraph
        currentGraph.balanceNodes(self.nodeBalancer)
        self.display.drawGraph(currentGraph)

    def importExportGraphs(self):
        while True:
            print(
'''
-i [fileName]   : Import graph
-x [fileName]   : Export graph
-e              : Exit to main menu
''')
            userInput = input(' > ')
            userInput = parseArguments(userInput)

            if not userInput:
                print('Invalid input')
                continue

            if userInput[0] == '-i' and len(userInput) == 2:
                fileName = userInput[1]
                try:
                    self.graphsManager.importGraph(fileName)
                    print(f'Imported graph: {fileName}')
                except Exception as e:
                    print(e)

            elif userInput[0] == '-x' and len(userInput) == 2:
                fileName = userInput[1]
                try:
                    self.graphsManager.exportGraph(fileName)
                    print(f'Exported graph: {fileName}')
                except Exception as e:
                    print(e)

            elif userInput[0] == '-e':
                break

            else:
                print('Invalid input or missing arguments')

if __name__ == '__main__':
    display = TurtleDisplay()
    # display = DearPyGui()
    nodeBalancer = FDG()
    graphsManager = GraphsManager()
    app = App(display, nodeBalancer, graphsManager)
    app.mainMenu()