# Function to create seeds file with numbers from 1 to n
def create_seeds_file(seeds_file, n):
    with open(seeds_file, 'w') as file:
        for i in range(1, n + 1):
            file.write(f"{i}\n")
            
# Set the value of n
n = 200

# Set location and name of seeds file
seeds_file='seeds_scripts\\seeds.inp'

create_seeds_file(seeds_file, n)

print(f"Successfully generated seeds file '{seeds_file}' form 1 to {n}")