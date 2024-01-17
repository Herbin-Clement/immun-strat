import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

if __name__ == "__main__":
    n = 100
    m = 3
    seed = 1
    g = nx.barabasi_albert_graph(n, m, seed)
