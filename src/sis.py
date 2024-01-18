import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

def generate_barabasi_albert_graph(n, m, seed):
    """
    Generate B(n,m) Barabasi-Albert model
    """
    G = nx.barabasi_albert_graph(n, m, seed)
    for node in G.nodes(data=False):
        G.nodes[node]["state"] = "S"
    return G

def generate_erdos_renyi_graph(n, p, seed):
    G = nx.erdos_renyi_graph(n, p, seed)
    for node in G.nodes(data=False):
        G.nodes[node]["state"] = "S"
    return G

def generate_complete_graph(n):
    G = nx.complete_graph(n)
    for node in G.nodes(data=False):
        G.nodes[node]["state"] = "S"
    return G

def add_random_infected(G, n):
    for node in random.sample(list(G.nodes), n):
        G.nodes[node]["state"] = 'I'

def print_g_sis_carac(G):
    """
    Print differents caracteristic for SIS model
    """
    susceptible = 0
    infected = 0
    vaccinated=0
    for _, data in G.nodes(data=True):
        if data["state"] == 'S':
            susceptible += 1
        elif data["state"] == 'I':
            infected += 1
        elif data["state"] == 'V':
            vaccinated+=1    
    print(f"G has {susceptible} suceptibles nodes, {infected} infected nodes {vaccinated} vaccinated nodes")
    
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

def print_state(states):
    for state in states:
        print(state)

def plot_infected_grow(states, n, title="Infection growth"):
    x = [step["t"] for step in states]
    y = [step["cur_inf"]/n for step in states]
    plt.figure(facecolor="#505050")
    ax = plt.axes()
    ax.set_title(title)
    ax.plot(x, y, color="orange")
    ax.set_facecolor("#505050")
    ax.set_xlabel("t")
    ax.set_ylim([0, 1])
    ax.set_ylabel("Infectious rate")
    plt.show()

def run_sis(G, beta, gamma, t_max):
    sim_states = []
    for t in range(1, t_max + 1):
        sim_step_state = {"t": t, "cur_sus": 0, "cur_inf": 0, "infected": 0, "recover":0}
        nodes = [G.nodes[node]["state"] for node in list(G.nodes)]
        for n in G.nodes(data=False):
            if G.nodes[n]["state"] == 'V': 
                continue
            if G.nodes[n]["state"] == 'I':              # if node infected 
                if np.random.rand() < gamma:            # node recover if r > Gamma
                    nodes[n] = 'S'
                    # G.nodes[n]["state"] = 'S'
            else:                                       # if node not infected
                for ne in G.neighbors(n):               # for each neighbor
                    if G.nodes[ne]["state"] == 'I':     # if not infected
                        if np.random.rand() < beta:     # node become infected if r > Beta
                            nodes[n] = 'I'
                            # G.nodes[ne]["state"] = 'I'
                            break

        for node, state in enumerate(nodes): # update graph and save state
            if G.nodes[node]["state"] == 'S':
                sim_step_state["cur_sus"] += 1
                if state == 'I':
                    sim_step_state["infected"] += 1
            else:
                sim_step_state["cur_inf"] += 1
                if state == 'S':
                    sim_step_state["recover"] += 1
            G.nodes[node]["state"] = state
        sim_states.append(sim_step_state)
    return sim_states



def vaccinate_greedy(G, num_to_vaccinate, beta):
    vaccinated_nodes = set()
    while len(vaccinated_nodes) < num_to_vaccinate:
        node_impacts = {node: sum(beta for neighbor in G.neighbors(node) if G.nodes[neighbor]['state'] == 'I') for node in G.nodes() if G.nodes[node]['state'] != 'V'}
        node_to_vaccinate = max(node_impacts, key=node_impacts.get)
        vaccinated_nodes.add(node_to_vaccinate)
        G.nodes[node_to_vaccinate]['state'] = 'V'

def vaccinate_by_degree(G, num_to_vaccinate):
    degrees = G.degree()
    top_nodes = sorted(degrees, key=lambda x: x[1], reverse=True)[:num_to_vaccinate]
    for node, _ in top_nodes:
        G.nodes[node]['state'] = 'V'

def vaccinate_by_betweenness_centrality(G, num_to_vaccinate):
    centrality = nx.betweenness_centrality(G)
    top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:num_to_vaccinate]
    for node, _ in top_nodes:
        G.nodes[node]['state'] = 'V'

def vaccinate_by_pagerank(G, num_to_vaccinate):
    pagerank = nx.pagerank(G)
    top_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:num_to_vaccinate]
    for node, _ in top_nodes:
        G.nodes[node]['state'] = 'V'
