# Project Title

A simple model of a brain of a worm: a ring of 5 connected neurons (nodes).

## Description

An in-depth paragraph about your project and overview of use.

The ring is represented as 5 connected (we set the way of connections) nodes.
These 5 nodes are adapted for solving a simple task: determining majority value.
Each node may have only a binary input value: 0 or 1.
If among 5 nodes there are 3 or more with value 0, then the majority value is 0.
If there are 3 or more with value 1, then the majority value is 1.

## Getting Started

Here we manually set the input values.
    # Creating the nodes with manually set values
    node_1 = Node(1)
    node_2 = Node(0)
    node_3 = Node(1)
    node_4 = Node(0)
    node_5 = Node(1)

Here we manually set connections between the nodes.
    # Initializing nodes' connections
    node_1.update_connections([node_2, node_3])
    node_2.update_connections([node_3, node_4, node_5])
    node_3.update_connections([node_4])
    node_4.update_connections([node_5])
    node_5.update_connections([node_1])

We "call" the nodes manually, one node at a time:
    # Calling each node once, one node at a time
    node_1.start()
    node_2.start()
    node_3.start()
    node_4.start()
    node_5.start()

### Dependencies

no dependencies

### Installing


### Executing program

Program does not require any parameters for launching.

## Help

## Authors

vch12

## Version History

Current version 0.05

## License


## Acknowledgments

