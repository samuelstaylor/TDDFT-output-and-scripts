# Script for reformatting XYZ files for VisIt — floating-point, aligned columns

def reformat_xyz(input_file: str, output_file: str, precision: int = 9, width: int = 13):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    output_lines = []
    i = 0
    while i < len(lines):
        # Read number of atoms
        num_atoms_line = lines[i].strip()
        try:
            num_atoms = int(num_atoms_line)
        except ValueError:
            i += 1
            continue

        # Read comment line
        comment_line = lines[i + 1].strip()
        comment = comment_line if comment_line.startswith("#") else "Converted from trajectory.xyz"

        # Read atom lines
        atom_lines = lines[i + 2:i + 2 + num_atoms]
        atom_data = []
        for line in atom_lines:
            parts = line.strip().split()
            if len(parts) != 4:
                continue
            element, x, y, z = parts
            x_float = float(x)
            y_float = float(y)
            z_float = float(z)

            # Right-align float columns with consistent width
            formatted_line = (
                f"{element:<2} "
                f"{x_float:>{width}.{precision}f} "
                f"{y_float:>{width}.{precision}f} "
                f"{z_float:>{width}.{precision}f}"
            )
            atom_data.append(formatted_line)

        # Append to output
        output_lines.append(str(num_atoms))
        output_lines.append(comment)
        output_lines.extend(atom_data)

        i += 2 + num_atoms

    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))


def main():
    # Adjust filenames and formatting settings as needed
    reformat_xyz("trajectory.xyz", "trajectory_reformatted.xyz", precision=9, width=13)


if __name__ == '__main__':
    main()
