#pr 53
import networkx as nx
import random
import matplotlib.pyplot as plt

# Set the random seed
random.seed(10)

# Generate an Erdös-Rényi graph with 10000 nodes and 100000 edges
G1 = nx.gnm_random_graph(10000, 100000)

# Generate a preferential attachment graph with 10000 nodes and out-degree 10
G2 = nx.barabasi_albert_graph(10000, 10)

# Assign node attributes based on the last digit of node ID
for node in G1.nodes():
    last_digit = node % 10
    if last_digit in [0, 2, 4, 6]:
        G1.nodes[node]['support'] = 'you'
    elif last_digit in [1, 3, 5, 7]:
        G1.nodes[node]['support'] = 'rival'
    else:
        G1.nodes[node]['support'] = 'undecided'

for node in G2.nodes():
    last_digit = node % 10
    if last_digit in [0, 2, 4, 6]:
        G2.nodes[node]['support'] = 'you'
    elif last_digit in [1, 3, 5, 7]:
        G2.nodes[node]['support'] = 'rival'
    else:
        G2.nodes[node]['support'] = 'undecided'


def simulate_election(graph, k):
    you_votes = 0
    rival_votes = 0
    high_rollers = sorted(graph.degree(), key=lambda x: (-x[1], x[0]))[:1000]
    high_roller_nodes = [node for node, _ in high_rollers]

    for node in graph.nodes():
        support = graph.nodes[node]['support']
        if support == 'you':
            if node in high_roller_nodes:
                you_votes += 1
            elif random.random() < 0.4 + k/10000:
                you_votes += 1
            else:
                rival_votes += 1
        elif support == 'rival':
            if node in high_roller_nodes:
                rival_votes += 1
            elif random.random() < 0.4 - k/10000:
                rival_votes += 1
            else:
                you_votes += 1
        else:
            if node in high_roller_nodes:
                you_votes += 1
            elif random.random() < 0.5:
                you_votes += 1
            else:
                rival_votes += 1
    return you_votes - rival_votes

# Define the range of values for k
ks = range(1000, 10000, 1000)

# Simulate the election for each value of k for both graphs
results1 = [simulate_election(G1, k) for k in ks]
results2 = [simulate_election(G2, k) for k in ks]

# Plot the results
plt.plot(ks, results1, label='Erdös-Rényi')
plt.plot(ks, results2, label='Preferential attachment')
plt.legend()
plt.xlabel('Amount spent on ads (Rs. k)')
plt.ylabel('Number of votes you win by')
plt.show()

# Find the minimum amount needed to win the election for each graph
min_amount1 = ks[results1.index(max(results1))]
min_amount2 = ks[results2.index(max(results2))]

print("Minimum amount to win the election in Erdös-Rényi graph:", min_amount1)
print("Minimum amount to win the election in Preferential attachment graph:", min_amount2)
