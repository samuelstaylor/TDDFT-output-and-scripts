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
    
    def plot_linegraph(self, ax):
        ax.plot(self.time_steps[1:], self.kinetic_energies, color=self.color, linewidth=2)
        
        # Increase the number of ticks on the x-axis
        ax.locator_params(axis='x', nbins=10)
        
        ax.set_xlabel('Time (fs)', fontsize=16, fontweight='bold', fontname='Times New Roman')
        ax.set_ylabel('Kinetic Energy (eV)', fontsize=16, fontweight='bold', fontname='Times New Roman')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.xaxis.set_tick_params(labelsize=14)
        ax.yaxis.set_tick_params(labelsize=14)
        
        # Set tick label font to Times New Roman
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontname('Times New Roman')

def main():
    ke_graph = KineticEnergyGraph(elem="H", color='red', snapshot_dot_color='tab:green')
    input_file_base_path = 'k_energy_v_time/trajectory_files/excitation-angle30-2-'
    output_file_path = "k_energy_v_time/image/"
    output_file_name = "k_energy_x7.png"
    
    x_start=7
    x_end=7
    y_start=1
    y_end=1
    
    x_vals = range(x_start, x_end+1)
    y_vals = range(y_start, y_end+1)

    # Create a figure with 24 subplots (3 rows and 8 columns)
    if len(x_vals)>1:
        fig, axes = plt.subplots(len(x_vals), len(y_vals), figsize=(24, 10))  # Adjust figure size as needed
    elif len(x_vals)==1 and (y_end-y_start == 0):
        fig, axes = plt.subplots(int(len(x_vals)*2), int(len(y_vals)), figsize=(24, 10))  # Adjust figure size as needed
    else:
        fig, axes = plt.subplots(int(len(x_vals)*2), int(len(y_vals)/2), figsize=(24, 10))  # Adjust figure size as needed
        
    axes = axes.flatten()  # Flatten 2D axes array into 1D for easy iteration

   
    for i, x in enumerate(x_vals):
        for j, y in enumerate(y_vals):
            file_name = input_file_base_path + "x" + str(x) + "y" + str(y) + "/trajectory.xyz"
            print("Processing file:", file_name)
            
            # Read the trajectory, calculate velocity, and plot the kinetic energy line graph
            ke_graph.read_trajectory(file_name)
            ke_graph.calculate_velocity()
            ax = axes[i * 8 + j]  # Select the appropriate subplot
            ke_graph.plot_linegraph(ax)
            
            # Set title with subscript for x and y using subscript_numbers
            title = subscript_numbers(f'x{x}y{y}')
            ax.set_title(title, fontsize=20, fontweight='bold', fontname='Times New Roman')

    plt.tight_layout()
    plt.savefig(output_file_path + output_file_name)
    print("All line graphs plotted and saved at:", output_file_path + output_file_name)
    #plt.show()

if __name__ == "__main__":
    main()
