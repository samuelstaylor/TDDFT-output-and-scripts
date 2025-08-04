# dft-to-traj.py

dft_file = r"trajectory.xyz-to-dft.inp\dft\cyclopentane-dft-18-z.inp"
xyz_file = r"trajectory.xyz-to-dft.inp\trajectory\cyclopentane-trajectory-18-z.xyz"

# Mapping of atomic numbers to element symbols
ELEMENTS = {
    1: "H",
    6: "C",
    7: "N",
    8: "O",
}

def convert_dft_to_xyz(dft_file, xyz_file):
    with open(dft_file, 'r') as dft, open(xyz_file, 'w') as xyz:
        # Read the number of atoms
        num_atoms_line = dft.readline().strip()
        num_atoms = int(num_atoms_line.split()[0])
        
        # Write the number of atoms and a comment line to the XYZ file
        xyz.write(f"{num_atoms}\n")
        xyz.write(" # iter =     0  time[fs]= 0.00000\n")
        
        # Process each atom line
        for _ in range(num_atoms):
            line = dft.readline().strip().split()
            while line == "":
                print("skipping empty line after number of atoms:", dft.readline().strip())
                line = dft.readline().strip().split()
            x, y, z, atomic_number = float(line[0]), float(line[1]), float(line[2]), int(line[3])
            element = ELEMENTS[atomic_number]
            xyz.write(f"{element} {x:.10f} {y:.10f} {z:.10f}\n")


convert_dft_to_xyz(dft_file, xyz_file)