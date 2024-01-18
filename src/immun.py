import networkx as nx

def immun_high_degree(G, n):
    G = G.copy()
    degs = list(G.degree)
    degs = sorted(degs, key=lambda x: x[1], reverse=True)[:n]
    for node, degs in degs:
        G.nodes[node]["state"] = 'V'
    return G

def immun_page_rank(G, n):
    G = G.copy()
    weights = nx.pagerank(G)
    pg = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:n]
    for node, _ in pg:
        G.nodes[node]["state"] = 'V'
    return G

def immun_betweenness_centrality(G, n):
    G = G.copy()
    centrality = nx.betweenness_centrality(G)
    top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:n]
    for node, _ in top_nodes:
        G.nodes[node]['state'] = 'V'
    return G

def immun_greedy(G, n, beta):
    G = G.copy()
    vaccinated_nodes = set()
    while len(vaccinated_nodes) < n:
        node_impacts = {node: sum(beta for neighbor in G.neighbors(node) if G.nodes[neighbor]['state'] == 'I') for node in G.nodes() if G.nodes[node]['state'] != 'V'}
        node_to_vaccinate = max(node_impacts, key=node_impacts.get)
        vaccinated_nodes.add(node_to_vaccinate)
        G.nodes[node_to_vaccinate]['state'] = 'V'
    return G
