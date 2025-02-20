#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <cmath>
#include <chrono>
#include <fstream>
#include <random>
using namespace std;
#define ll long long
#define faster ios_base::sync_with_stdio(false); cin.tie(NULL); cout.tie(NULL);
auto start = std::chrono::high_resolution_clock::now();
std::mt19937 gen(0);
std::uniform_real_distribution<> dis(0.0, 1.0);
int n,m;
const int maxIter=100;
const int popSize=100;
const double w=0.7298;
const double c1=1.4961;
const double c2=1.4961;
const double alpha=0.2;
//##############################################################################################
vector<vector<int>> adj(n,vector<int>(n,0));
vector<vector<int>> adj_list(n);
vector<int> degreeArr(n,0);
vector<int> GBest;
vector<double> PBest_Fitness, P_Fitness;
double GBest_Fitness=-1000.0;
vector<vector<int>> PBest,population_x,population_v;
//##############################################################################################
double fitnessCal(vector<int> x){
    double res=0.0;
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            if(x[i]==x[j]){
                res+=(adj[i][j]-((degreeArr[i]*degreeArr[j])/(2.0*m)));
            }
        }
    }
    return (res/(2.0*m));
}
double fitnessCal2(vector<int> tempCommunity, vector<int> x,double fitness, int u){
    double res=fitness*(2.0*m);
    int oldCommunity = x[u];
    int newCommunity = tempCommunity[u];
    for(int i=0;i<n;i++) if (x[i]==oldCommunity) res-=2.0*(adj[i][u]-((degreeArr[i]*degreeArr[u])/(2.0*m)));
    for(int i=0;i<n;i++) if (tempCommunity[i]==newCommunity) res+=2.0*(adj[i][u]-((degreeArr[i]*degreeArr[u])/(2.0*m)));;

    return (res/(2.0*m));
}
vector<int> reorder(vector<int> x){
    int check=0;
    for(int i=0;i<n;i++){
        if(x[i]!=i){
            check=1;
            break;
        }
    }
    if(!check) return x;
    vector<int> res(n);
    vector<vector<int>> comm(n);
    for(int i=0;i<n;i++){
        comm[x[i]].push_back(i);
    }
    int idx=1;
    for(int i=0;i<n;i++){
        if(comm[i].size()==0) continue;
        for(int j=0;j<comm[i].size();j++){
            res[comm[i][j]]=idx;
        }
        idx++;
    }
    return res;
}
void updateStatus(int j) {
    //####################################### update velocity #######################################
    double r1 = dis(gen);
    double r2 = dis(gen);
    vector<double> tmp(n);
    for(int k=0;k<n;k++)
        tmp[k]=population_v[j][k]*w;
    for(int k=0;k<n;k++){
        int diff1=(population_x[j][k]!=PBest[j][k])?1:0;
        int diff2=(population_x[j][k]!=GBest[k])?1:0;
        double temp1=c1*r1*diff1;
        double temp2=c2*r2*diff2;
        double sumVel=tmp[k]+temp1+temp2;
        population_v[j][k]=(sumVel>=1.0)?1:0;
    }
    //####################################### update position #######################################
    for (int k = 0; k < n; k++) {
        if (population_v[j][k] == 1) {
            double bestFitness = -999999.0;
            vector<int> bestCommunity=population_x[j];
            if(adj_list[k].empty()) continue;
            for (int l : adj_list[k]) {
                vector<int> tempCommunity = population_x[j];
                tempCommunity[k] = tempCommunity[l];
                // double tempFitness = fitnessCal2(tempCommunity, population_x[j], P_Fitness[j], k);
                double tempFitness= fitnessCal(tempCommunity);
                if (tempFitness > bestFitness) {
                    bestFitness = tempFitness;
                    bestCommunity = tempCommunity;
                }
            }
            bestCommunity = reorder(bestCommunity);
            P_Fitness[j] = bestFitness;
            population_x[j] = bestCommunity;

            if (P_Fitness[j] > PBest_Fitness[j]) {
                PBest_Fitness[j] = P_Fitness[j];
                PBest[j] = population_x[j];
                if (PBest_Fitness[j] > GBest_Fitness) {
                    GBest_Fitness = PBest_Fitness[j];
                    GBest = PBest[j];
                }
            }
        }
    }
}
void init() {
    population_x.resize(popSize,vector<int>(n,0));
    PBest.resize(popSize,vector<int>(n,0));
    population_v.resize(popSize,vector<int>(n,0));
    PBest_Fitness.resize(popSize,-99999.0);
    P_Fitness.resize(popSize,-99999.0);
    GBest.resize(n);
   for(int i=0;i<popSize;i++){
       for(int node=0;node<n;node++){
           population_x[i][node]=node;
           PBest[i][node]=node;
           population_v[i][node]=0;
       }
    }
    for(int i=0;i<popSize;i++){
        int numAlpha=static_cast<int>(alpha*n);
        for(int k=0;k<numAlpha;k++){
            int randNode=std::uniform_int_distribution<>(0,n-1)(gen);
            for(auto neigh:adj_list[randNode]){
                population_x[i][neigh]=population_x[i][randNode];
            }
        }
        population_x[i]=reorder(population_x[i]);
        double fit=fitnessCal(population_x[i]);
        P_Fitness[i]=fit;
        if(fit>=PBest_Fitness[i]){
            PBest[i]=population_x[i];
            PBest_Fitness[i]=fit;
            if(fit>GBest_Fitness){
                GBest_Fitness=fit;
                GBest=population_x[i];
            }
        }
    }
    
    return;
}
int main(){
    faster
    // string fileName="GN-0.00";
    // freopen("/home/thanglm2006/Experimental data/synthetic networks/GN/GN-0.00/network.dat","r",stdin);
    // // cin>>n>>m;
    // n=128;m=2048;
    freopen("/home/thanglm2006/dataset/football.txt", "r", stdin);
    cin>>n>>m;
    adj.resize(n,vector<int>(n,0));
    degreeArr.resize(n,0);
    adj_list.resize(n);
    for(int i=0;i<m;i++){
        int u,v;
        cin>>u>>v;
        adj[u-1][v-1]=1;
        adj[v-1][u-1]=1;
        adj_list[u-1].push_back(v-1);
        adj_list[v-1].push_back(u-1);
        degreeArr[u-1]++;
        degreeArr[v-1]++;                           
    }
    init();
    for(int i=0;i<maxIter;i++){
        for(int j=0;j<popSize;j++){
            updateStatus(j);
        }
        cout<<"Iteration "<<i<<": "<<endl;
        cout<<"GBest_Fitness: "<<GBest_Fitness<<endl;
        cout<<"GBest: ";
        for(int j=0;j<n;j++){
            cout<<GBest[j]<<" ";
        }
        cout<<endl;
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::duration<double>>(end - start);
    cout << "total time: " << duration.count() << " seconds or " << duration.count() / 60 << " minutes and " << fmod(duration.count(), 60) << " seconds." << endl;
    cout<<"GBest_Fitness: "<<GBest_Fitness<<endl;
    cout<<"community: ";
    for(int i=0;i<n;i++){
        cout<<GBest[i]<<" ";
    }
    cout<<endl;
    cout<<"number of communities: "<<*max_element(GBest.begin(),GBest.end())<<endl;
    // ofstream tableFile("GDPSO-GN-0.00.csv", ios::app);

    // tableFile << fileName<< ", "; 
    // tableFile << GBest_Fitness << ","; 
    // tableFile << duration.count() << ", ";
    // tableFile << *max_element(GBest.begin(), GBest.end()) << ", \n";    
    return 0;
}