import multiprocessing
import time
import math
import numpy as np
from sklearn.metrics import normalized_mutual_info_score
import networkx as nx
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
lock = multiprocessing.Lock()
manager=multiprocessing.Manager()
found=manager.Value('b',False)
start_time=time.time()
Max_Iterations=100
population= 100
alpha=0.2
w=0.7298
c1=1.4961
c2=1.4961
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# in this code, I count the nodes from 0 to n-1
dataset='karate'
fitness_function='NMI'
with open(f'/home/thanglm2006/dataset/{dataset}.txt') as f:
    lines = f.readlines()
    tmp=lines[0].split()
    n = int(tmp[0])
    m = int(tmp[1])
    adj = np.zeros((n,n))
    degree_array = np.zeros(n)
    adj_list = [[] for i in range(n)]
    adj_list2 = [[] for i in range(n)]
    for i in range(1,len(lines)):
        tmp = lines[i].split()
        u = int(tmp[0])-1
        v = int(tmp[1])-1
        adj[u][v]=1
        adj[v][u]=1
        adj_list[u].append(v)
        adj_list[v].append(u)
        adj_list2[u].append(v)
for i in range(n):
    for j in range(n):
      degree_array[i]+=adj[i][j]
population_X=np.array([np.arange(n) for i in range(population)])
PBest=np.copy(population_X)
population_fitness=np.array([float(0.0) for i in range(population)])
PBest_fitness=np.copy(population_fitness)
population_V=np.array([np.zeros(n) for i in range(population)])
GBest=np.arange(n)
Gbest_fitness=float(-1000.0)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def fitness_calculator(tempCommunities):
    fitness=float(1/(2.0*m))
    sum=float(0.0)
    for i in range(n):
        for j in range(n):
            if tempCommunities[i]==tempCommunities[j]:
                sum+=(adj[i][j]-((degree_array[i]*degree_array[j])/(2.0*m)))
    return fitness*sum
'''''''''''''''''''''''''''this is for optimizing the fitness function'''''''''''''''''''''''''''''''''''
def fitness_calculator2(tempCommunity,originCommunity,fitness,u):
    tempFitness=float(fitness*(2.0*m))
    old_community=originCommunity[u]
    new_community=tempCommunity[u]
    for i in range(n):
        if originCommunity[i]==old_community:
            tempFitness-=2.0*(adj[i][u]-((degree_array[i]*degree_array[u])/(2.0*m)))
    for i in range(n):
        if tempCommunity[i]==new_community:
            tempFitness+=2.0*(adj[i][u]-((degree_array[i]*degree_array[u])/(2.0*m)))
    tempFitness/=(2.0*m)
    return tempFitness
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def NMI_calculator(community):
    if dataset=='karate':
        G=nx.karate_club_graph()
        true_labels = [1 if G.nodes[i]['club'] == 'Officer' else 0 for i in G.nodes()]
        return normalized_mutual_info_score(community, true_labels)
    elif dataset=='football':
        G = nx.read_gml('/home/thanglm2006/football.gml')
        true_labels = [G.nodes[node]['value'] for node in G.nodes]
        return normalized_mutual_info_score(community, true_labels)
    else:
        return 0
def reorder(tempCommunities):
    '''This is for avoiding the case that the community is the same as original community'''
    tmp=np.arange(n)
    if np.array_equal(tempCommunities,tmp):
        return tempCommunities
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    a=[[] for i in range(len(tempCommunities))]
    for i in range(len(tempCommunities)):
        a[tempCommunities[i]].append(i)
    idx=1

    for i in range(len(tempCommunities)):
        if len(a[i])==0:
            continue
        for j in a[i]:
            tempCommunities[j]=idx
        idx+=1
    return tempCommunities
NMI_calculator(population_X[0])
'''''''''''''''''''''''''''''''''''''''''''''''''''Main'''''''''''''''''''''''''''''''''''''''''''''''''''
def position_updating(i,j):
    if found.value:
        return
    ''''''''''''''''''''''''''''''''''''''''pop_v updating'''''''''''''''''''''''''''''''''''''''''
    global GBest, Gbest_fitness
    r1 = np.random.uniform(0, 1)
    r2 = np.random.uniform(0, 1)
    population_V[j] = w * population_V[j]
    v1 = (population_X[j] != PBest[j]).astype(int)
    v2 = (GBest != population_X[j]).astype(int)
    tmp1 = c1 * r1 * v1
    tmp2 = c2 * r2 * v2
    tmp3 = tmp1 + tmp2
    population_V[j] = ((population_V[j] + tmp3) >= 1).astype(int)
    '''''''''''''''''''''''''''''''''''''''' '''''''''''''''''''''''''''''''''''''''''

    ''''''''''''''''''''''''''''''''''''''''updating pop_x'''''''''''''''''''''''''''''''''''''''''
    for k in range(n):
        if population_V[j][k] == 0:
            continue
        else:
            best_finess = -999999.0
            best_communities = np.copy(population_X[j])
            for l in adj_list[k]:
                tempCommunities = np.copy(population_X[j])
                tempCommunities[k] = tempCommunities[l]
                tempFitness = NMI_calculator(tempCommunities)
                if tempFitness == 0:
                    tempFitness = fitness_calculator2(tempCommunities, population_X[j], population_fitness[j], k)
                if tempFitness > best_finess:
                    best_finess = tempFitness
                    best_communities = np.copy(tempCommunities)
            best_communities = reorder(best_communities)
            best_finess = NMI_calculator(best_communities)
            if best_finess == 0:
                best_finess = fitness_calculator2(best_communities, population_X[j], population_fitness[j], k)
            population_X[j] = np.copy(best_communities)
            population_fitness[j] = best_finess
            if best_finess > PBest_fitness[j]:
                PBest[j] = np.copy(best_communities)
                PBest_fitness[j] = best_finess
                if best_finess > Gbest_fitness:
                    Gbest_fitness = best_finess
                    GBest = np.copy(best_communities)
                    if math.isclose(best_finess, 1.0, rel_tol=1e-9) and fitness_function == 'NMI':
                        with lock:
                            if not found.value:
                                print("Iteration ", i, ": ", '\n', Gbest_fitness, " ", GBest)
                                end_time = time.time()
                                total_running_time = end_time - start_time
                                print(
                                    f"Total running time: {total_running_time:.6f} seconds or {int(total_running_time / 60)} minutes and {total_running_time % 60:.6f} seconds")
                                print("final result: ")
                                print(f"best fitness with {fitness_function} formula: ", Gbest_fitness)
                                print("number of communities: ", len(np.unique(GBest)))
                                print("communities: ", GBest)
                                found.value = True
                        return
                    Gbest_fitness = best_finess
                    GBest = np.copy(best_communities)
    '''''''''''''''''''''''''''''''''''''''' '''''''''''''''''''''''''''''''''''''''''

'''Population Initialization'''
for i in range(population):
    for j in range(int(alpha * n)):
        random_vertice = np.random.randint(0, n - 1)
        for k in adj_list[random_vertice]:
            population_X[i][k] = population_X[i][random_vertice]
    population_fitness[i] = NMI_calculator(population_X[i])
    if population_fitness[i]==0:
        fitness_function = 'Q'
        population_fitness[i]=fitness_calculator(population_X[i])


    check1=0
    check2=0
    if population_fitness[i] >= PBest_fitness[i]:
        PBest[i] = population_X[i]
        PBest_fitness[i] = population_fitness[i]
        check1=1
        if population_fitness[i] >= Gbest_fitness:
            Gbest_fitness = population_fitness[i]
            GBest = population_X[i]
            check2=1

    population_X[i]=reorder(population_X[i])
    if check1==1:
        PBest[i]=reorder(PBest[i])
    if check2==1:
        GBest=reorder(GBest)
print("Initial result: ",Gbest_fitness," ",GBest)

''''''''''''''''''''''''''''''''''''''''Main Loop'''''''''''''''''''''''''''''''''''''''''
if 1:
    with multiprocessing.Pool(processes=3) as pool:
        for i in range(Max_Iterations):
            if found.value:
                pool.terminate()
                pool.join()
                exit()
            pool.starmap(position_updating, [(i, j) for j in range(population)])
            if not found.value:
                print("Iteration ",i,": ",'\n',Gbest_fitness," ",GBest)
else:
    for i in range(Max_Iterations):
        for j in range(population):
            position_updating(i,j)
            if found.value:
                exit()
        print("Iteration ", i, ": ", '\n', Gbest_fitness, " ", GBest)
end_time=time.time()
total_running_time=end_time-start_time
print("final result: ")
print(f"best fitness with {fitness_function} formula: ",Gbest_fitness)
print("number of communities: ",len(np.unique(GBest)))
print("communities: ",GBest)
print(f"Total running time: {total_running_time:.6f} seconds or {int(total_running_time / 60)} minutes and {total_running_time % 60} seconds")
