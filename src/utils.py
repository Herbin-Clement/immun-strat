import networkx as nx

def print_g_carac(G, name="G"):
    n = G.number_of_nodes()
    m = G.number_of_edges()
    print(f"{name} has {n} nodes and {m} edges")