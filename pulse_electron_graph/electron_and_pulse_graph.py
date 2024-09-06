import matplotlib.pyplot as plt

'''
info_input_file  = "_FIGURES/CE_theory_paper/C3H8_7.5_traj_dens/C3H8_7.50_r47_info.txt"
pulse_input_file = "_FIGURES/CE_theory_paper/C3H8_7.5_traj_dens/pulse_7.5.dat"
output_file      = "_FIGURES/CE_theory_paper/C3H8_7.5_traj_dens/C3H8_7.5_r47_info.png"
'''
info_input_file  = "_FIGURES/CE_theory_paper/C4H10_7.5_traj_dens/C4H10_7.5_r4_info.txt"
pulse_input_file = "_FIGURES/CE_theory_paper/C4H10_7.5_traj_dens/pulse_7.5.dat"
output_file      = "_FIGURES/CE_theory_paper/C4H10_7.5_traj_dens/C4H10_7.5_r4_info.png"

pulse_color = 'tab:blue'
electron_color = 'tab:green'
add_vertical_lines = True
vertical_line_color = "#D3B3E5"
verticle_lines=[18.5,20.5,30,45,80,120]

# Enable LaTeX for rendering text
plt.rcParams['font.family'] = 'Times New Roman'

# Lists to store data
time_info = []
electron_num = []
time_pulse = []
values_pulse = []

# Read info.txt
with open(info_input_file, 'r') as file:
    for line in file:
        parts = line.split()
        time_info.append(float(parts[1]))
        electron_num.append(float(parts[2]))

# Read pulse.dat
with open(pulse_input_file, 'r') as file:
    data_points_added = 0
    for line in file:
        parts = line.split()
        if len(parts) > 1:
            if float(parts[0]) > 120:
                break
            time_pulse.append(float(parts[0]))
            values_pulse.append(float(parts[1]))

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 8))

# Plot the first dataset
ax1.set_xlabel('Time (fs)', fontsize=24, weight='bold')
ax1.plot(time_pulse, values_pulse, color=pulse_color, label='Electric Field', alpha=0.75,linewidth=2.5)
ax1.tick_params(axis='y', labelcolor=pulse_color, which='both', direction='in', width=2, length=6, labelsize=20)
ax1.tick_params(axis='x', labelsize=20, which='both', direction='in', width=2, length=6)  # Increase and bold x tick labels
ax1.set_ylabel('Electric Field (V/Å)', color=pulse_color, fontsize=24, weight='bold')

# Create a second y-axis
ax2 = ax1.twinx()
ax2.set_ylabel('Number of Electrons', color=electron_color, fontsize=24, weight='bold')
ax2.plot(time_info, electron_num, color=electron_color, label='Number of electrons',linewidth=2.5)
ax2.tick_params(axis='y', labelcolor=electron_color, which='both', direction='in', width=2, length=6, labelsize=20)

# Add vertical lines
if add_vertical_lines:
    for line_x_loc in verticle_lines:
        ax2.axvline(x=line_x_loc, color=vertical_line_color, linewidth=1,linestyle="--")
        
fig.tight_layout()
#plt.title('Electric Field and Number of Electrons in Butane', fontsize=14, weight='bold')
ax1.grid(False)  # Setting dashed grid lines
ax2.grid(False)  # Turn off grid for the secondary y-axis

plt.savefig(output_file, bbox_inches='tight')

plt.show()
