import matplotlib.pyplot as plt

# Lists to store data
file_name = "info_r62"
time_info = []
electron_num = []
time_pulse = []
values_pulse = []

# Read info.txt
with open(file_name + ".txt", 'r') as file:
    for line in file:
        parts = line.split()
        time_info.append(float(parts[1]))
        electron_num.append(float(parts[2]))

# Read pulse.dat
with open('pulse.dat', 'r') as file:
    data_points_added = 0
    for line in file:
        parts = line.split()
        if len(parts) > 1:
            if float(parts[0]) > 120:
                break
            time_pulse.append(float(parts[0]))
            values_pulse.append(float(parts[1]))

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 8))  # Adjust the figsize parameter to increase the figure size

# Plot the first dataset
color = 'tab:blue'
ax1.set_xlabel('Time (fs)', fontsize=12, weight='bold')
ax1.plot(time_pulse, values_pulse, color='tab:red', label='Info Data', alpha=0.5)
ax1.tick_params(axis='y', labelcolor='tab:red', which='both', direction='in', width=2, length=6, labelsize=10)

# Create a second y-axis
ax2 = ax1.twinx()
ax1.set_ylabel('Electric Field (V/Å)', color='tab:red', fontsize=12, weight='bold')
ax2.set_ylabel('Number of Electrons', color='tab:blue', fontsize=12, weight='bold')

# Make the pulse line faded and in the background
ax2.plot(time_info, electron_num, color='tab:blue', label='Electric Field')
ax2.tick_params(axis='y', labelcolor='tab:blue', which='both', direction='in', width=2, length=6, labelsize=10)

plt.title('Number of Electrons in Butane', fontsize=14, weight='bold')  # Moved title outside tight_layout

fig.tight_layout()
ax1.grid(False)  # Setting dashed grid lines
ax2.grid(False)  # Turn off grid for the secondary y-axis

# Save the plot as a PNG image with adjusted bounding box
plt.savefig(file_name +'.png', bbox_inches='tight')

plt.show()

print("successfully printed", file_name)