import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import src.utils as utils
import src.sis as sis
import src.immun as immun
import src.data as data
import src.greedy as gr


n = 10000
seed = 100
beta = 0.4
gamma = 0.4
t_max = 12
m = 3
initial_infected_nodes = 5
initial_vaccinated_nodes = 5

print("Get graph...")
GRQC = sis.generate_barabasi_albert_graph(n, m, 10)
# GRQC = data.get_graph("graph/GRTQC.txt")
# print("Add infected nodes...")
# S = sis.add_random_infected(GRQC, initial_infected_nodes)
# print("Greedy algorithm...")
# GW, W = gr.greedy_algorithm(GRQC, S, initial_vaccinated_nodes)
sis.run_sim3(
    GRQC,
    initial_infected_nodes,
    initial_vaccinated_nodes,
    beta,
    gamma,
    t_max,
    "test",
    "Infected growth (test network graph)"
)