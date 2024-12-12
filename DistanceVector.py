# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 18:44:59 2024

@author: luca
"""
import networkx as nx
import random
import time
import matplotlib.pyplot as plt

#inizializza le tabelle di routing con le distanze dai vicini e le altre ad infinito
def initialise_route_tab():
    routing_tables = {}
    for node in G.nodes():
        routing_tab = {}
        for target in G.nodes():
            if(target == node):
                routing_tab[target] = {}  
                routing_tab[target]['weight'] = 0
                routing_tab[target]['nexHop'] = ''
            elif(G.has_edge(node, target)):
                routing_tab[target] = {}
                routing_tab[target]['weight'] = G[node][target]['weight']
                routing_tab[target]['nextHop'] = target
            else:
                routing_tab[target] = {}
                routing_tab[target]['weight'] = float('inf')
                routing_tab[target]['nextHop'] = ''
        routing_tables[node] = routing_tab
    return routing_tables
        
#Aggiorna le tabelle di routing  
def update_routing_tab():
    changes = False
    for node in G.nodes():
        for neightbour in G.neighbors(node):
            for target in G.nodes():
                #Se la nuova distanza è minore di quella presente la cambia
                if(routing_tables[node][target]['weight'] > routing_tables[neightbour][target]['weight'] + routing_tables[node][neightbour]['weight']):
                    routing_tables[node][target]['weight'] = routing_tables[neightbour][target]['weight'] + routing_tables[node][neightbour]['weight']
                    routing_tables[node][target]['nextHop'] = neightbour
                    changes = True;
    #ritorna vero tutte le volte che viene eseguito almeno un cambiamento
    return changes
    
#Restituisce le tabelle come stringa
def tables_to_string():
    table_str = ""
    for node in G.nodes:
        table_str += f"Tabella di {node}:\n"
        table_str += str(routing_tables[node]) + "\n\n"
    return table_str

#Ritorna la tabella come lista di liste
def tabels_to_list():
    data = [['', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    for source in G.nodes():
        temp = [source]
        for target in G.nodes():
            temp.append(routing_tables[source][target])
        data.append(temp)
    return data
    
    
#Verifica che te tabele risultanti siano corrette
def verify_tables():
    print("\nverifica in corso")
    for source in G.nodes():
        for target in G.nodes():
            #compara il risultato con quello della funzione dijkstra_path_length
            if(nx.dijkstra_path_length(G, source, target) != routing_tables[source][target]['weight']):
                print("distanza sbagliata", nx.dijkstra_path_length(G, source, target), "!=" , routing_tables[source][target]['weight'])
    print("verifica completata")          

G = nx.Graph()

num_nodes = 10
probability = 0.2

G = nx.erdos_renyi_graph(n=num_nodes, p=probability)

while True:
    #Crea un grafo casuale con 10 nodi
    G = nx.erdos_renyi_graph(n=num_nodes, p=probability)

    # Aggiunge dei pesi casuali agli archi appena creati
    for (u, v) in G.edges():
        G[u][v]['weight'] = random.randint(1, 10)  # Pesi casuali tra 1 e 10
    #verifica che il grafo sia connesso    
    if(nx.is_connected(G)):
        break
    
routing_tables = initialise_route_tab()

print("\Tabelle iniziali\n")
print(tables_to_string())

#Fa aggiornare le tabelle ogni 2 secondi fino a che non ci sono più cambiamenti
changes = True
while update_routing_tab():
    print("\nAggiornamento\n")
    print(tables_to_string())
    time.sleep(2)

#Divide la pagina in 2 righe
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 10))

# Disegna il grafo
pos = nx.spring_layout(G)  # Layout per il posizionamento dei nodi
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=8, ax=ax1)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, ax=ax1)

data = tabels_to_list()

#Stampa le tabelli finali
ax2.axis('off')
table = ax2.table(cellText=data[1:], colLabels=data[0], loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1.2, 1.2)
verify_tables()

# Mostra il grafo
plt.show()


    