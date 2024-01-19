import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import src.utils as utils
import src.sis as sis
import src.immun as immun
import src.data as data
import src.greedy as gr

n = 5000
m = 3
beta = 0.8
gamma = 0.4
t_max = 12
n_inf = 5
n_vac = 10

# print("Barabasi-Albert graph ...")
# print("Get graph ...")
# BA = sis.generate_barabasi_albert_graph(n, m, 10)
# print("Run simulation without cluster ...")
# sis.run_sim(BA, n_inf, n_vac, beta, gamma, t_max, "ba", "Infected growth (Barabasi-Albert graph)", cluster=False)
# print("Run simulation with cluster ...")
# sis.run_sim(BA, n_inf, n_vac, beta, gamma, t_max, "ba_clust", "Infected growth (Barabasi-Albert graph)", cluster=True)

# print("GRQC network ...")
# print("Get graph ...")
# GRQC = data.get_graph("graph/grqc.txt")
# print("Run simulation without cluster ...")
# sis.run_sim(GRQC, n_inf, n_vac, beta, gamma, t_max, "grqc", "Infected growth (GRQC network)", cluster=False)
# print("Run simulation with cluster ...")
# sis.run_sim(GRQC, n_inf, n_vac, beta, gamma, t_max, "grqc_clust", "Infected growth (GRQC network)", cluster=True)

# print("HepTH network ...")
# print("Get graph ...")
# HEPTH = data.get_graph("graph/HepTh.txt")
# print("Run simulation without cluster ...")
# sis.run_sim_without_betweenness(HEPTH, n_inf, n_vac, beta, gamma, t_max, "hepth", "Infected growth (HEPTH network)", cluster=False)
# print("Run simulation with cluster ...")
# sis.run_sim_without_betweenness(HEPTH, n_inf, n_vac, beta, gamma, t_max, "hepth_clust", "Infected growth (HEPTH network)", cluster=True)

print("Deezer network ...")
print("Get graph ...")
deezer = data.get_graph("graph/deezer.txt", sep=",") 
print("Run simulation without cluster ...")
sis.run_sim_without_betweenness(deezer, n_inf, n_vac, beta, gamma, t_max, "deezer", "Infected growth (Deezer network)", cluster=False)
print("Run simulation with cluster ...")
sis.run_sim_without_betweenness(deezer, n_inf, n_vac, beta, gamma, t_max, "deezer_clust", "Infected growth (Deezer network)", cluster=True)

print("enron network ...")
print("Get graph ...")
enron = data.get_graph("graph/enron.txt")
print("Run simulation without cluster ...")
sis.run_sim_without_betweenness(enron, n_inf, n_vac, beta, gamma, t_max, "enron", "Infected growth (Enron network)", cluster=False)
print("Run simulation with cluster ...")
sis.run_sim_without_betweenness(enron, n_inf, n_vac, beta, gamma, t_max, "enron_clust", "Infected growth (Enron network)", cluster=True)