# Basic Graph Visualization Tool 
A simple tool for visualizing node-based graphs using a force-directed algorithm. This was written as an exercise  
in implementing algorthims, practicing object oriented programing concepts, and using git for version control. 

## Requirements
- NumPy (Written using version 1.23.2, but should work on any version)

## Features
 - Implements Force Directed Graph Algorithm
    - Models nodes and connections using physical forces (springs for attraction and magnetism for repulsion)
    - Algorithm based on the one described in section 12.2 of [this paper](https://cs.brown.edu/people/rtamassi/gdhandbook/chapters/force-directed.pdf) by Stephen G. Kobourov
 - User Interface via Terminal
    - Menu system to view, add, and edit both nodes and relations
    - Catches invalid inputs, duplicate elements, and unwanted relations
 - Graph Display Implemented with Python Turtle