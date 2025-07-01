import matplotlib.pyplot as plt
import numpy as np

def load_data(file_path, num_columns):
    """Load data from a file, skipping empty lines."""
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                columns = line.split()
                if len(columns) >= num_columns:
                    data.append([float(col) for col in columns[:num_columns]])
            except ValueError:
                # Skip lines that cannot be parsed
                continue
    return np.array(data)

def plot_data(data, title, x_label, y_label, output_file, y_columns=None, max_freq=None):
    """Plot data and save the graph."""
    plt.figure(figsize=(10, 6))
    if y_columns:
        plt.plot(data[:, 0], data[:, 1], linestyle='-', linewidth=1.0, label=f"Windowed Dipole (Column 2)")
        plt.plot(data[:, 0], data[:, 2], linestyle='--', linewidth=1.0, label=f"Dipole (Column 3)")
    else:
        plt.plot(data[:, 0], data[:, 1], linestyle='-', linewidth=1.0, label="FFT Magnitude (Column 2)")
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(x_label, fontsize=14, fontweight='bold')
    plt.ylabel(y_label, fontsize=14, fontweight='bold')
    if max_freq is not None:
        plt.xlim(0, max_freq)
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    #plt.show()

# File paths
input_directory = "hhg/input/"
output_directory = "hhg/output/"
max_freq = 300 # Frequency [Omega] = (angular frequency × 2π)
files = {
    #                                   file_path                      num_columns  y_columns
    "DP_X.DAT_C04_FFT":           (input_directory+"dp_x.dat_C04_FFT",           2,    None),
    "DP_X.DAT_C04_WINDOW":        (input_directory+"dp_x.dat_C04_WINDOW",        3,    [1, 2]),
    "DP_X.DAT_C04_FFT_NO_WINDOW": (input_directory+"dp_x.dat_C04_FFT_NO_WINDOW", 2,    None)
}

# Plot each file
for title, (file_path, num_columns, y_columns) in files.items():
    data = load_data(file_path, num_columns)
    if y_columns:
        plot_data(data, title, "Time [fs] (Column 1)", "Dipole", output_directory+f"{title}.png", y_columns)
    else:
        plot_data(data, title, "Frequency (Column 1)", "FFT Magnitude (Column 2)", output_directory+f"{title}.png", y_columns,max_freq= max_freq)
