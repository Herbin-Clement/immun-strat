import networkx as nx

def immun_high_degree(G, n):
    """
    Add vaccinated node with highest degree
    """
    Gc = G.copy()
    degs = list(Gc.degree)
    degs = sorted(degs, key=lambda x: x[1], reverse=True)[:n]
    for node, degs in degs:
        Gc.nodes[node]["state"] = 'V'
    return Gc

def immun_page_rank(G, n):
    """
    Add vaccinated node with highest PageRank
    """
    Gc = G.copy()
    weights = nx.pagerank(Gc)
    pg = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:n]
    for node, _ in pg:
        Gc.nodes[node]["state"] = 'V'
    return Gc

def immun_betweenness_centrality(G, n):
    """
    Add vaccinated node with highest betweenness centrality
    """
    Gc = G.copy()
    centrality = nx.betweenness_centrality(Gc)
    top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:n]
    for node, _ in top_nodes:
        Gc.nodes[node]['state'] = 'V'
    return Gc