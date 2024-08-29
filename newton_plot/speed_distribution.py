import csv
import matplotlib.pyplot as plt

# Function to read speeds from a CSV file
def read_speeds(file_path):
    speeds = {'C[0]': [], 'C[1]': [], 'H[2]': [], 'H[3]': []}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if 'Speed[A/fs]' in row:
                speeds['C[0]'].append(float(row[1]))
                speeds['C[1]'].append(float(row[2]))
                speeds['H[2]'].append(float(row[3]))
                speeds['H[3]'].append(float(row[4]))
    return speeds

# Read speeds from both quantum and classical CSV files
quantum_speeds = read_speeds('newton_plot/moleculeFormations_14.csv')
classical_speeds = read_speeds('newton_plot/atom_info.csv')

# Plot the distributions
atoms = ['C[0]', 'C[1]', 'H[2]', 'H[3]']
plt.figure(figsize=(12, 8))

for i, atom in enumerate(atoms, 1):
    plt.subplot(2, 2, i)
    plt.hist(quantum_speeds[atom], bins=30, alpha=0.5, label='Quantum', color='blue')
    plt.hist(classical_speeds[atom], bins=30, alpha=0.5, label='Classical', color='orange')
    plt.title(f'Speed Distribution for {atom}',weight='bold')
    plt.xlabel('Speed [A/fs]',weight='bold')
    plt.ylabel('Frequency',weight='bold')
    plt.legend()

plt.tight_layout()
plt.savefig(f'newton_plot/images/speed_histogram.png')
plt.show()

