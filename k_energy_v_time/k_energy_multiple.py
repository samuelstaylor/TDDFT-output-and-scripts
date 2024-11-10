import numpy as np
import matplotlib.pyplot as plt

# Function to convert numbers to subscripted versions
def subscript_numbers(molecule):
    subscript_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return molecule.translate(subscript_map)

class KineticEnergyGraph:
    def __init__(self, elem="H", color="red", snapshot_dot_color='tab:green'):
        print("-=GENERATING KE-GRAPH=-")
        self.time_steps = None
        self.positions = None
        self.color = color
        self.snapshot_dot_color = snapshot_dot_color
        self.speeds = []
        self.kinetic_energies = []
        mass_convfactor = 1.66053886 / 1.602176487e-2
        element_num_nucleons = {"H": 1, "C": 12}
        self.mass = element_num_nucleons[elem] * mass_convfactor
        print('  Element', elem, 'mass (eV_fs^2/A^2):', self.mass)
    
    def read_trajectory(self, file_name=""):
        with open(file_name, 'r') as file:
            lines = file.readlines()
        
        data = []
        time_steps = []
        num_atoms = int(lines[0].strip())
        for i in range(0, len(lines), num_atoms + 2):
            time_line = lines[i + 1].strip()
            time = float(time_line.split('=')[1].split()[0]) / 1000  # div. by 1000 to convert iteration num to time
            time_steps.append(time)
            
            atom_data = lines[i + 2:i + 2 + num_atoms]
            atom_positions = []
            atom = atom_data[-2]  # Extract second-to-last atom
            parts = atom.split()
            x, y, z = map(float, parts[1:])
            atom_positions.append((x, y, z))
            data.append(atom_positions)
        
        self.time_steps = np.array(time_steps)
        self.positions = np.array(data)
    
    def calculate_velocity(self):
        speeds = []
        for i in range(1, len(self.time_steps)):
            dt = self.time_steps[i] - self.time_steps[i-1]
            dx = self.positions[i][0][0] - self.positions[i-1][0][0]
            dy = self.positions[i][0][1] - self.positions[i-1][0][1]
            dz = self.positions[i][0][2] - self.positions[i-1][0][2]
            speed = np.sqrt(dx**2 + dy**2 + dz**2) / dt
            speeds.append(speed)
        self.speeds = np.array(speeds)
        self.kinetic_energies = 1/2 * self.mass * (self.speeds)**2
    
    def plot_linegraph(self, ax, col):
        ax.plot(self.time_steps[1:], self.kinetic_energies, color=self.color, linewidth=2)
        
        # Set y-axis limits from 0.25 to 2.6 for each plot
        ax.set_ylim(0.0, 2.25)
        
        #for x4:
        #ax.set_ylim(0.2, 2.3)

        
        # Increase the number of ticks on the x-axis
        ax.locator_params(axis='x', nbins=10)
        
        # Remove individual axis labels
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        # Enable gridlines and make them dashed
        ax.grid(True, linestyle='--', alpha=0.7)

        # Increase tick label size
        tick_label_size = 24
        ax.tick_params(axis='both', which='major', labelsize=tick_label_size)

        # Remove the tick marks
        ax.tick_params(axis='both', which='both', length=0)  # Removes the tick marks
        
        # Set tick label font to Times New Roman
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontname('Times New Roman')
        
        # Remove y-axis tick labels for columns other than the first one
        if col != 1 and col != 5:
            ax.set_yticklabels([])  # Remove y-tick labels
            
        print("col=", col)


def main():
    ke_graph = KineticEnergyGraph(elem="H", color='red', snapshot_dot_color='tab:green')
    input_file_base_path = 'k_energy_v_time/trajectory_files/excitation-angle30-2-'
    output_file_path = "k_energy_v_time/image/"
    output_file_name = "k_energy_x3.png"
    
    x_start = 3
    x_end = 3
    y_start = 1
    y_end = 8
    
    x_vals = range(x_start, x_end + 1)
    y_vals = range(y_start, y_end + 1)

    # Create a figure with subplots, keeping the original 2x4 layout
    rows = 2
    cols = 4
    fig, axes = plt.subplots(rows, cols, figsize=(24, 10))  # Adjust figure size as needed

    # Flatten 2D axes array into 1D for easy iteration
    axes = axes.flatten()

    for i, x in enumerate(x_vals):
        for j, y in enumerate(y_vals):
            file_name = input_file_base_path + "x" + str(x) + "y" + str(y) + "/trajectory.xyz"
            print("Processing file:", file_name)
            
            # Read the trajectory, calculate velocity, and plot the kinetic energy line graph
            ke_graph.read_trajectory(file_name)
            ke_graph.calculate_velocity()
            ax = axes[i * cols + j]  # Select the appropriate subplot
            ke_graph.plot_linegraph(ax, j + 1)  # Pass the column index to plot_linegraph
            
            # Set title with subscript for x and y using subscript_numbers
            title = subscript_numbers(f'x{x}y{y}')
            ax.set_title(title, fontsize=32, fontweight='bold', fontname='Times New Roman')

    # Adjust spacing between subplots
    fig.subplots_adjust(wspace=0.1, hspace=0.2)  # Smaller wspace reduces horizontal space

    # Add common x and y labels for the entire figure
    fig.text(0.5, 0.045, 'Time (fs)', ha='center', va='center', fontsize=40, fontweight='bold', fontname='Times New Roman')
    fig.text(0.09, 0.5, 'Kinetic Energy (eV)', ha='center', va='center', rotation='vertical', fontsize=40, fontweight='bold', fontname='Times New Roman')

    #plt.tight_layout()
    plt.savefig(output_file_path + output_file_name)
    print("All line graphs plotted and saved at:", output_file_path + output_file_name)
    #plt.show()

if __name__ == "__main__":
    main()
