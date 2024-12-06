import json
from matplotlib import pyplot as plt
import numpy as np

# Open and read the JSON file
with open('data.json', 'r') as file:
    data = json.load(file)


# Extract the last multiplier from each round, handling empty lists
multipliers = []

last_multipliers = [round['multipliers'][-1] for round in data['rounds'] if round['multipliers']]

last_multipliers_with_index = [
    (i, round['multipliers'][-1]) 
    for i, round in enumerate(data['rounds']) 
    if round['multipliers']
]


print(last_multipliers_with_index)

# Find the index of the round with the maximum last multiplier
max_index, max_multiplier = max(last_multipliers_with_index, key=lambda x: x[1])

treshold = 100

winning_multipliers = [
    round['multipliers'][-1] 
    for round in data['rounds'] 
    if round['multipliers'] and round['multipliers'][-1] > treshold
]

test_round = data['rounds'][24]

multipliers = test_round['multipliers']
latencies = test_round['latencies']

plt.plot(multipliers, latencies)
plt.show()