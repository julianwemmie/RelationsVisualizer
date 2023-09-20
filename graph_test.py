from node import Node
from graph import Graph

def addNode_test():
    graph = Graph()
    graph.addNode('a')

    condition1 = 'a' in graph.nodes
    condition2 = 'a' in graph.relationsMap

    return all([condition1, condition2])

def addRelation_test():
    graph = Graph()
    graph.addNode('a')
    graph.addNode('b')

    graph.addRelation('a', 'b')

    condition1 = set(('a', 'b')) in graph.relations
    condition2 = graph.relationsMap == {
        'a': ['b'],
        'b': ['a']
    }
    return all([condition1, condition2])

def removeNode_test():
    graph = Graph()
    graph.addNode('a')
    graph.removeNode(nodeName='a')

    condition1 = 'a' not in graph.nodes
    condition2 = 'a' not in graph.relationsMap
    return all([condition1, condition2])

def removeRelation_test():
    graph = Graph()
    graph.addNode('a')
    graph.addNode('b')
    graph.addRelation('a', 'b')
    graph.removeRelation('a', 'b')

    condition1 = 'a' in graph.nodes
    condition2 = 'b' in graph.nodes
    condition3 = set(('a', 'b')) not in graph.relations
    condition4 = 'b' not in graph.relationsMap['a']

    return all([condition1, condition2, condition3, condition4])

def stressTest_test():
    graph = Graph()
    graph.addNode('a')
    graph.addNode('b')
    graph.addNode('c')
    graph.addNode('d')

    graph.removeNode(nodeName='c')

    graph.addRelation('a', 'b')
    graph.addRelation('a', 'd')
    graph.addRelation('b', 'd')

    graph.removeNode(nodeName='a')
    graph.removeRelation('b', 'd')

    condition1 = 'a' not in graph.nodes
    condition2 = 'a' not in graph.relationsMap['b']
    condition3 = 'a' not in graph.relationsMap
    condition4 = set(('a', 'b')) not in graph.relations

    return all([condition1, condition2, condition3, condition4])

def runTests():
    tests = [
        addNode_test,
        addRelation_test,
        removeNode_test,
        removeRelation_test,
        stressTest_test
    ]

    for test in tests:
        print(f'{test.__name__}')
        passed = test()
        print(f'\t{passed}')
        
if __name__ == '__main__':
    runTests()