import re
import csv
import os


def read_initial_info(file_path):
    """
    Reads the first line of the file to extract:
      - projectile_direction (missing letter from the pattern after the second underscore)
      - molecule_name (prefix before the first underscore)
      - initial_velocity (user input)
      - full file contents (to process all chunks)
    """
    with open(file_path, 'r') as f:
        first_line = f.readline().strip()
        first_field = first_line.split(",")[0].strip()
        parts = first_field.split("_")
        if len(parts) < 3:
            raise ValueError("Unexpected format in first line.")

        # Extract projectile direction from the pattern after the second underscore.
        pattern_str = parts[2]
        match = re.match(r"([xyzXYZ])\d+([xyzXYZ])", pattern_str)
        if not match:
            raise ValueError("Pattern not found in first field.")
        char1 = match.group(1).lower()
        char2 = match.group(2).lower()
        missing = {'x', 'y', 'z'} - {char1, char2}
        if not missing:
            raise ValueError("Could not determine projectile direction.")
        projectile_direction = missing.pop()

        molecule_name = parts[0]
        prompt_msg = f"Input the initial {projectile_direction} velocity: "
        try:
            initial_velocity = float(input(prompt_msg))
        except ValueError:
            raise ValueError("Invalid velocity input.")

        # Read the complete file contents.
        f.seek(0)
        file_contents = f.read()

    return projectile_direction, molecule_name, initial_velocity, file_contents


def extract_data(file_contents, projectile_dir):
    """
    Extract data from file contents divided in 8-line chunks.
    For each chunk:
       - fragments: comma-separated values in the first line excluding the first entry.
       - electron_gain: value from the last entry in the second line.
       - final_velocity: from the velocity line corresponding to projectile_dir.
         Mapping: x -> line 5, y -> line 6, z -> line 7.
       - final_speed: last value in the 8th line.
    """
    data_list = []
    chunks = [chunk for chunk in file_contents.split("\n\n") if chunk.strip()]
    for chunk in chunks:
        lines = [line.strip() for line in chunk.splitlines() if line.strip()]
        if len(lines) < 8:
            continue

        fields = [field.strip() for field in lines[0].split(",") if field.strip()]
        incident_point_full = fields[0]
        fragments = fields[1:]

        density_fields = [field.strip() for field in lines[1].split(",") if field.strip()]
        electron_gain = float(density_fields[-1])

        mapping = {"x": 4, "y": 5, "z": 6}
        vel_line_idx = mapping[projectile_dir.lower()]
        velocity_fields = [field.strip() for field in lines[vel_line_idx].split(",") if field.strip()]
        final_velocity = float(velocity_fields[-1])

        speed_fields = [field.strip() for field in lines[7].split(",") if field.strip()]
        final_speed = float(speed_fields[-1])

        data_list.append({
            "incident_point_full": incident_point_full,
            "fragments": fragments,
            "electron_gain": electron_gain,
            "final_velocity": final_velocity,
            "final_speed": final_speed
        })
    return data_list


def process_data(data_chunks, initial_velocity, molecule_name):
    """
    Processes the extracted data to build a mapping using incident points as keys.
    For each incident point it computes:
      - behavior: R if sign of final_velocity differs from initial_velocity; T otherwise
      - electron_gain: value from the chunk
      - ke_loss: computed using an arbitrary function
      - fragment_products: determined by comparing fragments with molecule_name
    """

    def calculate_ke_loss(v_initial, v_final):
        """
        Calculate kinetic energy loss using:
           ½ * m * (v_initial^2 - v_final^2)
        """
        m = 103.64269314
        return 0.5 * m * ((v_initial ** 2) - (v_final ** 2))

    result_mapping = {}
    sign = lambda x: 1 if x >= 0 else -1

    for data in data_chunks:
        # Extract incident point from the first value of the first line of the chunk.
        full_field = data.get("incident_point_full")
        incident_point = full_field.split("_", 2)[2]

        # Behavior check.
        behavior = "R" if sign(initial_velocity) != sign(data["final_velocity"]) else "T"

        # Electron gain.
        electron_gain = data["electron_gain"]

        # Calculate kinetic energy loss.
        ke_loss = calculate_ke_loss(initial_velocity, data["final_speed"])

        # Process fragment_products.
        fragments = data["fragments"]
        if fragments:
            first_prefix = fragments[0].split("[")[0].strip()
            if first_prefix == molecule_name:
                fragment_products = "-"
            else:
                prod_list = []
                for frag in fragments[:-1]:
                    prod_list.append(frag.split("[")[0].strip())
                fragment_products = ", ".join(prod_list)
        else:
            fragment_products = "-"

        result_mapping[incident_point] = {
            "behavior": behavior,
            "electron_gain": electron_gain,
            "ke_loss": ke_loss,
            "fragment_products": fragment_products
        }
    return result_mapping


def sort_key_incident(incident):
    """
    Extracts numeric values from an incident string such as x0z0, x0y0, or y0z0
    and returns a tuple for sorting.
    """
    # The pattern now captures two letters (any of x, y, or z) and their numbers.
    pattern = re.search(r'([xyz])(\d+)([xyz])(\d+)', incident, re.I)
    if pattern:
        first_val = int(pattern.group(2))
        second_val = int(pattern.group(4))
        return first_val, second_val
    return float('inf'), float('inf')


def subscript_numbers(text: str) -> str:
    """
    Replace every occurrence of a number in text with a LaTeX subscript.
    E.g., 'x0z0' becomes 'x$_{0}$z$_{0}$'
    """
    return re.sub(r'(\d+)', r'$_{\1}$', text)


def export_to_latex_table():
    """
    Reads data from output.csv in the current directory and creates a LaTeX table
    code in a text file (table_latex.txt). Every row in output.csv is treated as data.
    Electron gain and KE loss values are rounded to 2 decimal places.
    Incident point numbers and numbers in fragment products are subscripted.
    """
    input_csv = os.path.join(os.getcwd(), "output.csv")
    output_txt = os.path.join(os.getcwd(), "table_latex.txt")

    # Read all rows from the CSV file
    with open(input_csv, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data_rows = list(reader)

    latex_lines = [
        r"\begin{table}[ht]",
        r"\renewcommand{\arraystretch}{0.5}",
        r"\begin{ruledtabular}",
        r"\begin{tabular}{lcccc}",
        r"    \textrm{Incident point} & \textrm{Effect} & \textrm{Electron} & \textrm{KE loss} & \textrm{Fragment products} \\",
        r"    \textrm{} & \textrm{(R/T)} & \textrm{gain} & \textrm{(eV)} & \textrm{} \\",
        r"    \colrule"
    ]

    # Process each data row from the CSV.
    for row in data_rows:
        # Subscript any numbers in incident points.
        incident = subscript_numbers(row[0].strip())
        effect = row[1].strip()
        try:
            e_gain = f"{float(row[2].strip()):.2f}"
        except ValueError:
            e_gain = row[2].strip()
        try:
            ke_loss = f"{float(row[3].strip()):.2f}"
        except ValueError:
            ke_loss = row[3].strip()
        # Subscript any numbers in fragment products.
        frag_prod = subscript_numbers(row[4].strip()) if len(row) > 4 else ""
        line = (r"    \textrm{\textbf{" + incident + r"}} & " +
                effect + r" & " + e_gain + r" & " +
                ke_loss + r" & " + frag_prod + r" \\")
        latex_lines.append(line)

    latex_lines.extend([
        r"\end{tabular}",
        r"\end{ruledtabular}",
        r"\caption{Insert caption here.}",
        r"\label{insert-label-here}",
        r"\end{table}"
    ])

    with open(output_txt, 'w') as f:
        for line in latex_lines:
            f.write(line + "\n")


def main():
    while True:
        file_path = input("Enter the input file path: ").strip()
        if os.path.isfile(file_path):
            break
        else:
            print(f"File {file_path} does not exist. Please enter a valid file path.")

    projectile_direction, molecule_name, initial_velocity, file_contents = read_initial_info(file_path)
    data_chunks = extract_data(file_contents, projectile_direction)
    result_mapping = process_data(data_chunks, initial_velocity, molecule_name)

    print(f"Molecule Name: {molecule_name}")
    print(f"Projectile Direction: {projectile_direction}")

    # Sort incidents using the sort_key_incident function.
    sorted_incidents = sorted(result_mapping.keys(), key=sort_key_incident)

    # Export the sorted data to a CSV file.
    # Order: Incident Point, Behavior, Electron Gain, KE Loss (eV), Fragment Products
    output_csv = os.path.join(os.getcwd(), "output.csv")
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for incident in sorted_incidents:
            info = result_mapping[incident]
            writer.writerow([incident, info["behavior"], info["electron_gain"], info["ke_loss"],
                             info["fragment_products"]])

    export_to_latex_table()


if __name__ == '__main__':
    main()