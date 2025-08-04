import math

def rotate_about_z(x, y, angle_rad):
    """Rotate point (x, y) counterclockwise about the z-axis by angle in radians."""
    x_rot = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    y_rot = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    return x_rot, y_rot

def rotate(filename="dft.inp", output_filename="rotated_dft.inp"):
    with open(filename, 'r') as f:
        lines = f.readlines()

    angle_rad = math.radians(45)
    header = lines[0].strip()
    rotated_lines = [header + "\n"]

    for line in lines[1:]:
        # Skip empty lines or lines without at least 5 entries
        if line.strip() == "" or len(line.split()) < 5:
            rotated_lines.append(line)
            continue

        parts = line.split()
        try:
            x, y, z = map(float, parts[:3])
            rest = parts[3:]
        except ValueError:
            # If line doesn't contain floats in the first three entries, skip rotation
            rotated_lines.append(line)
            continue

        x_rot, y_rot = rotate_about_z(x, y, angle_rad)
        new_line = f"{x_rot: >14.10f} {y_rot: >14.10f} {z: >14.10f} {' '.join(rest)}\n"
        rotated_lines.append(new_line)

    with open(output_filename, 'w') as f_out:
        f_out.writelines(rotated_lines)

if __name__ == "__main__":
    rotate()
