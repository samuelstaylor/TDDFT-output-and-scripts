import matplotlib.pyplot as plt

# Lists to store data
file_name = "info"
time_info = []
electron_num = []

# Read info.txt
with open(file_name + ".txt", 'r') as file:
    for line in file:
        parts = line.split()
        time_info.append(float(parts[1]))
        electron_num.append(float(parts[2]))

# Plotting
fig, ax1 = plt.subplots()

# Plot the first dataset
color = 'tab:blue'
ax1.set_xlabel('Time (fs)', fontsize=12, weight='bold')
ax1.plot(time_info, electron_num, color='tab:blue', label='Electric Field')
ax1.tick_params(axis='y', labelcolor='tab:blue', which='both', direction='in', width=2, length=6, labelsize=10)

ax1.set_ylabel('Number of Electrons', color='tab:blue', fontsize=12, weight='bold')

fig.tight_layout()
plt.title('Number of Electrons in Butane', fontsize=14, weight='bold')
ax1.grid(False)  # Setting dashed grid lines

# Save the plot as a PNG image
plt.savefig(file_name + '.png')

print("Successfully Printed", file_name)
