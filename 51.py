#pr 51
import networkx as nx
import random

# Generate an Erdős-Rényi graph with 10000 nodes and 100000 edges
G1 = nx.gnm_random_graph(10000, 100000, seed=10)

# Generate a preferential attachment graph with 10000 nodes and out-degree 10
G2 = nx.barabasi_albert_graph(10000, 10, seed=10)



# Assign voter support based on the last digit of the node ID
for node in G1.nodes:
    last_digit = node % 10
    if last_digit in [0, 2, 4, 6]:
        G1.nodes[node]['support'] = 'you'
    elif last_digit in [1, 3, 5, 7]:
        G1.nodes[node]['support'] = 'rival'
    else:
        G1.nodes[node]['support'] = 'undecided'

for node in G2.nodes:
    last_digit = node % 10
    if last_digit in [0, 2, 4, 6]:
        G2.nodes[node]['support'] = 'you'
    elif last_digit in [1, 3, 5, 7]:
        G2.nodes[node]['support'] = 'rival'
    else:
        G2.nodes[node]['support'] = 'undecided'


# Set the initial support of the decided voters
for node in G1.nodes:
    if G1.nodes[node]['support'] == 'you':
        G1.nodes[node]['initial_support'] = 0.4
    elif G1.nodes[node]['support'] == 'rival':
        G1.nodes[node]['initial_support'] = 0.4
    else:
        G1.nodes[node]['initial_support'] = 0.2

for node in G2.nodes:
    if G2.nodes[node]['support'] == 'you':
        G2.nodes[node]['initial_support'] = 0.4
    elif G2.nodes[node]['support'] == 'rival':
        G2.nodes[node]['initial_support'] = 0.4
    else:
        G2.nodes[node]['initial_support'] = 0.2

# Simulate the election process for 10 days
for day in range(1, 11):
    # Update the support of the undecided voters based on the preferences of their neighbors
    for node in G1.nodes:
        if G1.nodes[node]['support'] == 'undecided':
            neighbor_support = [G1.nodes[neighbor]['initial_support'] for neighbor in G1.neighbors(node)]
            if neighbor_support.count(0.4) > neighbor_support.count(0.6):
                G1.nodes[node]['support'] = 'you'
            elif neighbor_support.count(0.4) < neighbor_support.count(0.6):
                G1.nodes[node]['support'] = 'rival'
            else:
                G1.nodes[node]['support'] = random.choice(['you', 'rival'])

    for node in G2.nodes:
        if G2.nodes[node]['support'] == 'undecided':
            neighbor_support = [G2.nodes[neighbor]['initial_support'] for neighbor in G2.neighbors(node)]
            if neighbor_support.count(0.4) > neighbor_support.count(0.6):
                G2.nodes[node]['support'] = 'you'
            elif neighbor_support.count(0.4) < neighbor_support.count(0.6):
                G2.nodes[node]['support'] = 'rival'
            else:
                G2.nodes[node]['support'] = random.choice(['you', 'rival'])


    # Print the support of each candidate on this day
    you_support1 = sum([G1.nodes[node]['initial_support'] for node in G1.nodes if G1.nodes[node]['support'] == 'you'])
    rival_support1 = sum(
        [G1.nodes[node]['initial_support'] for node in G1.nodes if G1.nodes[node]['support'] == 'rival'])
    you_support2 = sum([G2.nodes[node]['initial_support'] for node in G2.nodes if G2.nodes[node]['support'] == 'you'])
    rival_support2 = sum(
        [G2.nodes[node]['initial_support'] for node in G2.nodes if G2.nodes[node]['support'] == 'rival'])
    print(f"Day {day}: You - {you_support1 + you_support2:.2%}, Rival - {rival_support1 + rival_support2:.2%}")

# Count the votes on the election day
you_votes1 = sum([1 for node in G1.nodes if G1.nodes[node]['support'] == 'you'])
rival_votes1 = sum([1 for node in G1.nodes if G1.nodes[node]['support'] == 'rival'])
you_votes2 = sum([1 for node in G2.nodes if G2.nodes[node]['support'] == 'you'])
rival_votes2 = sum([1 for node in G2.nodes if G2.nodes[node]['support'] == 'rival'])

# Print the result of the election
if you_votes1 + you_votes2 > rival_votes1 + rival_votes2:
    print("You win!")
elif you_votes1 + you_votes2 < rival_votes1 + rival_votes2:
    print("Rival wins!")
else:
    print("It's a tie!")

import networkx as nx
import numpy as np

np.random.seed(10)

n = 10000
m = 100000
erdos_renyi_graph = nx.gnm_random_graph(n, m)

preferential_attachment_graph = nx.barabasi_albert_graph(n, 10)

voter_support = {}
for node in erdos_renyi_graph.nodes:
    last_digit = node % 10
    if last_digit in [0, 2, 4, 6]:
        voter_support[node] = 'You'
    elif last_digit in [1, 3, 5, 7]:
        voter_support[node] = 'Rival'
    else:
        voter_support[node] = 'Undecided'


def decide_support(graph, voter_support):
    updated_support = voter_support.copy()
    for node in graph.nodes:
        neighbors = list(graph.neighbors(node))
        neighbor_support = [voter_support[neighbor] for neighbor in neighbors]
        support_counts = {
            'You': neighbor_support.count('You'),
            'Rival': neighbor_support.count('Rival')
        }
        if support_counts['You'] > support_counts['Rival']:
            updated_support[node] = 'You'
        elif support_counts['Rival'] > support_counts['You']:
            updated_support[node] = 'Rival'
        else:
            num_ties = neighbor_support.count('Undecided')
            if num_ties % 2 == 0:
                updated_support[node] = 'You'
            else:
                updated_support[node] = 'Rival'
    return updated_support


for day in range(1, 11):
    voter_support = decide_support(preferential_attachment_graph, voter_support)

num_support_you = list(voter_support.values()).count('You')
num_support_rival = list(voter_support.values()).count('Rival')

if num_support_you > num_support_rival:
    election_result = 'You win the election!'
elif num_support_rival > num_support_you:
    election_result = 'Your rival wins the election!'
else:
    election_result = 'It\'s a tie!'

print(election_result)
