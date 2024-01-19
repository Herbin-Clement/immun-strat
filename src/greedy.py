import numpy as np
import random
import networkx as nx
from tqdm import tqdm
import src.sis as sis

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
    return nx.ego_graph(G, node, radius=k)#Subgraph.nodes(data=True)

def get_subgraph(G, infected_nodes, k):
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
    GW, not_inf_vac_nodes = get_subgraph(G, infected_nodes, 2)
    for _ in range(n_vac):
        delta_W_u = []
        VW = V(GW, beta, gamma, infected_nodes)
        for i in tqdm(range(len(not_inf_vac_nodes))):
            node = not_inf_vac_nodes[i]
            VWp = V(GW, beta, gamma, node)
            delta_W_u.append((node, VW - VWp))
            GW.nodes[node]["state"] = 'S'
        print(delta_W_u)
        best_node = max(delta_W_u, key=lambda k: k[1])[0]
        W.append(best_node)
        not_inf_vac_nodes.remove(best_node)
        GW.nodes[best_node]["state"] = 'V'
        G.nodes[best_node]["state"] = 'V'
    return G, W

# def greedy_algorithm(G, infected_nodes, n_vac, beta, gamma):
#     """
#     """
#     W = []
#     GS, _ = remove_edge_from_nodes(G, infected_nodes)
#     GW = GS.copy()
#     not_inf_nodes = get_not_infected_nodes(G)
#     not_inf_vac_nodes = not_inf_nodes
#     for _ in range(n_vac):
#         delta_W_u = []
#         VW = V(GW, beta, gamma, infected_nodes)
#         for i in tqdm(range(len(not_inf_vac_nodes))):
#             node = not_inf_nodes[i]
#             Wp = W + [node]
#             GWp, _ = remove_edge_from_nodes(GW, [node])
#             VWp = V(GWp, beta, gamma, infected_nodes)
#             print(VW, VWp)
#             delta_W_u.append((node, VW - VWp))
#         best_node = max(delta_W_u, key=lambda k: k[1])[0]
#         W.append(best_node)
#         not_inf_vac_nodes.remove(best_node)
#         GW, _ = remove_edge_from_nodes(GW, [best_node])
#     for node in W:
#         G.nodes[node]['state'] = 'V'
            