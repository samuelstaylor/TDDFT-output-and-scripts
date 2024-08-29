import csv
from histograms_stats_molecule_formation.fragments_stats_plots import process_fragments

fragment_charges = process_fragments('moleculeFormations.csv')

# Dictionary to store neutral molecule valence electron counts
C_valence_electrons = 4
H_electrons = 1

neutral_counts = {
    "C2":   (2 * C_valence_electrons) + (0 * H_electrons),
    "CH":   (1 * C_valence_electrons) + (1 * H_electrons),
    "C2H":  (2 * C_valence_electrons) + (1 * H_electrons),
    "C3H":  (3 * C_valence_electrons) + (1 * H_electrons),
    "C4H":  (4 * C_valence_electrons) + (1 * H_electrons),
    "CH2":  (1 * C_valence_electrons) + (2 * H_electrons),
    "C2H2": (2 * C_valence_electrons) + (2 * H_electrons),
    "C2H3": (2 * C_valence_electrons) + (3 * H_electrons),
    "C2H4": (2 * C_valence_electrons) + (4 * H_electrons),
    "C3H2": (3 * C_valence_electrons) + (2 * H_electrons),
    "C3H3": (3 * C_valence_electrons) + (3 * H_electrons),
    "C3H4": (3 * C_valence_electrons) + (4 * H_electrons),
    "C4H2": (4 * C_valence_electrons) + (2 * H_electrons),
    "C4H3": (4 * C_valence_electrons) + (3 * H_electrons),
    "C4H4": (4 * C_valence_electrons) + (4 * H_electrons),
    "C4H5": (4 * C_valence_electrons) + (5 * H_electrons),
    "C4H6": (4 * C_valence_electrons) + (6 * H_electrons)
}

# Calculate charges and store them in a dictionary
for key, array in fragment_charges.items():
    updated_values = [neutral_counts[key] - x for x in array]
    fragment_charges[key] = updated_values

# Write the dictionary contents to a CSV file
with open("charges.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in fragment_charges.items():
        row = [key] + [str(x) for x in value]  # Convert numbers to strings for CSV
        writer.writerow(row)

print("Charges written to charges.csv")
