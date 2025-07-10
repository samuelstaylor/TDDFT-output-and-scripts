# script for reformatting XYZ files for VisIt

def reformat_xyz(input_file: str, output_file: str):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    output_lines = []
    i = 0
    while i < len(lines):
        # Parse atom count
        num_atoms_line = lines[i].strip()
        try:
            num_atoms = int(num_atoms_line)
        except ValueError:
            i += 1
            continue

        # Parse comment line
        comment_line = lines[i + 1].strip()
        comment = comment_line if comment_line.startswith("#") else "Converted from trajectory.xyz"

        # Parse atom data
        atom_lines = lines[i + 2:i + 2 + num_atoms]
        atom_data = []
        for line in atom_lines:
            parts = line.strip().split()
            if len(parts) != 4:
                continue
            element, x, y, z = parts
            atom_data.append(f"{element:<2}{x:>20}{y:>20}{z:>20}")

        # Append reformatted block
        output_lines.append(f"{num_atoms}")
        output_lines.append(comment)
        output_lines.extend(atom_data)

        i += 2 + num_atoms

    # Write to output without extra blank lines
    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))


def main():
    # change this accordingly
    reformat_xyz("trajectory.xyz", "trajectory_reformatted.xyz")


if __name__ == '__main__':
    main()