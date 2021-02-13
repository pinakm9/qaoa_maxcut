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

# write a wrapper class for networkx.Graph for conveniently displaying weighted graphs
class WeightedGraph(nx.Graph):
    """
    Description: a wrapper class around networkx.Graph for convenient implementation of weighted graphs
    """
    def __init__(self, nx_graph):
        """
        Args:
            nx_graph: networkx.Graph object to wrap around
        """
        self.nx_graph = nx_graph
        self.layout = nx.spring_layout(nx_graph)

    def __getattr__(self, name):
        """
        Description: delegates standard networkx.Graph attributes conveniently
        """
        return getattr(self.nx_graph, name)
    
    def draw(self, cut=None):
        """
        Description: consistently draws the weighted graph

        Args:
            cut: a bit-string to decide node colors, default=None
        """
        if cut is None:
            colors = ['blue' for node in self.nx_graph]
        else:
            colors = ['blue' if cut[int(node)] == '0' else 'red' for node in self.nx_graph]
        nx.draw(self.nx_graph, pos=self.layout, node_color=colors)
        labels = nx.get_edge_attributes(self.nx_graph, 'weight')
        nx.draw_networkx_edge_labels(self.nx_graph, pos=self.layout, edge_labels=labels)
        plt.show()

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
    return WeightedGraph(g)


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
    return WeightedGraph(g)

    