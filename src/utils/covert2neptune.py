import itertools
import random

import networkx as nx
import pandas as pd

# generate node list
f = "data/raw/nodes.graphml"
G = nx.read_graphml(f)

verticies = []
columns = [
    "~id",
    "~label",
    "labelV:String",
    "externalUserId:Int",
    "familyName:String",
    "givenName:String",
    "motherName:String",
    "DOB:String",
    "POB:String",
    "createdAt:String",
    "isActive:String",
    "systemId:String",
]

for node in G.nodes:
    attributeList = G.nodes[node]
    attributeList["~id"] = node
    attributeList["~label"] = "MyLabel"
    verticies.append(attributeList)

df_nodes = pd.DataFrame(verticies)
df_nodes.to_csv("data/processed/neptune_digest_nodes.csv", index=False, sep=",")

# generate edge list from matches
columns = ["~id", "~from", "~to", "weight:Double"]
df_match = pd.read_csv("data/raw/match.csv", skiprows=[0], names=columns)
df_match.to_csv("data/processed/edge_list.csv", index=False, sep=",")

# generate complete graph
edges = itertools.combinations(G.nodes, 2)
elist = []
i = 0
for edge in edges:
    e = {}
    e["~id"] = i
    e["~from"] = edge[0]
    e["~to"] = edge[1]
    e["~label"] = "probability"
    e["weight:Double"] = random.uniform(0, 1)
    elist.append(e)
    i += 1

df_edges = pd.DataFrame(elist)
df_edges.to_csv("data/processed/neptune_digest_edges.csv", index=False, sep=",")
