import os
import csv
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parent
CHARGE_DIR = BASE / "charge_stats"

# Convert en dashes to \textendash in labels
def dash(s):
    return s.replace("–", r"\textendash ")

ROW_ORDER = [
    ("c",       "Orthogonal", dash("C")),
    ("c_xy",    "Planar",     dash("C")),
    ("n",       "Orthogonal", dash("N")),
    ("n_xy",    "Planar",     dash("N")),
    ("cc",      "Orthogonal", dash("C–C")),
    ("cc_xy",   "Planar",     dash("C–C")),
    ("cn",      "Orthogonal", dash("C–N")),
    ("cn_xy",   "Planar",     dash("C–N")),
    ("nn",      "Orthogonal", dash("N–N")),
    ("nn_xy",   "Planar",     dash("N–N")),
    ("center",  "Orthogonal", dash("Center")),
    ("h_xy",    "Planar",     dash("H")),
    ("mean_orth", "Orthogonal", "Mean"),
    ("mean_plan", "Planar", "Mean"),
    ("mean_all",  "All", "Mean")
]

IP_LABELS = {
    "c": "C",
    "c_xy": "C",
    "n": "N",
    "n_xy": "N",
    "cc": dash("C–C"),
    "cc_xy": dash("C–C"),
    "cn": dash("C–N"),
    "cn_xy": dash("C–N"),
    "nn": dash("N–N"),
    "nn_xy": dash("N–N"),
    "center": "Center",
    "h_xy": "H"
}


def read_charge_csv(path):
    with open(path, "r") as f:
        lines = [l.strip() for l in f.readlines()]

    density_line = next(l for l in lines if l.startswith("Densities"))
    parts = density_line.split(",")[1:]
    densities = [float(x) for x in parts if x.strip() != ""]
    return densities[:10]


def compute_means(rows):
    """Compute means excluding values that round to 0.00."""
    arr = np.array([r[2:] for r in rows])

    def filt_mean(values):
        cleaned = [v for v in values if round(v, 2) != 0.00]
        return round(float(np.mean(cleaned)), 2) if cleaned else 0.00

    orth = [r for r in rows if r[1] == "Orthogonal"]
    plan = [r for r in rows if r[1] == "Planar"]

    def col_means(subrows):
        if not subrows:
            return [0.00] * 11
        cols = list(zip(*[r[2:] for r in subrows]))
        return [filt_mean(col) for col in cols]

    return col_means(orth), col_means(plan), col_means(rows)


def fmt(x):
    """Format numeric entries: 2 decimals, but if rounds to 0 → \textemdash."""
    if round(x, 2) == 0.00:
        return r"\textemdash"
    return f"{x:.2f}"


def main():
    rows = []

    for dirname in os.listdir(CHARGE_DIR):
        subdir = CHARGE_DIR / dirname
        if not subdir.is_dir():
            continue

        csv_path = subdir / "charge_stats.csv"
        if not csv_path.exists():
            continue

        geometry = "Planar" if dirname.endswith("xy") else "Orthogonal"
        ip = IP_LABELS.get(dirname, dirname)

        vals = read_charge_csv(csv_path)

        N1, N2 = vals[0], vals[1]
        C1, C2, C3, C4 = vals[2], vals[3], vals[4], vals[5]
        H1, H2, H3, H4 = vals[6], vals[7], vals[8], vals[9]
        total = sum([N1, N2, C1, C2, C3, C4, H1, H2, H3, H4])

        rows.append([
            ip, geometry,
            C1, C2, C3, C4,
            H1, H2, H3, H4,
            N1, N2,
            total
        ])

    # append means
    mean_orth, mean_plan, mean_all = compute_means(rows)
    rows.append(["Mean", "Orthogonal"] + mean_orth)
    rows.append(["Mean", "Planar"] + mean_plan)
    rows.append(["Mean", "All"] + mean_all)

    # reorder rows
    ordered_rows = []
    for key, geom, label in ROW_ORDER:
        for r in rows:
            if r[0] == label and r[1] == geom:
                ordered_rows.append(r)

    # build LaTeX table
    latex_output = ""

    def add(line):
        nonlocal latex_output
        latex_output += line + "\n"

    add(r"\begin{table*}[t]")
    add(r"\centering")
    add(r"\renewcommand{\arraystretch}{1.25}")
    add(r"\setcellgapes{3pt}\makegapedcells")
    add("")
    add(r"\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l l c c c c c c c c c c c}")
    add(r"\toprule")
    add(r"\textbf{IP} &")
    add(r"\textbf{Geom.} &")
    add(r"\textbf{C\textsubscript{1}} & \textbf{C\textsubscript{2}} & "
        r"\textbf{C\textsubscript{3}} & \textbf{C\textsubscript{4}} & "
        r"\textbf{H\textsubscript{1}} & \textbf{H\textsubscript{2}} & "
        r"\textbf{H\textsubscript{3}} & \textbf{H\textsubscript{4}} & "
        r"\textbf{N\textsubscript{1}} & \textbf{N\textsubscript{2}} & "
        r"\textbf{Total} \\")
    add(r"\midrule")
    add(r"\arrayrulecolor[gray]{0.75}")

    for r in ordered_rows:
        ip, geom = r[0], r[1]
        nums = [fmt(x) for x in r[2:]]
        add(f"\\textbf{{{ip}}} & {geom} & " + " & ".join(nums) + r" \\")
        add(r"\midrule")

    add(r"\arrayrulecolor{black}")
    add(r"\bottomrule")
    add(r"\end{tabular*}")
    add("")
    add(r"\caption{Caption.}")
    add(r"\label{tab:number-electrons}")
    add(r"\end{table*}")

    # print to terminal
    print(latex_output)

    # save to table.tex
    with open(BASE / "table.tex", "w") as f:
        f.write(latex_output)

    print("\n[Saved output to table.tex]\n")


if __name__ == "__main__":
    main()
