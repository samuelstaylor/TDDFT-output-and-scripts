import numpy as np
from scipy.interpolate import interp1d

# Read data from pulse.dat
time_steps = []
electric_field = []

with open('pulse.dat', 'r') as file:
    # Skip the first line
    next(file)
    for line in file:
        parts = line.split()
        if len(parts) >= 2:
            time_steps.append(float(parts[0]))
            electric_field.append(float(parts[1]))

# Interpolate data
interp_func = interp1d(time_steps, electric_field, kind='linear')

# Create new time steps with 0.001 increments, ensuring we stay within the original bounds
new_time_steps = np.arange(time_steps[0], time_steps[-1], 0.001)
new_electric_field = interp_func(new_time_steps)

# Write the interpolated data to pulse_inter.dat
with open('pulse_inter.dat', 'w') as file:
    for t, ef in zip(new_time_steps, new_electric_field):
        file.write(f"{t:.3f}\t{ef:.10f}\n")

print("Interpolation complete. Data saved to pulse_inter.dat")
