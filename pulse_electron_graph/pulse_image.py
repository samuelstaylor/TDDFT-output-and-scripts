import matplotlib.pyplot as plt

# Lists to store data
time_pulse = []
values_pulse = []

# Read pulse.dat
with open('pulse.dat', 'r') as file:
    for line in file:
        parts = line.split()
        if len(parts) > 1:
            if float(parts[0]) > 120:
                break
            time_pulse.append(float(parts[0]))
            values_pulse.append(float(parts[1]))

# Plotting
fig, ax1 = plt.subplots()

# Plot the first dataset
ax1.set_xlabel('Time (fs)', fontsize=20, weight='bold')
ax1.plot(time_pulse, values_pulse, color='black', label='Info Data', alpha=1)
ax1.tick_params(axis='y', labelcolor='black', which='both', direction='in', width=2, length=6, labelsize=16)
ax1.tick_params(axis='x', labelcolor='black', which='both', direction='in', width=2, length=6, labelsize=16)


# Add more tick marks on both axes
ax1.xaxis.set_major_locator(plt.MaxNLocator(12))
ax1.yaxis.set_major_locator(plt.MaxNLocator(10))

# Add minor ticks on both axes
ax1.minorticks_on()
ax1.tick_params(axis='x', which='minor', direction='in', length=3, width=1, labelsize=18)
ax1.tick_params(axis='y', which='minor', direction='in', length=3, width=1, labelsize=14)

# Set y-axis label
ax1.set_ylabel('Electric Field (V/Å)', color='black', fontsize=20, weight='bold')

# Set x-axis limits
ax1.set_xlim(0, 120)

# Add a horizontal dashed line at 7.26 V/Å
ax1.axhline(y=7.26, color='gray', linestyle='--', linewidth=1)

# Add text at the 7.26 V/Å line
ax1.text(-.35, 7.05, '7.26', color='black', fontsize=16, verticalalignment='bottom', horizontalalignment='right')

fig.tight_layout()
#plt.title('GDD = 0 Pulse Used in Coulomb Explosion Simulations', fontsize=14, weight='bold')
ax1.grid(False)  # Turn off grid for primary y-axis

# Save the plot as a PNG image
plt.savefig("pulse_7_26.png")

plt.show()
