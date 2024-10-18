import csv
import matplotlib.pyplot as plt
import matplotlib as mpl

class AtomSpeedPlotter:
    def __init__(self, num_carbons, num_hydrogens, classical_file, quantum_file, output_file):
        self.num_carbons = num_carbons
        self.num_hydrogens = num_hydrogens
        self.atom_labels = self.generate_atom_labels()
        self.classical_file = classical_file
        self.quantum_file = quantum_file
        self.output_file = output_file
        
        self.setup_plot_params()

    # Set global plot parameters
    def setup_plot_params(self):
        mpl.rcParams['font.family'] = 'Times New Roman'
        mpl.rcParams['font.weight'] = 'bold'
        mpl.rcParams['axes.labelweight'] = 'bold'
        mpl.rcParams['axes.labelsize'] = 18  # Increase label font size
        mpl.rcParams['xtick.labelsize'] = 14  # Increase x tick font size
        mpl.rcParams['ytick.labelsize'] = 14  # Increase y tick font size
        mpl.rcParams['legend.fontsize'] = 14  # Legend font size

    # Generate atom labels based on user input
    def generate_atom_labels(self):
        labels = {}
        for i in range(self.num_carbons):
            labels[f'C[{i}]'] = []
        for i in range(self.num_hydrogens):
            labels[f'H[{i + self.num_carbons}]'] = []
        return labels

    # Read speeds from a CSV file
    def read_speeds(self, file_path):
        speeds = {label: [] for label in self.atom_labels}
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if 'Speed[A/fs]' in row:
                    for i, label in enumerate(self.atom_labels):
                        speeds[label].append(float(row[i + 1]))  # Start from the second column for speeds
        return speeds

    # Format labels with subscripts
    def format_label(self, atom_label):
        # ₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉
        if '[' in atom_label and ']' in atom_label:
            base, subscript = atom_label.split('[')
            subscript = subscript.replace(']', '')
            if subscript == '0':
                return f'{base}₁'
            if subscript == '1':
                return f'{base}₂'
            if subscript == '2':
                return f'{base}₁'
            if subscript == '3':
                return f'{base}₂'
        return atom_label

    # Plot the distributions
    def plot_speeds(self, num_rows, num_cols):
        quantum_speeds = self.read_speeds(self.quantum_file)
        classical_speeds = self.read_speeds(self.classical_file)
        
        plt.figure(figsize=(14, 5))  # Adjust the figure size to match a 2x7 grid
        for i, atom in enumerate(self.atom_labels, 1):
            plt.subplot(num_rows, num_cols, i)  # Create a grid for subplots
            plt.hist(quantum_speeds[atom], bins=30, alpha=0.5, label='Quantum', color='blue')
            plt.hist(classical_speeds[atom], bins=30, alpha=0.5, label='Classical', color='orange')
            formatted_label = self.format_label(atom)
            plt.title(f'{formatted_label}', weight='bold', fontsize=20)
            plt.xlabel('Speed [Å/fs]', weight='bold')
            plt.ylabel('Frequency', weight='bold')
            plt.legend()

        plt.tight_layout()
        plt.savefig(self.output_file)
        plt.show()

# Example of how to use the class
if __name__ == "__main__":
    num_carbons = 2  # Adjust this for different molecules
    num_hydrogens = 2  # Adjust this for different molecules
    classical_file = 'speed_distribution\\atom_info.csv'
    quantum_file = 'speed_distribution\\moleculeFormations_14.csv'
    output_file = 'speed_distribution/images/speed_histogram.png'

    plotter = AtomSpeedPlotter(num_carbons, num_hydrogens, classical_file, quantum_file, output_file)
    plotter.plot_speeds(num_rows=2, num_cols=2)
