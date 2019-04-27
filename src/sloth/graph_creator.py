#coding:utf-8

"""
Define mechanisms for graph creation due to model connections
"""

import pygraphviz as pgv

class ConnectionGraph:

    """
    Defines ConnectionGraph, that holds the information regarding the connectivity of the Model objects among a Problem
    """

    def __init__(self, name=''):

        self.nodes = []

        self.edges = []

        self.graph = pgv.AGraph(name=name,  ranksep=.5, directed=True)

    def add_node(self, id_name, shape='box', color='black', label=""):

        self.graph.add_node(id_name, shape=shape, color=color, label=label)

        self.nodes.append(id_name)

    def add_edge(self, node_1_id_name, node_2_id_name):

        self.edges.append( (node_1_id_name, node_2_id_name) )

        self.graph.add_edge(node_1_id_name, node_2_id_name)

    def draw(self, file_name, show_headings):

        if show_headings is False:

            self.graph.node_attr.update(label="")

        self.graph.layout(prog='dot')

        self.graph.draw(file_name)

