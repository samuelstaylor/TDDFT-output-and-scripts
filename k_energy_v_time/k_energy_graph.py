import numpy as np
import matplotlib.pyplot as plt

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
            time = float(time_line.split('=')[-1])
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
        print("  Initial speed (A/fs):", speeds[0])
        print("  Final speed (A/fs):", speeds[-1])
        self.speeds = np.array(speeds)
        self.kinetic_energies = 1/2 * self.mass * (self.speeds)**2
    
    def plot_velocity(self, output_file, snapshot_times):
        plt.figure(figsize=(10.2, 8))  # Set figure size
        plt.plot(self.time_steps[1:], self.speeds, linestyle='-', color=self.color, linewidth=2, label='Speed (A/fs)')  # Line graph
        
        # Plot green points at snapshot_times
        snapshot_indices = [i for i, t in enumerate(self.time_steps[1:]) if any(np.isclose(t, st) for st in snapshot_times)]
        plt.scatter(np.array(self.time_steps[1:])[snapshot_indices], self.speeds[snapshot_indices], color=self.snapshot_dot_color, zorder=5, s=200, edgecolor='black')
        
        plt.xlabel('Time (fs)', fontsize=30, fontweight='bold', fontname='Times New Roman')
        plt.ylabel('Velocity (Å/fs)', fontsize=30, fontweight='bold', fontname='Times New Roman', color=self.color)
        plt.xlim(left=0)  # Ensure x-axis starts at 0

        #plt.legend(fontsize=26, loc='upper right', frameon=True, labelspacing=1.2)
        
        plt.grid(True, axis='both', linestyle='--', alpha=0.7)  # Horizontal grid lines only, dashed and translucent
        plt.xticks(fontsize=24, fontname='Times New Roman')
        plt.yticks(fontsize=24, fontname='Times New Roman', color=self.color)
        plt.tight_layout()  # Adjust layout to fit labels and ticks
        plt.savefig(output_file)
        print("Speed plot generated at:", output_file)
        plt.show()
        
    def plot_kinetic_energy(self, output_file, snapshot_times):
        plt.figure(figsize=(10.2, 8))  # Set figure size
        plt.plot(self.time_steps[1:], self.kinetic_energies, linestyle='-', color=self.color, linewidth=2, label='Kinetic Energy (eV)')  # Line graph
        
        # Plot green points at snapshot_times
        snapshot_indices = [i for i, t in enumerate(self.time_steps[1:]) if any(np.isclose(t, st) for st in snapshot_times)]
        plt.scatter(np.array(self.time_steps[1:])[snapshot_indices], self.kinetic_energies[snapshot_indices], color=self.snapshot_dot_color, zorder=5, s=200, edgecolor='black')
        
        plt.xlabel('Time (fs)', fontsize=30, fontweight='bold', fontname='Times New Roman')
        plt.ylabel('Kinetic Energy (eV)', fontsize=30, fontweight='bold', fontname='Times New Roman', color=self.color)
        plt.xlim(left=0)  # Ensure x-axis starts at 0

        #plt.legend(fontsize=26, loc='upper right', frameon=True, labelspacing=1.2)
        
        plt.grid(True, axis='both', linestyle='--', alpha=0.7)  # Horizontal grid lines only, dashed and translucent
        plt.xticks(fontsize=24, fontname='Times New Roman')
        plt.yticks(fontsize=24, fontname='Times New Roman', color=self.color)
        plt.tight_layout()  # Adjust layout to fit labels and ticks
        plt.savefig(output_file)
        print("KE plot generated at:", output_file)
        plt.show()

def main():
    ke_graph = KineticEnergyGraph(elem="H", color='red', snapshot_dot_color='tab:green')
    input_file_path = 'k_energy_v_time/h_graph_traj_dens/'
    output_file_path = 'k_energy_v_time/h_graph_traj_dens/image/'

    input_file_name = 'x2y7_trajectory.xyz'
    output_speed_name = 'x2y7_speed.png'
    output_ke_name = 'x2y7_ke.png'
    
    snapshot_times = [0,20,32,36,47,56,67,76.5]

    ke_graph.read_trajectory(input_file_path + input_file_name)
    ke_graph.calculate_velocity()
    ke_graph.plot_velocity(output_file_path + output_speed_name, snapshot_times)
    ke_graph.plot_kinetic_energy(output_file_path + output_ke_name, snapshot_times)
    
if __name__ == "__main__":
    main()
