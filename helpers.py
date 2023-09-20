import os

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def parseArguments(userInput: str):
    userInput = userInput.strip()

    inputs = userInput.split(' ')
    inputs = [inpt for inpt in inputs if inpt != '']

    if not inputs:
        return []

    if len(inputs[0]) != 2:
        return []
    
    if not inputs[0][0] == '-' or not inputs[0][1].isalpha():
        return []
    
    arguments = []
    arguments.append(inputs.pop(0))

    for inpt in inputs:
        [arguments.append(item) for item in inpt.split(',')]

    return arguments

