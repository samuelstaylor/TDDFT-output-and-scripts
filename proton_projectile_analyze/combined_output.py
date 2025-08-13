import pandas as pd
import re
import os
import math

def combine_velocity_data(files, velocities, output_file, latex_file):
    process_abbrev = {
        "abstraction": "A",
        "transmission": "T",
        "absorption": "P",
        "reflection": "R",
        "scattering": "S"
    }

    def round_numbers(s):
        # Round decimal numbers in strings to 2 decimals
        return re.sub(r"(\d+\.\d+)", lambda m: f"{float(m.group()):.2f}", s)

    def format_molecule(s):
        # Add subscripts: H2 -> H_2
        s = re.sub(r"([A-Za-z])(\d+)", r"\1_\2", s)
        # Convert [+x.xx] or [-x.xx] to superscript {+x.xx} or {-x.xx}
        s = re.sub(r"\[([+-]?\d*\.?\d+)\]", r"^{\1}", s)
        # Wrap letters and numbers (excluding superscripts) in \mathrm{}
        s = re.sub(r"([A-Za-z][A-Za-z0-9_]*)(\^\{[+-]?\d+\.?\d+\})?", r"\\mathrm{\1}\2", s)
        return s

    def clean_value(x):
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return "–"
        if str(x).strip() in ["-", "nan", "NaN"]:
            return "–"
        try:
            return f"{float(x):.2f}"
        except ValueError:
            return "–"

    dataframes = []

    for file, velocity in zip(files, velocities):
        if not os.path.exists(file):
            print(f"Warning: file not found {file}")
            continue

        df = pd.read_csv(file, header=None, names=["Incident Point", "Reaction", "Value", "Details"])
        df["Reaction"] = df["Reaction"].str.lower().map(process_abbrev).fillna(df["Reaction"])
        df["Value"] = df["Value"].apply(clean_value)
        df["Details"] = df["Details"].astype(str).apply(round_numbers).apply(format_molecule)

        def make_cell(row):
            return f"\\makecell{{{row['Reaction']}, {row['Value']}, \\\\ ${row['Details']}$}}"

        df["Combined"] = df.apply(make_cell, axis=1)
        df["Velocity"] = velocity
        dataframes.append(df)

    if not dataframes:
        print("No dataframes to combine.")
        return

    combined_df = pd.concat(dataframes)
    grouped = combined_df.pivot(index="Incident Point", columns="Velocity", values="Combined")

    # Save LaTeX
    with open(latex_file, "w") as f:
        f.write("\\begin{table*}[t]\n\\centering\n")
        f.write("\\begin{tabular}{|l|" + "c|" * len(velocities) + "}\n\\hline\n")
        f.write("Incident Point & " + " & ".join([f"Velocity {v}" for v in velocities]) + " \\\\\n")
        f.write("\\hline\n")
        for idx, row in grouped.iterrows():
            row_str = f"{idx} & " + " & ".join([str(row.get(v, "")) for v in velocities]) + " \\\\\n"
            f.write(row_str + "\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\caption{Combined velocity data. Each cell contains the reaction (abbreviated) and value on the first line, and molecule details on the second line.}\n")
        f.write("\\label{tab:combined_velocity_data}\n")
        f.write("\\end{table*}\n")

    # Save CSV
    combined_df.to_csv(output_file, quoting=1, quotechar='"')
    print(f"CSV saved to {output_file}")
    print(f"LaTeX table saved to {latex_file}")


# Input files and velocities
velocities = [0.1, 0.3, 0.5]
files = [f"v_{v}/output/output.csv" for v in velocities]
output_file = "combined_output.csv"
latex_file = "combined_output.tex"

# Combine the data
combine_velocity_data(files, velocities, output_file, latex_file)
