import numpy as np

def rotate_vector(vector, theta, phi):
    """
    Rotate a vector by theta about y-axis, then phi about z-axis.
    Theta and phi in radians.
    """
    # Rotation matrix about y-axis (theta)
    Ry = np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

    # Rotation matrix about z-axis (phi)
    Rz = np.array([
        [np.cos(phi), -np.sin(phi), 0],
        [np.sin(phi), np.cos(phi), 0],
        [0, 0, 1]
    ])

    # Combined rotation: first Ry, then Rz
    R = Rz @ Ry

    return R @ vector

def rotate_e_field(input_file, output_file, theta_deg, phi_deg, epsilon=1e-15):
    """
    Rotates each electric field vector by theta (polar) and phi (azimuthal) angles.
    Angles in degrees. Values close to zero are set to zero using epsilon.
    """

    # Convert to radians
    theta = np.radians(theta_deg)
    phi = np.radians(phi_deg)

    # Load data
    with open(input_file, 'r') as f:
        lines = f.readlines()

    n_rows = int(lines[0].strip())
    data = np.loadtxt(lines[1:], dtype=float)

    times = data[:, 0]
    e_fields = data[:, 1:4]

    # Rotate each vector
    rotated_e_fields = np.array([rotate_vector(e, theta, phi) for e in e_fields])

    # Apply epsilon threshold to set near-zero values to zero
    rotated_e_fields[np.abs(rotated_e_fields) < epsilon] = 0.0

    # Combine and write output
    rotated_data = np.column_stack((times, rotated_e_fields))

    with open(output_file, 'w') as f:
        f.write(f"{n_rows}\n")
        for row in rotated_data:
            f.write(f"{row[0]:.8f}\t{row[1]:.8e}\t{row[2]:.8e}\t{row[3]:.8e}\n")

    print(f"Rotation complete. Output written to {output_file}")

# Example usage:
input_file = "RHCP_pulse_strong.dat"
output_file = "RHCP_pulse_rotated.dat"
rotate_e_field(input_file, output_file, theta_deg=90, phi_deg=0)