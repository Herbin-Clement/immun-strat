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
    
def draw_g_sis(G, color_sus="green", color_inf="red"):
    """
    Draw the graph
    """
    cmp = []
    for _, data in G.nodes(data=True):
        if data["state"] == 'S':
            cmp.append(color_sus)
        else:
            cmp.append(color_inf)
    nx.draw(G, node_color=cmp, node_size=100, width=0.5, with_labels=len(G.nodes) < 100, font_size=7)

def plot_infected_grow(states, legends, n, file, plt_title="Infection growth", folder="folder"):
    """
    Plot the infected rate over time
    """
    x = [step["t"] for step in states[0]]
    plt.figure(facecolor="#505050")
    ax = plt.axes()
    ax.set_title(plt_title)
    for i, state in enumerate(states):
        y = [step["cur_inf"]/n for step in state]
        print(y)
        ax.plot(x, y, label=legends[i])
    ax.set_facecolor("#505050")
    ax.set_xlabel("t")
    ax.set_ylim([0, 1])
    ax.set_ylabel("Infectious rate")
    ax.legend()
    print(f"filename: {folder}/{file}.png")
    plt.savefig(f"{folder}/{file}.png")
    plt.show()

def run_sis(G, beta, gamma, t_max, start_sus, start_inf):
    """
    Run a simulation of a SIS model
    """
    sim_states = [{"t": 0, "cur_sus": start_sus, "cur_inf": start_inf}]
    for t in range(1, t_max + 1):
        sim_step_state = {"t": t, "cur_sus": 0, "cur_inf": 0, "infected": 0, "recover": 0}
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

        for node, state in enumerate(nodes): # update graph and save state
            if G.nodes[node]["state"] == 'I':
                sim_step_state["cur_inf"] += 1
            G.nodes[node]["state"] = state
        sim_states.append(sim_step_state)
    return sim_states

def run_sim(G, n_inf, n_vac, beta, gamma, t_max, file, plt_title, folder="images"):
    n = len(list(G.nodes))
    utils.print_g_carac(G)
    G_hg = immun.immun_high_degree(G, n_vac)
    G_pg = immun.immun_page_rank(G, n_vac)
    # G_bc = immun.immun_betweenness_centrality(G, n_vac)
    G_gr = immun.immun_greedy(G, n_vac, beta)

    add_random_infected(G, n_inf)
    add_random_infected(G_hg, n_inf)
    add_random_infected(G_pg, n_inf)
    # add_random_infected(G_bc, n_inf)
    add_random_infected(G_gr, n_inf)

    print_g_sis_carac(G)
    print_g_sis_carac(G_hg, name="G_HG")
    print_g_sis_carac(G_pg, name="G_PG")
    # print_g_sis_carac(G_bc, name="G_PG")
    print_g_sis_carac(G_gr, name="G_PG")

    G_states = run_sis(G, beta, gamma, t_max)
    G_hg_states = run_sis(G_hg, beta, gamma, t_max)
    G_pg_states = run_sis(G_pg, beta, gamma, t_max)
    # G_bc_states = run_sis(G_bc, beta, gamma, t_max)
    G_gr_states = run_sis(G_gr, beta, gamma, t_max)
    

    plot_infected_grow([G_states, G_hg_states, G_pg_states, G_gr_states],
                       ["Normal", "High degree", "PageRank", "Greedy"],
                       n,
                       file=file,
                       plt_title=plt_title,
                       folder=folder)


def run_sim2(G, n_inf, n_vac, beta, gamma, t_max, file, plt_title, folder="images"):
    n = len(list(G.nodes))
    utils.print_g_carac(G)
    G_hg = immun.immun_high_degree(G, n_vac)
    G_pg = immun.immun_page_rank(G, n_vac)
    # G_bc = immun.immun_betweenness_centrality(G, n_vac)

    S = add_random_infected(G, n_inf)
    add_random_infected(G_hg, n_inf)
    add_random_infected(G_pg, n_inf)
    # add_random_infected(G_bc, n_inf)
    G_gr = G.copy()
    gr.greedy_algorithm(G, S, n_vac)

    print_g_sis_carac(G)
    print_g_sis_carac(G_hg, name="G_HG")
    print_g_sis_carac(G_pg, name="G_PG")
    # print_g_sis_carac(G_bc, name="G_PG")
    print_g_sis_carac(G_gr, name="G_GR")

    G_states = run_sis(G, beta, gamma, t_max)
    G_hg_states = run_sis(G_hg, beta, gamma, t_max)
    G_pg_states = run_sis(G_pg, beta, gamma, t_max)
    # G_bc_states = run_sis(G_bc, beta, gamma, t_max)
    G_gr_states = run_sis(G_gr, beta, gamma, t_max)
    

    plot_infected_grow([G_states, G_hg_states, G_pg_states, G_gr_states],
                       ["Normal", "High degree", "PageRank", "Greedy"],
                       n,
                       file=file,
                       plt_title=plt_title,
                       folder=folder)

def run_sim3(G, n_inf, n_vac, beta, gamma, t_max, file, plt_title, folder="images"):
    n = len(list(G.nodes))
    utils.print_g_carac(G)
    G_pg = immun.immun_page_rank(G, n_vac)

    S = add_random_infected(G, n_inf)
    add_random_infected(G_pg, n_inf)
    G_gr, W = gr.greedy_algorithm(G, S, n_vac, beta, gamma)

    print_g_sis_carac(G)
    print_g_sis_carac(G_gr, name="G_GR")
    print_g_sis_carac(G_pg, name="G_PG")

    G_states = run_sis(G, beta, gamma, t_max, start_sus=n-n_inf-n_vac, start_inf=n_inf)
    G_pg_states = run_sis(G_pg, beta, gamma, t_max, start_sus=n-n_inf-n_vac, start_inf=n_inf)
    G_gr_states = run_sis(G_gr, beta, gamma, t_max, start_sus=n-n_inf-n_vac, start_inf=n_inf)
    

    plot_infected_grow([G_states, G_pg_states, G_gr_states],
                       ["Normal", "PageRank", "Greedy"],
                       n,
                       file=file,
                       plt_title=plt_title,
                       folder=folder)