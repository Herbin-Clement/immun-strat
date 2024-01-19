import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import src.immun as immun
import src.utils as utils
import src.greedy as gr
from tqdm import tqdm 

def generate_barabasi_albert_graph(n, m, seed):
    """
    Generate B(n,m) Barabasi-Albert model
    """
    G = nx.barabasi_albert_graph(n, m, seed)
    for node in G.nodes(data=False):
        G.nodes[node]["state"] = 'S'
    return G

def add_random_infected(G, n):
    """
    Add n infected nodes in G randomly
    """
    i = 0
    nodes = list(G.nodes)
    S = []
    while i < n:
        node = random.sample(nodes, 1)[0]
        s = G.nodes[node]["state"]
        if s != 'V' and s != 'I':
            G.nodes[node]["state"] = 'I'
            S.append(node)
            i += 1
    return S

def add_cluster_infected(G, n):
    i = 0
    nodes = list(G.nodes)
    S = []
    found = False
    while not found:
        node = random.sample(nodes, 1)[0]
        s = G.nodes[node]["state"]
        if s != 'V' and s != 'I':
            G.nodes[node]["state"] = 'I'
            S.append(node)
            found = True
            while len(S) < n:
                for ne in G.neighbors(S[i]):
                    s = G.nodes[ne]["state"] 
                    if s != 'V' and s != 'I':
                        G.nodes[ne]["state"] = 'I'
                        S.append(ne)
                        if len(S) == n:
                            return S
                i += 1

def print_g_sis_carac(G, name="G"):
    """
    Print differents caracteristic for SIS model
    """
    susceptible = 0
    infected = 0
    vaccinated = 0
    for _, data in G.nodes(data=True):
        if data["state"] == 'S':
            susceptible += 1
        elif data["state"] == 'V':
            vaccinated += 1
        else:
            infected += 1
    print(f"{name} has {vaccinated} vaccinated nodes, {susceptible} suceptibles nodes and {infected} infected nodes")
    
def draw_g_sis(G, color_sus="green", color_inf="red", color_vac="blue"):
    """
    Draw the graph
    """
    cmp = []
    for _, data in G.nodes(data=True):
        if data["state"] == 'S':
            cmp.append(color_sus)
        elif data["state"] == 'I':
            cmp.append(color_inf)
        else:
            cmp.append(color_vac)
        
    nx.draw(G, node_color=cmp, node_size=100, width=0.5, with_labels=len(G.nodes) < 100, font_size=7)

def plot_infected_grow(states, legends, n, file="image", plt_title="Infection growth", folder="folder", save=True):
    """
    Plot the infected rate over time
    """
    x = [i for i in range(len(states[0]))]
    # plt.figure(facecolor="#505050")
    plt.figure()
    ax = plt.axes()
    ax.set_title(plt_title)
    for i, n_inf in enumerate(states):
        ax.plot(x, [y/n for y in n_inf], label=legends[i], linestyle="--", marker="o")
    # ax.set_facecolor("#505050")
    ax.set_xlabel("t")
    ax.set_ylim([0, 1])
    ax.set_ylabel("Infectious rate")
    ax.legend()
    print(f"filename: {folder}/{file}.png")
    if save:
        plt.savefig(f"{folder}/{file}.png")

def run_sis(G, beta, gamma, t_max, start_sus, start_inf):
    """
    Run a simulation of a SIS model
    """
    infs = [start_inf]
    for t in range(1, t_max + 1):
        nodes = [G.nodes[node]["state"] for node in list(G.nodes)]
        for n in G.nodes(data=False):
            if G.nodes[n]["state"] == 'V':
                continue
            if G.nodes[n]["state"] == 'I':              # if node infected 
                if np.random.rand() < gamma:            # node recover if r > Gamma
                    nodes[n] = 'S'
            else:                                       # if node not infected
                for ne in G.neighbors(n):               # for each neighbor
                    if G.nodes[ne]["state"] == 'I':     # if not infected
                        if np.random.rand() < beta:     # node become infected if r > Beta
                            nodes[n] = 'I'
                            break
        infs.append(0)
        for node, state in enumerate(nodes): # update graph and save state
            if G.nodes[node]["state"] == 'I':
                infs[t] += 1
            G.nodes[node]["state"] = state
    return infs

def run_k_sis(G, beta, gamma, t_max, start_sus, start_inf, k):
    infs = []
    mean = []
    for i in tqdm(range(k), ):
        Gc = G.copy()
        infs.append(run_sis(Gc, beta, gamma, t_max, start_sus, start_inf))
    for i in range(len(infs[0])):
        n = 0
        for j in range(len(infs)):
            n += infs[j][i]
        mean.append(n/len(infs))
    return mean

def run_fast_sis(G, beta, gamma):
    """
    Run a simulation of a SIS model
    """
    G = nx.convert_node_labels_to_integers(G)
    S = [node[0] for node in G.nodes(data=True) if node[1]["state"] == 'I']
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
        for node in nodes: # update graph and save state
            G.nodes[node[0]]["state"] = node[1]
    return inf

def run_sim(G, n_inf, n_vac, beta, gamma, t_max, file, plt_title, folder="images", k=100, cluster=False):
    n = len(list(G.nodes))
    G_pg = immun.immun_page_rank(G, n_vac)

    if cluster:
        S = add_cluster_infected(G, n_inf)
        add_cluster_infected(G_pg, n_inf)
    else:
        S = add_random_infected(G, n_inf)
        add_random_infected(G_pg, n_inf)

    G_gr, _ = gr.greedy_algorithm(G.copy(), S, n_vac, beta, gamma)

    utils.print_g_carac(G)
    print_g_sis_carac(G)
    print_g_sis_carac(G_gr, name="G_GR")
    print_g_sis_carac(G_pg, name="G_PG")

    G_states = run_k_sis(G, beta, gamma, t_max, start_sus=n-n_inf-n_vac, start_inf=n_inf, k=k)
    G_pg_states = run_k_sis(G_pg, beta, gamma, t_max, start_sus=n-n_inf-n_vac, start_inf=n_inf, k=k)
    G_gr_states = run_k_sis(G_gr, beta, gamma, t_max, start_sus=n-n_inf-n_vac, start_inf=n_inf, k=k)
    
    print(G_states)
    print(G_pg_states)
    print(G_gr_states)

    plot_infected_grow([G_states, G_pg_states, G_gr_states],
                       ["Normal", "PageRank", "Greedy"],
                       n,
                       file=file,
                       plt_title=plt_title,
                       folder=folder)