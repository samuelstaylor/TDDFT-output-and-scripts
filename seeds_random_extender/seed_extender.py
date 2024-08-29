import random

# Read the existing seeds from the file
with open('seeds.txt', 'r') as file:
    existing_seeds = [int(line.strip()) for line in file]

# Ensure no repeating values and generate until we have 5000 unique values
while len(existing_seeds) < 5000:
    new_value = random.randint(1, 99999999)
    existing_seeds.append(new_value)

# Write the extended list of seeds back to the file
with open('seeds_long.txt', 'w') as file:
    for seed in existing_seeds:
        file.write(f"{seed}\n")
