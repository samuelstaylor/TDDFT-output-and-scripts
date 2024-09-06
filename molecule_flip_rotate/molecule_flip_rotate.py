import numpy as np

def read_dft_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    header = lines[0].strip()
    data = []
    for line in lines[1:-1]:
        if len(line.split()) >= 3:
            print(line.split()[:3])
            data.append([float(x) for x in line.split()[:3]] + [int(x) for x in line.split()[3:]])

    footer = lines[-1].strip()

    return header, data, footer

def write_dft_file(file_path, header, data, footer):
    with open(file_path, 'w') as f:
        f.write(header + '\n')
        for atom in data:
            f.write(f"{atom[0]:10.7f} {atom[1]:10.7f} {atom[2]:10.7f} {atom[3]} {atom[4]}\n")
        f.write(footer + '\n')

def rotate_molecule(data, axis, angle):
    # Normalize the axis
    axis = np.array(axis)
    axis = axis / np.linalg.norm(axis)
    
    # Compute rotation matrix using Rodrigues' rotation formula
    angle = np.radians(angle)
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    ux, uy, uz = axis
    
    rotation_matrix = np.array([
        [cos_theta + ux**2 * (1 - cos_theta), ux*uy*(1 - cos_theta) - uz*sin_theta, ux*uz*(1 - cos_theta) + uy*sin_theta],
        [uy*ux*(1 - cos_theta) + uz*sin_theta, cos_theta + uy**2 * (1 - cos_theta), uy*uz*(1 - cos_theta) - ux*sin_theta],
        [uz*ux*(1 - cos_theta) - uy*sin_theta, uz*uy*(1 - cos_theta) + ux*sin_theta, cos_theta + uz**2 * (1 - cos_theta)]
    ])
    
    print('data: ', data)
    
    # Rotate each atom's coordinates
    for atom in data:
        atom[:3] = np.dot(rotation_matrix, atom[:3])
    
    return data

def flip_molecule(data, flip_planes):
    for plane in flip_planes:
        axis = {'x': 0, 'y': 1, 'z': 2}[plane]
        for atom in data:
            atom[axis] *= -1
    return data

# Example usage
if __name__ == "__main__":
    input_file = 'molecule_flip_rotate\c2h6_dft.inp'
    output_file = 'molecule_flip_rotate\c2h6_dft_rotated_flipped.inp'
    
    # Read the dft.inp file
    header, data, footer = read_dft_file(input_file)
    
    # Rotate the molecule 45 degrees around the z-axis
    #data = rotate_molecule(data, axis=[0, 0, 1], angle=45)
    data = rotate_molecule(data, axis=[0, 1, 0], angle=90)

    
    # Flip the molecule along the yz-plane
    #data = flip_molecule(data, flip_planes=['x'])
    
    # Write the modified data to a new dft.inp file
    write_dft_file(output_file, header, data, footer)
