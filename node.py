class Node:
    def __init__(self, name):
        self.name = name
        self.xPos = 0
        self.yPos = 0

    def setPosition(self, x, y):
        self.xPos = x
        self.yPos = y    