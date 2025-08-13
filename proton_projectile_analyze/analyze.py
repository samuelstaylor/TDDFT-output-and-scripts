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
        - electron_densities: all numerical values from the second line.
        - final_velocity: from the velocity line corresponding to projectile_dir.
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
        fragments = fields[1:]  # Fragments are already clean (no charge fragments)

        density_fields = [field.strip() for field in lines[1].split(",") if field.strip()]
        # Extract all numerical electron densities from the second line (after "Densities")
        electron_densities = []
        for f in density_fields[1:]:  # Skip the "Densities" label
            try:
                electron_densities.append(float(f))
            except ValueError:
                # Handle cases where a density field might not be a valid number
                print(f"Warning: Non-numeric density field found: '{f}'. Skipping.")
                electron_densities.append(0.0)  # Default to 0 or handle as error

        # Ensure the number of fragments matches the number of electron densities
        if len(fragments) != len(electron_densities):
            # This is a critical mismatch, might indicate malformed input
            print(f"Warning: Mismatch between number of fragments ({len(fragments)}) and "
                  f"electron densities ({len(electron_densities)}) for chunk starting with '{incident_point_full}'. "
                  f"This chunk might be processed incorrectly.")
            # Adjust lists to match the smaller length to prevent index errors later
            min_len = min(len(fragments), len(electron_densities))
            fragments = fragments[:min_len]
            electron_densities = electron_densities[:min_len]

        mapping = {"x": 4, "y": 5, "z": 6}
        vel_line_idx = mapping[projectile_dir.lower()]
        velocity_fields = [field.strip() for field in lines[vel_line_idx].split(",") if field.strip()]
        final_velocity = float(velocity_fields[-1])

        speed_fields = [field.strip() for field in lines[7].split(",") if field.strip()]
        final_speed = float(speed_fields[-1])

        data_list.append({
            "incident_point_full": incident_point_full,
            "fragments": fragments,
            "electron_densities": electron_densities,  # Store the list of densities
            "final_velocity": final_velocity,
            "final_speed": final_speed
        })
    return data_list


def process_data(data_chunks, initial_velocity, molecule_name):
    """
    Processes the extracted data to build a mapping using incident points as keys.
    For each incident point it computes:
      - behavior: T (Transmission), R (Reflection/Scattering), Absorption, Abstraction
      - ke_loss: computed using an arbitrary function
      - fragment_products: determined by comparing fragments with molecule_name, including charges
    """

    # --- Helper Functions ---
    def calculate_ke_loss(v_initial, v_final):
        """
        Calculate kinetic energy loss using:
            ½ * m * (v_initial^2 - v_final^2)
        """
        m = 103.64269314
        return 0.5 * m * ((v_initial ** 2) - (v_final ** 2))

    def parse_formula(formula_str):
        """
        Parses a chemical formula string into a dictionary of element counts.
        Handles standard element symbols (one or two letters) and their numbers.
        Example: "C4H10" -> {'C': 4, 'H': 10}
        "H2O" -> {'H': 2, 'O': 1}
        """
        elements = {}
        # Regex to find an element symbol (one or two letters, first capitalized)
        # followed by an optional number.
        pattern = re.compile(r'([A-Z][a-z]?)(\d*)')

        # Remove any [number] notations before parsing formula
        clean_formula_str = re.sub(r'\[\d+\]', '', formula_str).strip()

        matches = pattern.finditer(clean_formula_str)

        for match in matches:
            element = match.group(1)
            count_str = match.group(2)
            count = int(count_str) if count_str else 1

            elements[element] = elements.get(element, 0) + count

        return elements

    def get_valence_electron_sum(formula_str):
        """
        Calculates the total number of valence electrons for a neutral molecule/atom
        given its chemical formula string.
        """
        VALENCE_ELECTRONS = {
            'H': 1, 'C': 4, 'N': 5, 'O': 6, 'S': 6, 'F': 7, 'Cl': 7, 'Br': 7, 'I': 7,
            # Add other common elements as needed
        }

        elements_counts = parse_formula(formula_str)
        total_valence_electrons = 0
        for element, count in elements_counts.items():
            if element in VALENCE_ELECTRONS:
                total_valence_electrons += VALENCE_ELECTRONS[element] * count
            else:
                print(
                    f"Warning: Unknown element '{element}' in formula '{formula_str}'. Assuming 0 valence electrons for it.")
        return total_valence_electrons

    def is_proton_bonded_product(fragment_name, mol_name):
        """
        Checks if a fragment name corresponds to the original molecule
        with exactly one additional hydrogen atom, based on chemical formula parsing.
        """
        mol_elements = parse_formula(mol_name)
        frag_elements = parse_formula(fragment_name)

        # Target elements: molecule's elements with H count incremented by 1
        target_elements = mol_elements.copy()
        target_elements['H'] = target_elements.get('H', 0) + 1

        # Compare frag_elements with target_elements
        # First, check if the number of unique elements is the same
        if len(frag_elements) != len(target_elements):
            return False

            # Then, iterate through target_elements and check if counts match in frag_elements
        for element, target_count in target_elements.items():
            if element not in frag_elements or frag_elements[element] != target_count:
                return False

        return True  # All checks passed

    def get_base_formula(frag_str):
        """
        Removes internal state notations like [0][1][2]... from the end of a chemical formula string.
        Example: "C4H10[0][1][4]" -> "C4H10"
        """
        return re.sub(r'\[\d+\]*', '', frag_str).strip()

    def format_fragments_with_charges(fragments_list, densities_list, original_mol_name):
        """
        Formats a list of fragments by calculating their charge and appending it in brackets.
        """
        formatted_list = []

        if not fragments_list:
            return "-"

        for i, frag in enumerate(fragments_list):
            if i < len(densities_list):
                valence_sum = get_valence_electron_sum(get_base_formula(frag))  # Use valence electrons
                density_value = densities_list[i]

                # Do NOT round the charge
                charge = valence_sum - density_value

                # Format charge to string, ensuring sign is included for positive numbers
                # Using f-string will handle decimals automatically.
                charge_str = f"{'+' if charge > 0 else ''}{charge}"
                formatted_list.append(f"{frag}[{charge_str}]")
            else:
                # Fallback if densities list is shorter than fragments list
                formatted_list.append(f"{frag}[Charge_Missing]")

        return ", ".join(formatted_list)

    # --- Main Processing Logic ---
    result_mapping = {}
    sign = lambda x: 1 if x >= 0 else -1

    for data in data_chunks:
        incident_point = data.get("incident_point_full").split("_", 2)[2]

        # Determine base behavior (Transmission or Scattering/Reflection)
        behavior_base = "R" if sign(initial_velocity) != sign(data["final_velocity"]) else "T"

        ke_loss = calculate_ke_loss(initial_velocity, data["final_speed"])

        fragments = data["fragments"]
        electron_densities = data["electron_densities"]

        behavior = behavior_base  # Default to T or R
        fragment_products_string = "-"  # Default fragment products string

        # Flag to check if H[14] (representing the free projectile proton) is present
        # This check is still crucial for primary classification to T/R.
        h14_is_fragment = "H[14]" in fragments

        # Check for proton-bonded product (e.g., C4H11 if molecule is C4H10)
        proton_bonded_product_name = None
        for frag in fragments:
            if is_proton_bonded_product(frag, molecule_name):
                proton_bonded_product_name = frag
                break

        # Get the normalized base name of the original molecule for comparison
        normalized_molecule_name = get_base_formula(molecule_name)

        # --- Decision Logic based on new rules ---

        if h14_is_fragment:
            # Rule: If H[14] is present, it means the proton did not bond to the main molecule.
            # Thus, it's a T/R event, even if other fragmentation occurred.
            behavior = behavior_base

            # List ALL fragments from the input, including H[14] and the original molecule
            # if they are explicitly present in the 'fragments' list for this chunk.
            fragments_to_display = fragments
            densities_to_display = electron_densities

            if not fragments_to_display:
                fragment_products_string = "-"
            else:
                fragment_products_string = format_fragments_with_charges(fragments_to_display, densities_to_display,
                                                                         molecule_name)

        elif proton_bonded_product_name:
            # Rule: H[14] is NOT present, but a proton-bonded product IS present.
            # We need to find the index of the proton_bonded_product_name to correctly slice densities

            if len(fragments) == 1 and fragments[0] == proton_bonded_product_name:
                # Case: Only the proton-bonded product (e.g., C4H11) is present
                # This is "Absorption" where the absorbed molecule itself is listed.
                behavior = "Absorption"
                try:
                    pb_index = fragments.index(proton_bonded_product_name)
                    fragments_to_display = [proton_bonded_product_name]
                    densities_to_display = [electron_densities[pb_index]]
                    fragment_products_string = format_fragments_with_charges(fragments_to_display, densities_to_display,
                                                                             molecule_name)
                except ValueError:  # Should not happen if proton_bonded_product_name was found
                    fragment_products_string = f"{proton_bonded_product_name}[Charge_Missing]"  # Fallback
            else:
                # Case: Proton-bonded product exists alongside other fragments (This is Abstraction)
                behavior = "Abstraction"
                # Collect fragments to display: all fragments except the original molecule and the proton-bonded product (base form)
                fragments_to_display = []
                densities_to_display = []
                for i, frag in enumerate(fragments):
                    # Condition: not the original molecule AND not the proton_bonded_product itself (based on base formula)
                    if (get_base_formula(frag) != normalized_molecule_name and
                            get_base_formula(frag) != get_base_formula(proton_bonded_product_name)):
                        fragments_to_display.append(frag)
                        if i < len(electron_densities):
                            densities_to_display.append(electron_densities[i])

                # If there are no other fragments distinct from the absorbed molecule,
                # format_fragments_with_charges will return "-".
                fragment_products_string = format_fragments_with_charges(fragments_to_display, densities_to_display,
                                                                         molecule_name)

        elif fragments and any(get_base_formula(f) != normalized_molecule_name for f in fragments):
            # Rule: H[14] is NOT present, proton_bonded_product_name is NOT present,
            # but other fragments (different from original molecule's base form) ARE present.
            # This implies the proton reacted and is likely part of one of these other fragments.
            # This is also classified as Abstraction.
            behavior = "Abstraction"
            # All fragments that are not the original molecule (base form) should be listed.
            fragments_to_display = []
            densities_to_display = []
            for i, frag in enumerate(fragments):
                if get_base_formula(frag) != normalized_molecule_name:
                    fragments_to_display.append(frag)
                    if i < len(electron_densities):
                        densities_to_display.append(electron_densities[i])

            fragment_products_string = format_fragments_with_charges(fragments_to_display, densities_to_display,
                                                                     molecule_name)

        else:
            # Default Case: No H[14], no proton-bonded product, and no other fragments
            # (meaning only original molecule or empty fragments list).
            # This means the original molecule passed through or reflected without significant reaction/fragmentation.
            behavior = behavior_base
            fragment_products_string = "-"  # Ensure "-" for T/R if only original molecule is present

        result_mapping[incident_point] = {
            "behavior": behavior,
            "ke_loss": ke_loss,
            "fragment_products": fragment_products_string
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
    # This regex now also handles the charge part [+-]\d+ and ensures it's not subscripted
    # It only targets numbers that are not immediately preceded by [+-]
    return re.sub(r'(?<![+-])(\d+)', r'$_{\1}$', text)


def export_to_latex_table(output_dir):
    """
    Reads data from output.csv in the specified output_dir and creates a LaTeX table
    code in a text file (table_latex.txt) in the same directory.
    Every row in output.csv is treated as data.
    KE loss values are rounded to 2 decimal places.
    Incident point numbers and numbers in fragment products are subscripted.
    """
    input_csv = os.path.join(output_dir, "output.csv")
    output_txt = os.path.join(output_dir, "table_latex.txt")

    # Read all rows from the CSV file
    with open(input_csv, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data_rows = list(reader)

    latex_lines = [
        r"\begin{table}[ht]",
        r"\renewcommand{\arraystretch}{0.5}",
        r"\begin{ruledtabular}",
        r"\begin{tabular}{lccc}",  # Changed from lcccc to lccc (removed electron gain column)
        r"    \textrm{Incident point} & \textrm{Effect} & \textrm{KE loss} & \textrm{Fragment products} \\",
        # Removed Electron gain header
        r"    \textrm{} & \textrm{(T/R/Abs/Abst)} & \textrm{(eV)} & \textrm{} \\",  # Removed Electron gain header
        r"    \colrule"
    ]

    # Process each data row from the CSV.
    for row in data_rows:
        # Subscript any numbers in incident points.
        incident = subscript_numbers(row[0].strip())
        effect = row[1].strip()  # This will now be T, R, Absorption, or Abstraction
        try:
            ke_loss = f"{float(row[2].strip()):.2f}"  # Index changed from 3 to 2
        except ValueError:
            ke_loss = row[2].strip()
        # Subscript any numbers in fragment products.
        frag_prod = subscript_numbers(row[3].strip()) if len(row) > 3 else ""  # Index changed from 4 to 3
        line = (r"    \textrm{\textbf{" + incident + r"}} & " +
                effect + r" & " +
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
        input_dir = input("Enter the input directory path (where moleculeFormations.csv is located): ").strip()
        # Construct the full file path
        file_path = os.path.join(input_dir, "moleculeFormations.csv")
        if os.path.isfile(file_path):
            break
        else:
            print(
                f"File '{file_path}' not found. Please ensure 'moleculeFormations.csv' exists in the specified directory.")

    while True:
        output_dir = input("Enter the output directory path: ").strip()
        # Create the directory if it doesn't exist
        try:
            os.makedirs(output_dir, exist_ok=True)
            break
        except OSError as e:
            print(f"Error creating directory {output_dir}: {e}. Please enter a valid path.")

    projectile_direction, molecule_name, initial_velocity, file_contents = read_initial_info(file_path)
    data_chunks = extract_data(file_contents, projectile_direction)
    result_mapping = process_data(data_chunks, initial_velocity, molecule_name)

    print(f"Molecule Name: {molecule_name}")
    print(f"Projectile Direction: {projectile_direction}")

    # Sort incidents using the sort_key_incident function.
    sorted_incidents = sorted(result_mapping.keys(), key=sort_key_incident)

    # Export the sorted data to a CSV file.
    # Order: Incident Point, Behavior, KE Loss (eV), Fragment Products
    output_csv = os.path.join(output_dir, "output.csv")
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for incident in sorted_incidents:
            info = result_mapping[incident]
            writer.writerow([incident, info["behavior"], info["ke_loss"],
                             info["fragment_products"]])  # Removed electron_gain

    export_to_latex_table(output_dir)  # Pass the output_dir to this function


if __name__ == '__main__':
    main()