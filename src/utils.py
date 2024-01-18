import networkx as nx

def print_g_carac(G, name="G"):
    """
    Print differents metrics of the graph
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()
    print(f"{name} n = {n}, m = {m}, max_deg = {max(G.degree, key=lambda x: x[1])}, transitivity = {nx.transitivity(G)}")