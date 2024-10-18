import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Set global font to Times New Roman
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['axes.labelsize'] = 18 # increase label font size
mpl.rcParams['xtick.labelsize'] = 14  # increase x tick font size
mpl.rcParams['ytick.labelsize'] = 14  # increase y tick font size
mpl.rcParams['legend.fontsize'] = 14  # Legend font size
# either make axis label 14, then ticks and legend 12
# or make axis label 16, then ticks and legend 14

mass_C = 1243.7123176930008  # Mass of C atom in nano units (eV_fs^2/A^2)
mass_H = 103.64269314108340  # Mass of H atom in nano units (eV_fs^2/A^2)

class AngularDistribution:
    def __init__(self, file_path, element, atom_number, data_type,alpha):
        self.file_path = file_path
        self.thetas = []
        self.kinetic_energies = []
        if element.strip().lower().startswith('c'):
            self.element = "C"
            self.mass = mass_C
            self.color = 'r'
        elif element.strip().lower().startswith('h'):
            self.element = "H"
            self.mass = mass_H
            self.color = 'b'
        self.atom_number = atom_number
        self.atom_number_sub = atom_number
        self.atom_number_to_subscript()
        self.alpha=alpha
        if data_type.strip().lower().startswith('c'):  # classical
            self.data_type = 'Classical'
        if data_type.strip().lower().startswith('s'):  # semi-classical
            self.data_type = 'Semi-classical'
        if data_type.strip().lower().startswith('q'):  # quantum
            self.data_type = 'Quantum'
        self.SHOW_LEGENDS=False

    def atom_number_to_subscript(self):
        # ₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉
        if self.atom_number == 0:
            self.atom_number_sub = '₁'
        if self.atom_number == 1:
            self.atom_number_sub = '₂'
        if self.atom_number == 2:
            self.atom_number_sub = '₁'
        if self.atom_number == 3:
            self.atom_number_sub = '₂'

    def calculate_theta(self, x_vel, y_vel, z_vel):
        speed = np.sqrt(x_vel ** 2 + y_vel ** 2 + z_vel ** 2)
        theta = np.arccos(x_vel / speed)  # Angle in radians
        theta = np.degrees(theta)  # Convert to degrees

        if x_vel < 0:
            # If y velocity component is negative, adjust theta
            if y_vel < 0:
                theta = 180 + (180 - theta)
        else:
            # If y velocity component is negative, adjust theta
            if y_vel < 0:
                theta = - theta

        return theta

    def parse_data(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith('r_seed') or line.startswith('C2H2'):
                x_vel = float(lines[i + 4].split(',')[self.atom_number + 1].strip())
                y_vel = float(lines[i + 5].split(',')[self.atom_number + 1].strip())
                z_vel = float(lines[i + 6].split(',')[self.atom_number + 1].strip())
                speed = float(lines[i + 7].split(',')[self.atom_number + 1].strip())

                theta = self.calculate_theta(x_vel, y_vel, z_vel)
                kinetic_energy = 0.5 * self.mass * speed ** 2

                self.thetas.append(theta)
                self.kinetic_energies.append(kinetic_energy)

    def plot(self, ax):
        # Ensure that LaTeX-style formatting is used correctly for subscripts in labels
        ax.scatter(self.thetas, self.kinetic_energies, marker='o', color=self.color,
                   label=f'{self.element}{self.atom_number_sub}',alpha=self.alpha)
        # Set axis labels with bold font
        ax.set_xlabel(r'θ°', fontweight='bold')
        ax.set_ylabel('Kinetic Energy (eV)', fontweight='bold')
        ax.grid(True)
        if self.SHOW_LEGENDS:
            ax.legend()
        if self.thetas[1] > -30 and self.thetas[1] < 30:
            ax.set_xlim(-15, 15) #default is (-30, 30)
        elif self.thetas[1] > 150 and self.thetas[1] < 210:
            ax.set_xlim(165, 195) #default is (150, 210)
        else:
            ax.set_xlim(-180, 180)
        if self.element=="C":
            ax.set_ylim(10, 28)
        if self.element=="H":
            ax.set_ylim(18, 36)

# Create an instance of the AngularDistribution class for all atoms
def main():
    atom_types = ['C', 'C', 'H', 'H']
   
    file_path = 'angular_distribution\\moleculeFormations_14.csv'

    data_type = 'q' # q for quantum, s for semi-classical, c for classical
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))  # Create a 2x2 grid for subplots
    #fig.suptitle(f'Angular Distribution C₂H₂ ({data_type})', fontsize=16, fontweight='bold')
    
    alpha=0.5

    for atom_number, atom_type in enumerate(atom_types):
        angular_distribution = AngularDistribution(file_path=file_path,
                                                   element=atom_type,
                                                   atom_number=atom_number,
                                                   data_type=data_type,
                                                   alpha=alpha)
        angular_distribution.parse_data()
        
        row = atom_number // 2  # Determine the row (0 or 1)
        col = atom_number % 2   # Determine the column (0 or 1)
        angular_distribution.plot(axes[row, col])  # Plot on the corresponding subplot

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make room for the title
    plt.savefig('angular_distribution/images/angular_distribution.png')
    plt.show()


if __name__ == '__main__':
    main()
