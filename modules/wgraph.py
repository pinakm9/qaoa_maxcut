import networkx as nx
from matplotlib import pyplot as plt
import random

# write a class for conveniently setting up edges for a graph
class Edge:
    """
    Description: a class for implementing a Python directed edge object
    """
    def __init__(self, start_node, end_node):
        """
        Args:
            start_node: integer identifier of the starting node
            end_node: integer identifier of the ending node 
        """
        self.start_node = start_node
        self.end_node = end_node


# write a function for creating a random weighted graph
def gen_random_wgraph(num_nodes, edge_creation_prob, unweighted=False, max_weight=10.0):
    """
    Description: a function for generating a random weighted graph with Erdős–Rényi model

    Args:
        num_nodes: number of nodes
        edge_creation_prob: probability of edge creation between two nodes
        unweighted: a boolean flag to decide if all the edges should have weight 1, default=False
        max_weight: maximum possible weight of an edge, default=10.0

    Returns: the generated random weighted graph        
    """
    # create graph with G(n, p) model
    g = nx.gnp_random_graph(n=num_nodes, p=edge_creation_prob)
    # assign weights randomly
    if not unweighted:
        for (u, v) in g.edges():
            g.edges[u, v]['weight'] = round(random.uniform(0.0, max_weight), 1) # round for making prettier graph plots
    else:
        for (u, v) in g.edges():
            g.edges[u, v]['weight'] = 1.0
    return g


# write a function for creating a randomly weighted graph from a given set of edges
def gen_wgraph_from_edges(edges, unweighted=False, max_weight=10.0):
    """
    Description: a function for generating a randomly weighted graph from a given set of edges

    Args:
        edges: set of Edge objects to construct the graph from
        unweighted: a boolean flag to decide if all the edges should have weight 1, default=False
        max_weight: maximum possible weight of an edge, default=10.0

    Returns: the generated weighted graph        
    """
    g = nx.Graph()
    if not unweighted:
        # assign weights randomly to the given edges
        for z in edges:
            g.add_edge(str(z.start_node), str(z.end_node), weight=round(random.uniform(0.0, max_weight), 1)) # round for making prettier graph plots
    else:
        # assign weight 1 to the given edges
        for z in edges:
            g.add_edge(str(z.start_node), str(z.end_node), weight=1.0)
    return g


# write a function for creating a weighted graph
def plot_wgraph(wgraph):
    """
    Description: a function for displaying a weighted graph

    Args:
        wgraph: the weighted graph to be plotted
    """
    pos = nx.spring_layout(wgraph)
    nx.draw(wgraph, pos)
    labels = nx.get_edge_attributes(wgraph, 'weight')
    nx.draw_networkx_edge_labels(wgraph, pos, edge_labels=labels)
    plt.show()