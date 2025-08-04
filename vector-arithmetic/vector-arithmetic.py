import numpy as np
'''
### GIVE THIS PROGRAM A VECTOR LIKE THE ONE BELOW:
vector = np.array([3, 4, 5])  
# Replace with your vector
''' 

# CALCULATE DISPLACEMENT VECTOR
r1 = np.array([-1.0693121949,  -0.6658553809,   0.2484739279])
r2 = np.array([-0.9859572843,   0.7894078088,  -0.2384276029])

# displacement vector
vector = r2 - r1  # Calculate the difference between two vectors

def vector_info(vector):
    # Calculate the magnitude of the vector
    magnitude = np.linalg.norm(vector)
    
    # Normalize the vector to get the unit vector
    unit_vector = vector / magnitude if magnitude != 0 else np.zeros(3)
    
    # Angles with the x, y, and z axes
    angle_x = np.degrees(np.arccos(unit_vector[0])) if magnitude != 0 else None
    angle_y = np.degrees(np.arccos(unit_vector[1])) if magnitude != 0 else None
    angle_z = np.degrees(np.arccos(unit_vector[2])) if magnitude != 0 else None
    
    # Angles from the xy, xz, and yz planes
    angle_xy = np.degrees(np.arccos(np.dot(unit_vector, [0, 0, 1]))) if magnitude != 0 else None
    angle_xz = np.degrees(np.arccos(np.dot(unit_vector, [0, 1, 0]))) if magnitude != 0 else None
    angle_yz = np.degrees(np.arccos(np.dot(unit_vector, [1, 0, 0]))) if magnitude != 0 else None
    
    # Print the results
    print(f"Vector: {vector}")
    print(f"Magnitude: {magnitude:.4f}")
    print(f"Angle with x-axis: {angle_x:.4f} degrees")
    print(f"Angle with y-axis: {angle_y:.4f} degrees")
    print(f"Angle with z-axis: {angle_z:.4f} degrees")
    print(f"Angle from xy-plane: {angle_xy:.4f} degrees")
    print(f"Angle from xz-plane: {angle_xz:.4f} degrees")
    print(f"Angle from yz-plane: {angle_yz:.4f} degrees")

# Example usage
if __name__ == "__main__":
    vector_info(vector)
    print('magic num =', 90 - 86.8908)