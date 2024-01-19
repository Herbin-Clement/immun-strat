import pandas as pd
import numpy as np
import networkx as nx

def get_graph(filename, sep="\t"):
    """
    Get edges data from a file
    Remove self-loop and select the biggest connected component 
    """
    grqc = pd.read_csv(filename, sep=sep, header=None)

    G = nx.Graph()

    for _, row in grqc.iterrows():
        G.add_edge(row[0], row[1])
    G.remove_edges_from(nx.selfloop_edges(G))

    for node in G.nodes(data=False):
        G.nodes[node]["state"] = 'S'
    
    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    G = G.subgraph(Gcc[0])
    G = nx.convert_node_labels_to_integers(G)

    print(f"G({G.number_of_nodes()}, {G.number_of_edges()})")
    return G