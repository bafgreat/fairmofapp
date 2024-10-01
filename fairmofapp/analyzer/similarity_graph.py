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
import os
import shutil
import gzip
import networkx as nx
import plotly.graph_objects as go
import pandas as pd


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
        marker=dict(size=20, color='blue')
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
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False)
    )
    return fig


def get_similar_mofs(mof_name, adj_matrix, top_n=5):
    '''
    A function that returns the top n similar MOFs to a given MOF.
    **parameters:**
        mof_name (str): The name of the MOF for which similarities are to be found.
        adj_matrix (dict): A dictionary where keys are MOF names,
        and values are dictionaries of neighboring MOFs and their similarity scores.
        top_n (int): The number of similar MOFs to return (default is 5).
    '''
    if mof_name not in adj_matrix:
        return pd.DataFrame(columns=["MOF", "Similarity"])

    mof_similarities = adj_matrix[mof_name]
    sorted_mofs = sorted(mof_similarities.items(), key=lambda x: x[1], reverse=True)
    sorted_mofs = [(name, score) for name, score in sorted_mofs if name != mof_name]
    return pd.DataFrame(sorted_mofs[:top_n], columns=["MOF", "Similarity"])


def search_and_extract_from_gzip(mof_names, gzip_path, output_dir="mof_folders"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with gzip.open(gzip_path, 'rb') as gz_file:
        file_content = gz_file.read()

        for mof_name in mof_names:
            mof_filename = f"{mof_name}_fair_op.cif"

            if mof_filename in file_content.decode('utf-8'):
                mof_output_path = os.path.join(output_dir, mof_filename)

                with open(mof_output_path, 'wb') as extracted_file:
                    extracted_file.write(file_content)

    return output_dir


# from mofstructure import filetyper
# data = filetyper.load_data('../../data/store/A0.json')
# nx_graph = create_graph_from_adjacency_matrix(data)
# print (nx_graph)
# fig = visualize_interactive_graph(nx_graph, 'Social_network')