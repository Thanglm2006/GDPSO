from networkx.generators.community import LFR_benchmark_graph
import networkx as nx
import csv
mu = 1.00
n = 128
tau1 = 3
tau2 = 1.5
average_degree = 10
minCommunity = 20
seed = 10

G = LFR_benchmark_graph(n, tau1, tau2, mu, average_degree, min_community=minCommunity, seed=seed)
community={frozenset(G.nodes[v]['community']) for v in G}
print(community)
numNode=G.number_of_nodes()
numEdge=G.number_of_edges()
with open("Experimental data/synthetic networks/GN/GN-1.00/network.dat", "w") as f:
    writer = csv.writer(f,delimiter=" ")
    writer.writerow([numNode,numEdge])
    for u,v in G.edges():
        writer.writerow([u,v])
node_community = {node: list(data["community"])[0] for node, data in G.nodes(data=True)}
with open("Experimental data/synthetic networks/GN/GN-1.00/community.dat", "w") as f:
    writer = csv.writer(f,delimiter=" ")
    for node, data in G.nodes(data=True):
        writer.writerow([node, list(data["community"])[0]])