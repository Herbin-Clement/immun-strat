import numpy as np
import random
from tqdm import tqdm

def get_not_infected_nodes(G):
    """
    Return the list of nodes that are not infected
    """
    not_infected_nodes = []
    for node, data in G.nodes(data=True):
        if data["state"] != 'I':
            not_infected_nodes.append(node)
    return not_infected_nodes

def remove_edge_from_nodes(G, nodes):
    """
    Remove every edges connected to the nodes
    """
    GS = G.copy()
    E = set()
    for u in nodes:
        neighbors = GS.neighbors(u)
        for v in neighbors:
            if u > v:
                E.add((u, v))
            else:
                E.add((v, u))
    for u, v in E:
        GS.remove_edge(u, v)
    return GS, E

def run_fast_sis(G, beta, gamma, S):
    """
    Run a simulation of a SIS model
    """
    G = G.copy()
    inf = 0
    S_copy = [node for node in S]
    for _ in range(2):
        nodes = []
        next_S = []
        for node in S_copy:
            if np.random.rand() < gamma:            
                nodes.append((node, 'S'))
                inf -= 1
            else:
                next_S.append(node)
            for ne in G.neighbors(node):               
                if G.nodes[ne]["state"] == 'S':     
                    if np.random.rand() < beta:     
                        nodes.append((ne, 'I'))
                        inf += 1
                        next_S.append(ne)
        for node, state in enumerate(nodes): # update graph and save state
            G.nodes[node]["state"] = state
    return inf

def V(G, beta, gamma, S, node=None):
    if node != None:
        G.nodes[node]["state"] = 'V'
    return run_fast_sis(G, beta, gamma, S)

def greedy_algorithm(G, infected_nodes, n_vac, beta, gamma):
    """
    """
    W = []
    GW = G.copy()
    not_inf_nodes = get_not_infected_nodes(G)
    not_inf_vac_nodes = not_inf_nodes
    for _ in range(n_vac):
        delta_W_u = []
        VW = V(GW, beta, gamma, infected_nodes)
        for i in tqdm(range(len(not_inf_vac_nodes))):
            node = not_inf_vac_nodes[i]
            VWp = V(GW, beta, gamma, infected_nodes, node)
            delta_W_u.append((node, VW - VWp))
            GW.nodes[node]["state"] = 'S'
        best_node = max(delta_W_u, key=lambda k: k[1])[0]
        W.append(best_node)
        not_inf_vac_nodes.remove(best_node)
        GW.nodes[best_node]["state"] = 'V'
    return GW, W

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
            