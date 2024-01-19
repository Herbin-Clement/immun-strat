import numpy as np
import random
import networkx as nx
from tqdm import tqdm
import src.sis as sis
import multiprocessing

def get_not_infected_nodes(G):
    """
    Return the list of nodes that are not infected
    """
    not_infected_nodes = []
    for node, data in G.nodes(data=True):
        if data["state"] != 'I':
            not_infected_nodes.append(node)
    return not_infected_nodes

def get_neighbourhood_subgraph(G, node, k):
    """
    Returns induced subgraph of neighbors centered at node within a given radius k.
    """
    return nx.ego_graph(G, node, radius=k)

def get_subgraph(G, infected_nodes, k):
    """
    Get a subgraph of neighbors centered at infected nodes
    """
    subgraph = get_neighbourhood_subgraph(G, infected_nodes[0], k)
    nodes = set()
    for node in infected_nodes[1:]:
        subgraph = nx.compose(subgraph, get_neighbourhood_subgraph(G, node, k))
    for node, state in subgraph.nodes(data=True):
        if state["state"] == 'S':
            nodes.add(node)
    print(subgraph.number_of_nodes(), subgraph.number_of_edges())
    return subgraph, list(nodes)

def V(G, beta, gamma, S, node=None, R=10):
    if node != None:
        G.nodes[node]["state"] = 'V'
    return np.mean([sis.run_fast_sis(G, beta, gamma) for _ in range(R)])

def greedy_algorithm(G, infected_nodes, n_vac, beta, gamma):
    """
    """
    W = []
    GW, not_inf_vac_nodes = get_subgraph(G, infected_nodes, 1)
    for _ in range(n_vac):
        delta_W_u = []
        VW = V(GW, beta, gamma, infected_nodes)
        for i in tqdm(range(len(not_inf_vac_nodes))):
            node = not_inf_vac_nodes[i]
            VWp = V(GW, beta, gamma, node)
            delta_W_u.append((node, VW - VWp))
            GW.nodes[node]["state"] = 'S'
        best_node = max(delta_W_u, key=lambda k: k[1])[0]
        W.append(best_node)
        not_inf_vac_nodes.remove(best_node)
        GW.nodes[best_node]["state"] = 'V'
        G.nodes[best_node]["state"] = 'V'
    return G, W