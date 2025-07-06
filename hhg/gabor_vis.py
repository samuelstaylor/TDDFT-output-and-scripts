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
    #plt.yscale('log')  # Apply logarithmic scale to the y-axis
    if max_freq is not None:
        plt.xlim(0, max_freq)
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.show()

# File paths
input_directory = "hhg/input/"
output_directory = "hhg/output/"
max_freq = 500 # Frequency [Omega] = (angular frequency × 2π)
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


### HHG SPECTRA INFO
# use logarithmic scale for y-axis
# x-axis is frequency (in a.u.) if scale = 0. y is arbitrary "absorption/energy/intensity/strength level" unit.

### SIMULATION: THINGS TO TRY/DO/SIMULATE
# try to lose no electrons with an HHG simulation. if you are losing electrons: CAP is too close or laser is too strong.
# play with different sim times. An infinitely long simulation would give very clear hhg spectrum with very sharp peaks.
# try gaussian envelope to compare

### THINGS TO LOOK FOR WHEN ANALYZING
# first peak should be freq. of laser (makes sense--electron density [and dipole] oscillates at frequency of laser.)
# first 5 to 10 peaks of harmonic spectrum should be same for different box size.
# every odd harmonic should be showing up. put vertical lines at odd harmonics
# should get even spacing and even width b/w peaks. again, if simulation ran infinitely then the peaks would be much sharper
# NOTE: add laser to the dipole figure


### EXTRA SIM: NEED TO KNOW EXCITED STATES OF ARGON
# do calculation for argon with excited states
# To do this, run a calculation with a kick instead of a laser
#    ^ ask Hamza, he knows how to do this properly
# OR we can artificially add a kick in z direction by setting the first row in the pulse.dat file as:
# <time> <E_x> <E_y> <E_z>
#  0.001   0     0     1
#  0.002   0     0     0
#  0.003   0     0     0
#   ...   ...   ...   ...
# and then the every other time step will have an E-field of 0. 
