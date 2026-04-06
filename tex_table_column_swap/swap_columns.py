import re

# Column mapping (1-indexed → new order)
mapping = [1,2,6,4,3,5,10,8,7,9,11,12,13]
# NEW ORDERING IN TERMS OF OLD ORDERING ^

def reorder_row(row):
    """Reorder columns in a LaTeX table row."""
    # Split by '&', but keep LaTeX formatting intact
    cols = [c.strip() for c in row.split('&')]

    # Check if row looks like a data row (has numbers or dashes)
    if len(cols) < 13:
        return row  # Leave formatting lines untouched

    # Apply mapping (convert to 0-index)
    new_cols = [cols[i-1] for i in mapping]

    return " & ".join(new_cols) + " \\\\"

def process_table(infile="table.tex", outfile="table_reordered.tex"):
    with open(infile, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # Match lines ending with "\\" that are likely table rows
        if "&" in line and line.strip().endswith("\\\\"):
            new_lines.append(reorder_row(line))
        else:
            new_lines.append(line)

    with open(outfile, "w") as f:
        f.writelines(new_lines)

    print(f"Done! Wrote reordered table to {outfile}")


if __name__ == "__main__":
    process_table()
