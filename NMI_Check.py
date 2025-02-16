# from sklearn.metrics import normalized_mutual_info_score
# import networkx as nx
#
#
# print("test result: ")
# G = nx.karate_club_graph()
# true_labels = [1 if G.nodes[i]['club'] == 'Officer' else 0 for i in G.nodes()]
# community=[1, 1, 1, 1 ,1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1 ,1, 2, 1, 2, 1, 2, 2, 2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ,2 ]
# print(normalized_mutual_info_score(community, true_labels))