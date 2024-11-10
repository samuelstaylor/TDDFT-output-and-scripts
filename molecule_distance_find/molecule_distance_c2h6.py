import numpy as np

# Function to calculate the center of mass of a molecule
def center_of_mass(positions, masses):
    total_mass = np.sum(masses)
    weighted_positions = np.array(positions) * np.array(masses)[:, np.newaxis]
    com = np.sum(weighted_positions, axis=0) / total_mass
    return com

# Function to calculate the distance between two points in 3D space
def distance_between_points(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

# Input positions and masses for two molecules
# Molecule 1: CH2[0][5][6]
positions_molecule_1 = [
    [-4.79386981, -0.331481466,  0.410834471],
    [-5.54653791,  0.292030538,  1.08389132],
    [-4.90714073,  0.712413610, -0.552842321]
]

masses_molecule_1 = [12.01, 1.008, 1.008]  # Example masses for C and H atoms

# Molecule 2: CH3[1][2][3][7]
positions_molecule_2 = [
    [1.24134716, -0.416652227, -0.0116468279],
    [1.09680776,  0.279193957, -1.25628331],
    [1.30802256, 0.532552143,  0.667095342],
    [1.97965121, -1.18091883, -0.181653120]
]

masses_molecule_2 = [12.01, 1.008, 1.008, 1.008]  # Example masses for C and H atoms

# Calculate the center of mass for both molecules
com_molecule_1 = center_of_mass(positions_molecule_1, masses_molecule_1)
com_molecule_2 = center_of_mass(positions_molecule_2, masses_molecule_2)

# Calculate the distance between the centers of mass
distance = distance_between_points(com_molecule_1, com_molecule_2)

# Output the results
print("Center of Mass for Molecule 1:", com_molecule_1)
print("Center of Mass for Molecule 2:", com_molecule_2)
print("Distance between the two molecules:", distance, "units")
