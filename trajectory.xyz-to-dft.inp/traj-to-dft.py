# traj-to-dft.py

input_file = r"trajectory.xyz-to-dft.inp\trajectory\cyclopentane-trajectory.xyz"
output_file= r"trajectory.xyz-to-dft.inp\dft\cyclopentane-dft.inp"
input_file = r"trajectory.xyz-to-dft.inp\trajectory\pentane-trajectory.xyz"
output_file= r"trajectory.xyz-to-dft.inp\dft\pentane-dft.inp"
grid_step = 0.3
n_grid_points = (100, 100, 100)

# Mapping of element symbols to atomic numbers
ELEMENTS = {
    "H": 1,
    "C": 6,
    "N": 7,
    "O": 8,
}

def convert_xyz_to_dft(xyz_file, dft_file, grid_step=0.3, n_grid_points=(100, 100, 100)):
    with open(xyz_file, 'r') as xyz, open(dft_file, 'w') as dft:
        # Read number of atoms
        num_atoms = int(xyz.readline().strip())
        xyz.readline()  # Skip the comment line

        # Write the number of atoms and three zeros
        dft.write(f"{num_atoms} 0 0 0\n\n")

        # Process each atom line
        for _ in range(num_atoms):
            line = xyz.readline().strip().split()
            element, x, y, z = line[0], float(line[1]), float(line[2]), float(line[3])
            atomic_number = ELEMENTS[element]
            # the number 1 at the end is boolean for "moveable. 1 means true"
            dft.write(f"{x: .10f} {y: .10f} {z: .10f} {atomic_number} 1\n")

        # Write the grid step and grid points
        dft.write(f"\n{grid_step} {n_grid_points[0]} {n_grid_points[1]} {n_grid_points[2]}\n")

# MAIN
convert_xyz_to_dft(input_file, output_file, grid_step, n_grid_points)