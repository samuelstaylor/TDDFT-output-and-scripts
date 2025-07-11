# script for reformatting XYZ files for VisIt

def reformat_xyz(input_file: str, output_file: str):
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
            # Exactly one space between columns, no formatting
            atom_data.append(f"{element} {x} {y} {z}")

        # Append to output
        output_lines.append(str(num_atoms))
        output_lines.append(comment)
        output_lines.extend(atom_data)

        i += 2 + num_atoms

    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))


def main():
    # change this accordingly
    reformat_xyz("trajectory.xyz", "trajectory_reformatted.xyz")


if __name__ == '__main__':
    main()