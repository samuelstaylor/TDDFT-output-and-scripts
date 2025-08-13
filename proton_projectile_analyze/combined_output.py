import pandas as pd
import re

def combine_velocity_data(files, velocities, output_file, latex_file=None):
    # Define a mapping for abbreviations
    process_abbreviations = {
        "abstraction": "A",
        "transmission": "T",
        "absorption": "P",
        "reflection": "R",
        "scattering": "S"
    }
    
    # Function to round numbers in a string to two decimal places
    def round_numbers_in_string(s):
        return re.sub(r"(\d+\.\d+)", lambda x: f"{float(x.group()):.2f}", s)
    
    # Function to convert molecule numbers to LaTeX subscript format
    def convert_to_subscript(s):
        return re.sub(r"([A-Za-z])(\d+)", r"\1_{\2}", s)
    
    # Function to convert bracketed values to LaTeX superscript format
    def convert_to_superscript(s):
        return re.sub(r"\[([^\]]+)\]", r"^{\1}", s)
    
    # Initialize an empty list to store DataFrames
    dataframes = []
    
    # Loop through files and velocities to read and process each file
    for file, velocity in zip(files, velocities):
        df = pd.read_csv(file, header=None, names=["Incident Point", "Reaction", "Value", "Details"])
        
        # Abbreviate the process names
        df["Reaction"] = df["Reaction"].str.lower().map(process_abbreviations).fillna(df["Reaction"])
        
        # Format numerical values to two decimal places
        df["Value"] = df["Value"].apply(lambda x: f"{float(x):.2f}" if isinstance(x, (int, float)) else x)
        
        # Round numbers in "Details", then apply subscripts, then superscripts
        df["Details"] = df["Details"].apply(round_numbers_in_string)
        df["Details"] = df["Details"].apply(convert_to_subscript)
        df["Details"] = df["Details"].apply(convert_to_superscript)
        
        # Wrap details in math mode for LaTeX
        df["Details"] = df["Details"].apply(lambda s: f"${s}$")
        
        # Add a velocity column
        df["Velocity"] = velocity
        
        # Combine the columns into a single string with thin spaces around |
        # Combine the columns into a single string with \textbar for vertical bars
        df["Combined"] = df.apply(
            lambda row: f"{row['Reaction']} \\textbar\\ {row['Value']} \\textbar\\ \\newline {row['Details']}", axis=1
        )
        dataframes.append(df)
    
    # Combine all DataFrames
    combined_df = pd.concat(dataframes)
    
    # Pivot the table to create the desired format
    grouped = combined_df.pivot(index="Incident Point", columns="Velocity", values="Combined")
    
    # Save the resulting table to a CSV file with all cells surrounded by quotes
    grouped.to_csv(output_file, quoting=1, quotechar='"')
    print(f"Combined table saved to {output_file}")
    
    # If a LaTeX file is specified, generate LaTeX table
    if latex_file:
        with open(latex_file, "w") as f:
            f.write("\\begin{table*}[t]\n")
            f.write("\\centering\n")
            f.write("\\begin{tabular}{|l|" + "c|" * len(velocities) + "}\n")
            f.write("\\hline\n")

            # Write header row
            header = "Incident Point & " + " & ".join([f"Velocity {v}" for v in velocities]) + " \\\\\n"
            f.write(header)
            f.write("\\hline\n")

            # Write data rows
            for index, row in grouped.iterrows():
                row_data = f"{index} & " + " & ".join([
                    round_numbers_in_string(str(row[v])) if not pd.isna(row[v]) else "" 
                    for v in velocities
                ]) + " \\\\\n"
                f.write(row_data)
                f.write("\\hline\n")

            f.write("\\end{tabular}\n")
            f.write("\\caption{Combined velocity data. Each cell contains the reaction (abbreviated), "
                    "value (to two decimal places), and details for the corresponding velocity.}\n")
            f.write("\\label{tab:combined_velocity_data}\n")
            f.write("\\end{table*}\n")
            print(f"LaTeX table saved to {latex_file}")


# Input files and velocities
velocities = [0.1, 0.3, 0.5]

files = []
for v in velocities:
    files.append(f"v_{v}/output/output.csv")

output_file = "combined_output.csv"
latex_file = "combined_output.tex"

# Combine the data
combine_velocity_data(files, velocities, output_file, latex_file)