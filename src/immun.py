import networkx as nx

def immun_high_degree(G, n):
    G = G.copy()
    degs = list(G.degree)
    degs = sorted(degs, key=lambda x: x[1], reverse=True)
    vac_nodes = [x[0] for x in degs[:n]]
    for node in vac_nodes:
        G.nodes[node]["state"] = 'V'
    return G

def immun_page_rank(G, n):
    G = G.copy()
    weights = nx.pagerank(G)
    pg = [(node, weight) for (node, weight) in weights.items()]
    pg = sorted(pg, key=lambda x: x[1], reverse=True)
    vac_nodes = [x[0] for x in pg[:n]]
    for node in vac_nodes:
        G.nodes[node]["state"] = 'V'
    return G