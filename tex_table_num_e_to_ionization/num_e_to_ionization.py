#!/usr/bin/env python3
import re

input_file = "num_electrons.tex"
output_file = "num_electrons_lost.tex"

# neutral valence electrons for each element
neutral = {"C": 4, "H": 1, "N": 5}

# total neutral valence electrons for C4H4N2
neutral_total = 30.0

# regex to find numbers like 3.51 or 4
number_pattern = re.compile(r"(?<![A-Za-z])(\d+\.\d+|\d+)(?![A-Za-z])")

# helper to strip trailing \\ and LaTeX commands from a cell for parsing
def clean_cell(cell):
    # remove \\ at end, remove \midrule \hline etc for parsing number/dash
    cell = cell.strip()
    # remove trailing \\ (maybe with spaces)
    cell = re.sub(r"\\\\\s*$", "", cell)
    # remove trailing \midrule, \toprule, \bottomrule appearing in same cell
    cell = re.sub(r"\\(midrule|toprule|bottomrule)\s*$", "", cell)
    return cell.strip()

# read file
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

output_lines = []
col_count = None
header_labels = None  # will be list like ["IP","Geom","C1",...,"Total"]

# detect header row to extract atom labels (this is robust to spacing)
for i, line in enumerate(lines):
    if "\\textbf{IP}" in line and "C1" in line:
        # try to split header on & and extract the plain text inside \textbf{...}
        parts = [p.strip() for p in re.split(r"\s*&\s*", line.rstrip())]
        header_labels = []
        for p in parts:
            # extract content inside \textbf{...} if present, otherwise raw text
            m = re.search(r"\\textbf\{([^}]*)\}", p)
            if m:
                header_labels.append(m.group(1).strip())
            else:
                # remove braces and whitespace
                header_labels.append(re.sub(r"[{}]", "", p).strip())
        col_count = len(header_labels)
        break

# Fallback if header not found: assume 13 columns and fixed header_labels
if header_labels is None:
    col_count = 13
    header_labels = ["IP", "Geom", "C1", "C2", "C3", "C4",
                     "H1", "H2", "H3", "H4", "N1", "N2", "Total"]

# Determine indexes for atom columns (all columns between the Geom column and the Total column)
# Find index of 'Total' in header_labels if present
try:
    total_idx = header_labels.index("Total")
except ValueError:
    total_idx = col_count - 1

# Atom columns are those between index 2 and total_idx-1 (common case)
atom_start = 2
atom_end = total_idx  # exclusive
atom_indices = list(range(atom_start, atom_end))
atom_labels = []
for idx in atom_indices:
    if idx < len(header_labels):
        atom_labels.append(header_labels[idx])
    else:
        # fallback label
        atom_labels.append(f"col{idx}")

# Now process lines
for line in lines:
    # if this line doesn't look like a table row, keep as-is
    if "&" not in line or "\\" not in line:
        output_lines.append(line)
        continue

    # split into cells (keep LaTeX spacing tolerant)
    parts = [p for p in re.split(r"\s*&\s*", line.rstrip())]

    # if the row doesn't have expected number of columns, leave as-is
    if len(parts) < col_count:
        output_lines.append(line)
        continue

    # clean copies for parsing
    parts_clean = [clean_cell(p) for p in parts]

    # skip header row (leave unchanged)
    if "\\textbf{IP}" in line:
        output_lines.append(line)
        continue

    # track how many neutral electrons to SUBTRACT from the total because of \textemdash atoms
    dash_subtract = 0.0

    # ---- Convert atom columns ----
    for idx, atom_label in zip(atom_indices, atom_labels):
        cell = parts_clean[idx]
        original_cell = parts[idx]

        # if the cell contains a \textemdash (anywhere), treat as missing atom
        if r"\textemdash" in cell:
            # find element letter (first char of atom_label, e.g., 'C' from 'C1')
            el = atom_label.strip()[0] if atom_label else None
            if el in neutral:
                dash_subtract += float(neutral[el])
            # leave the atom column unchanged (keep \textemdash)
            continue

        # otherwise, if there is a numeric value, convert it to electrons lost for that atom
        m = number_pattern.search(cell)
        if m:
            original_num = m.group(1)
            el = atom_label.strip()[0] if atom_label else None
            if el in neutral:
                lost = float(neutral[el]) - float(original_num)
                # format with two decimals, but preserve any trailing LaTeX in the original cell
                new_num = f"{lost:.2f}"
                # replace only the numeric substring (first occurrence)
                parts[idx] = original_cell.replace(original_num, new_num, 1)
            else:
                # not an element we know; leave as-is
                pass

    # ---- Convert Total column ----
    total_cell = parts_clean[total_idx]
    original_total_cell = parts[total_idx]

    # if total cell contains a number, adjust by subtracting neutral electrons for dashed atoms
    m_total = number_pattern.search(total_cell)
    if m_total:
        total_val = float(m_total.group(1))
        # SUBTRACT the neutral electrons corresponding to dashed atoms (user request)
        adjusted_total = total_val - dash_subtract
        # electrons lost = neutral_total - adjusted_total
        electrons_lost_total = neutral_total - adjusted_total
        parts[total_idx] = original_total_cell.replace(m_total.group(1),
                                                       f"{electrons_lost_total:.2f}", 1)
    else:
        # no numeric total (maybe \textemdash) -> leave unchanged
        pass

    # reassemble row preserving spacing and trailing chars
    new_line = " & ".join(parts)
    output_lines.append(new_line + "\n")

# write output
with open(output_file, "w", encoding="utf-8") as f:
    f.write("".join(output_lines))

print(f"Converted table written to {output_file}")
