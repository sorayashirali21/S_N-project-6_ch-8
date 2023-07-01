pr 54
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def decide_support_with_thresholds(graph, voter_support, thresholds):
    new_voter_support = voter_support.copy()

    for node in graph.nodes:
        neighbors = list(graph.neighbors(node))
        num_support_you = sum([1 for neighbor in neighbors if voter_support[neighbor] == 'You'])
        num_support_rival = sum([1 for neighbor in neighbors if voter_support[neighbor] == 'Rival'])
        threshold = thresholds[node]

        if num_support_you >= threshold:
            new_voter_support[node] = 'You'
        elif num_support_rival > threshold:
            new_voter_support[node] = 'Rival'

    return new_voter_support


def count_votes(voter_support):
    num_you_votes = sum([1 for support in voter_support.values() if support == 'You'])
    num_rival_votes = sum([1 for support in voter_support.values() if support == 'Rival'])
    return num_you_votes, num_rival_votes


def simulate_dinner_effect(graph, initial_voter_support, max_budget):
    x_values = np.arange(1000, max_budget + 1, 1000)
    y_values = []

    for budget in x_values:
        persuaded_voters = set()

        for node in graph.nodes:
            if 3000 <= node <= 3099:
                persuaded_voters.add(node)

        # new_voter_support = initial_voter_support.copy()
        new_voter_support = voter_support.copy()

        for node in persuaded_voters:
            new_voter_support[node] = 'You'

        for day in range(1, 11):
            # new_voter_support = decide_support_with_thresholds(graph, new_voter_support, T)
            # new_voter_support = decide_support_with_thresholds(graph, new_voter_support, thresholds)
            new_voter_support = decide_support_with_thresholds(graph, new_voter_support, T)

        num_you_votes, num_rival_votes = count_votes(new_voter_support)
        y_values.append(num_you_votes - num_rival_votes)

    return x_values, y_values


erdos_renyi_graph = nx.gnm_random_graph(10000, 100000, seed=10)

voter_support_erdos_renyi = {node: 'Undecided' for node in erdos_renyi_graph.nodes}

num_you_votes, num_rival_votes = count_votes(voter_support_erdos_renyi)

print("Initial Votes - Erdos-Renyi Graph:")
print("You:", num_you_votes)
print("Rival:", num_rival_votes)

preferential_attachment_graph = nx.barabasi_albert_graph(10000, 10, seed=10)

voter_support_preferential = {node: 'Undecided' for node in preferential_attachment_graph.nodes}

num_you_votes, num_rival_votes = count_votes(voter_support_preferential)

print("\nInitial Votes - Preferential Attachment Graph:")
print("You:", num_you_votes)
print("Rival:", num_rival_votes)

# T = [1, 1, 1, 1, 1, 4, 1, 0, 4, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 4, 0, 1, 4, 0, 1, 1, 1, 4, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 4, 1, 1, 4, 1, 4, 0, 1, 0, 1, 1, 1, 0, 4, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 4, 0, 4, 0, 0, 1, 1, 1, 4, 0, 4, 0]
T = [1] * 10000

x_values, y_values_erdos_renyi = simulate_dinner_effect(erdos_renyi_graph, voter_support_erdos_renyi, 9000)

x_values, y_values_preferential = simulate_dinner_effect(preferential_attachment_graph, voter_support_preferential,
                                                         9000)

plt.plot(x_values, y_values_erdos_renyi, label='Erdos-Renyi Graph')
plt.plot(x_values, y_values_preferential, label='Preferential Attachment Graph')
plt.xlabel('Budget (Rs. k)')
plt.ylabel('Votes Won (You - Rival)')
plt.legend()
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt


def simulate_rioting(thresholds):
    n = len(thresholds)
    state = [0] * n
    for i in range(n):
        if state[i] == 0:
            if sum(state[j] >= thresholds[j] for j in range(n)) >= thresholds[i]:
                state[i] = 1
    return sum(state)


# Define the vector of thresholds
T = [1, 1, 1, 1, 1, 4, 1, 0, 4, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 4, 0, 1, 4, 0, 1, 1, 1,
     4, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 4, 1, 1, 4, 1, 4, 0, 1, 0, 1, 1,
     1, 0, 4, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 4, 0, 4, 0, 0, 1, 1, 1,
     4, 0, 4, 0]

# Simulate the rioting behavior 1000 times and store the results in a histogram
results = [simulate_rioting(T) for _ in range(1000)]
n = len(T)
hist, bins = np.histogram(results, bins=np.arange(n + 2))

# Plot the histogram
plt.bar(range(n + 1), hist, align='center')
plt.xticks(range(n + 1))
plt.xlabel('Number of individuals with threshold k')
plt.ylabel('Number of simulations with that result')
plt.show()
