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
        return re.sub(r"(\d+\.\d+)", lambda m: f"{float(m.group()):.2f}", s)

    def format_molecule(s):
        s = re.sub(r"([A-Za-z])(\d+)", r"\1_\2", s)  # subscripts
        s = re.sub(r"\[([+-]?\d*\.?\d+)\]", r"^{\1}", s)  # superscripts
        s = re.sub(r"([A-Za-z][A-Za-z0-9_]*)(\^\{[+-]?\d+\.?\d+\})?",
                   r"\\mathrm{\1}\2", s)  # wrap in \mathrm{}
        return s

    def clean_value(x):
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return "--"
        if str(x).strip() in ["-", "nan", "NaN"]:
            return "--"
        try:
            return f"{float(x):.2f}"
        except ValueError:
            return "--"

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
            molecules = [m.strip() for m in row['Details'].split(",") if m.strip()]
            molecules_latex = " \\\\ ".join([f"${mol}$" for mol in molecules])
            if molecules_latex:
                return f"\\makecell{{{row['Reaction']}, {row['Value']} \\\\ {molecules_latex}}}"
            else:
                return f"\\makecell{{{row['Reaction']}, {row['Value']}}}"

        df["Combined"] = df.apply(make_cell, axis=1)
        df["Velocity"] = velocity
        dataframes.append(df)

    if not dataframes:
        print("No dataframes to combine.")
        return

    combined_df = pd.concat(dataframes)
    grouped = combined_df.pivot(index="Incident Point", columns="Velocity", values="Combined")

    with open(latex_file, "w") as f:
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\renewcommand{\\arraystretch}{1.2}\n")
        f.write("\\setcellgapes{2pt}\\makegapedcells\n")
        f.write("\\begin{tabular}{l" + "c" * len(velocities) + "}\n")
        f.write("\\toprule\n")
        f.write("\\makecell{\\textbf{Impact Point (IP)}\\\\\\textit{Projectile Velocity (\\AA/fs)}} & " +
                " & ".join([f"\\textbf{{{v}}}" for v in velocities]) + " \\\\\n")
        f.write("\\midrule\n")
        f.write("\\arrayrulecolor[gray]{0.75}\n")
        for idx, row in grouped.iterrows():
            row_str = f"\\textbf{{IP {idx}}} & " + " & ".join([str(row.get(v, "")) for v in velocities]) + " \\\\\n"
            f.write(row_str)
            f.write("\\midrule\n")
        f.write("\\arrayrulecolor{black}\n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\caption{Combined velocity data for different impact points (rows) and projectile velocities (columns). Each cell shows the reaction type (A: abstraction, S: scattering, P: absorption), followed by a value and the resulting fragment charges.}\n")
        f.write("\\label{tab:combined_velocity_data}\n")
        f.write("\\end{table*}\n")

    combined_df.to_csv(output_file, quoting=1, quotechar='"')
    print(f"CSV saved to {output_file}")
    print(f"LaTeX table saved to {latex_file}")


# Inputs
velocities = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3]
molecule_name = "C2H2"
molecule_name = "C3H8"
files = [molecule_name+f"/v_{v}/output/output.csv" for v in velocities]
output_file = molecule_name+"/combined_output.csv"
latex_file = molecule_name+"/combined_output.tex"

combine_velocity_data(files, velocities, output_file, latex_file)
