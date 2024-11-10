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
# Molecule 1: C2H[0][2][6]
positions_molecule_1 = [
    [-1.41961165, 0.0714071828, 1.12141185],
    [-1.51142721, -0.111672987, -.266641466],
    [-0.843684944, -0.507911786, -1.24405605]
]

masses_molecule_1 = [12.01, 12.01, 1.008]  # Example masses for C and H atoms

# Molecule 2: CH2[1][3][5]
positions_molecule_2 = [
    [3.50944358, 0.0749120040, 2.05040093],
    [4.38244074, 0.425556309, 2.93406511],
    [3.03197303, -0.566355394,  1.11287617]
]

masses_molecule_2 = [12.01, 1.008, 1.008]  # Example masses for C and H atoms

# Calculate the center of mass for both molecules
com_molecule_1 = center_of_mass(positions_molecule_1, masses_molecule_1)
com_molecule_2 = center_of_mass(positions_molecule_2, masses_molecule_2)

# Calculate the distance between the centers of mass
distance = distance_between_points(com_molecule_1, com_molecule_2)

# Output the results
print("Center of Mass for Molecule 1:", com_molecule_1)
print("Center of Mass for Molecule 2:", com_molecule_2)
print("Distance between the two molecules:", distance, "units")
