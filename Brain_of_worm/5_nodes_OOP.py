# 5 connected nodes for solving the majority classification problem
# 4 May 2022
# information exchange through 2 methods and two variables
# 1 -> 2 -> 3 -> 4 -> 5
# Think how to implement: All nodes are interconnected

class Node:
    # Class attribute
    # number_nodes = 5

    # initialization of an instance
    def __init__(self, input_val):
        self.input = input_val
        self.sum = 0
        self.counter = 0
        self.connections = []
        self.majority = 0

    # method for updating connections of a node
    def update_connections(self, list_of_nodes_val):
        print('list_of_nodes: %s' % list_of_nodes_val)
        print('self.connections = %s' % self.connections)
        self.connections = list_of_nodes
        print('self.connections = %s' % self.connections)
        print('========')

    # Here a node computes new sum, updates the counter
    # and sends them to all the connected nodes
    def start(self):
        print('BEFORE self.sum = %s' % self.sum)
        self.sum = self.sum + self.input
        print('AFTER self.sum = %s' % self.sum)

        print('BEFORE self.counter = %s' % self.counter)
        self.counter = self.counter + 1
        print('AFTER self.counter = %s' % self.counter)

        for x in range(len(self.connections)):
            print('current x = %s' % x)
            print('current node: %s' % self.connections[x])
            # here we send current sum from this node to a connected node
            self.connections[x].update_sum(self.sum)
            # here we send current counter from this node to a connected node
            self.connections[x].update_counter(self.counter)
            print('*****')

            #self.connections = list_of_nodes
            #print('self.connections = %s' % self.connections)
            ###self.connections[x].sum = self.sum + self.input
            ###self.connections[x].counter = self.counter + 1
            # self.connections[x].majority = 100

    # updating of a self.sum variable of a node
    def update_sum(self, value):
        self.sum = value

    # updating of a self.counter variable of a node
    def update_counter(self, value):
        self.counter = value

    # when the majority value is determined
    # updating of a self.majority variable of a node
    def update_maj_in_node(self, value):
        self.majority = value


if __name__ == '__main__':
    # Creating the nodes with manually set values
    node_1 = Node(1)
    node_2 = Node(0)
    node_3 = Node(1)
    node_4 = Node(0)
    node_5 = Node(1)

    list_of_nodes = [node_1, node_2, node_3, node_4, node_5]

    # Initializing nodes' connections
    node_1.update_connections([node_2, node_3])
    node_2.update_connections([node_3, node_4, node_5])
    node_3.update_connections([node_4])
    node_4.update_connections([node_5])
    node_5.update_connections([node_1])

    # Calling each node once, one node at a time
    node_1.start()
    node_2.start()
    node_3.start()
    node_4.start()
    node_5.start()  # here we could block sending data to node_1

    print('node_1.input = %s' % node_1.input)
    print('node_1.sum = %s' % node_1.sum)
    print('node_1.counter = %s' % node_1.counter)

    print('node_2.input = %s' % node_2.input)
    print('node_2.sum = %s' % node_2.sum)
    print('node_2.counter = %s' % node_2.counter)

    print('node_3.input = %s' % node_3.input)
    print('node_3.sum = %s' % node_3.sum)
    print('node_3.counter = %s' % node_3.counter)

    print('node_4.input = %s' % node_4.input)
    print('node_4.sum = %s' % node_4.sum)
    print('node_4.counter = %s' % node_4.counter)

    print('node_5.input = %s' % node_5.input)
    print('node_5.sum = %s' % node_5.sum)
    print('node_5.counter = %s' % node_5.counter)
    print('========')

    print('average input value = %s' % (node_5.sum / node_5.counter))

    # Calculating majority input value
    if (node_5.sum / node_5.counter) > 0.5:
        majority = 1
    else:
        if (node_5.sum / node_5.counter) < 0.5:
            majority = 0
        else:
            majority = 999  # not the case when number of nodes is odd
    print('majority = %s' % majority)
    print('length of list_of_nodes = %s' % len(list_of_nodes))

    # Updating majority value in all the nodes
    for x in range(len(list_of_nodes)):
        print('current x = %s' % x)
        print('current node: %s' % list_of_nodes[x])
        list_of_nodes[x].update_maj_in_node(majority)
    print('========')

    print('node_1.majority = %s' % node_1.majority)
    print('node_2.majority = %s' % node_2.majority)
    print('node_3.majority = %s' % node_3.majority)
    print('node_4.majority = %s' % node_4.majority)
    print('node_5.majority = %s' % node_5.majority)