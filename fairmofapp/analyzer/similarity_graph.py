#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"

##############################################################################
# fairmofapp is a mof data visualiser package for accelerating the discovery  #
# of MOF. It's primary aim is to provide a patform with which experimentalist #
# can efficiently interact with. This package is being developed by           #
# Dr Dinga Wonanke as part of hos MSCA post doctoral fellowship at TU Dresden.#
#                                                                             #
###############################################################################

import networkx as nx
import plotly.graph_objects as go


def create_graph_from_adjacency_matrix(adj_matrix: dict):
    """
    A function that create a networkx graph from an adjacency matrix
    which is in the form of a python dictionary. Any python dictionary
    should work seamlessly with this function.

    **parameters:**
        adj_matrix (dict): A dictionary where keys are node names,
        and values are dictionaries of neighboring nodes and edge weights.

    **returns:**
        nx.Graph: A NetworkX graph object with nodes and weighted edges.
    """
    nx_graph = nx.Graph()
    for node, neighbors in adj_matrix.items():
        for neighbor, weight in neighbors.items():
            nx_graph.add_edge(node, neighbor, weight=weight)

    return nx_graph


def visualize_interactive_graph(nx_graph: nx.Graph, title):
    """
    A plotly function to create an interactive graph to visualize
    the graph.

    **parameters:**
        nx_graph (nx.Graph): The NetworkX graph object to be visualized.
        title (str): The title of the graph visualization (default is 'Interactive Graph').

    **Returns:**
        A display of the interactive graph in the browser.
    """
    pos = nx.spring_layout(nx_graph)

    node_trace = go.Scatter(
        x=[pos[node][0] for node in nx_graph.nodes()],
        y=[pos[node][1] for node in nx_graph.nodes()],
        text=list(nx_graph.nodes()),
        mode='markers',
        textposition='bottom center',
        hoverinfo='text',
        marker=dict(size=10, color='blue')
    )

    edge_trace = []
    for edge in nx_graph.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        weight = edge[2]['weight']
        edge_trace.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=weight * 2, color='gray'),
            hoverinfo='none',
            mode='lines'
        ))

    fig = go.Figure(data=edge_trace + [node_trace])

    fig.update_layout(
        title=title,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    fig.show()
