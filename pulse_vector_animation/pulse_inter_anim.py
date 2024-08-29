import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from scipy.interpolate import interp1d

# Read data from pulse_inter.dat
time_steps = []
e_field_values = []

with open('pulse_inter.dat', 'r') as file:
    for line in file:
        parts = line.split()
        if len(parts) == 2:
            time_steps.append(float(parts[0]))
            e_field_values.append(float(parts[1]))

# Prepare the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-1.1 * max(e_field_values), 1.1 * max(e_field_values))  # Adjust the limits based on the expected range of e_field_values
ax.set_ylim(-1.2, 2.2)  # Helps place where the arrow is vertically
ax.set_aspect('equal')
ax.spines['left'].set_color('none')  # Remove left spine
ax.spines['right'].set_color('none')  # Remove right spine
ax.spines['top'].set_color('none')  # Remove top spine
ax.xaxis.set_ticks_position('bottom')  # Move x-axis ticks to the bottom
ax.yaxis.set_ticks([])  # Remove y-axis ticks

hw = .4  # Head width
hl = .6  # Head length
bw = .2  # Body width
# Initialize the vector arrow and text elements
arrow = ax.arrow(0, 0, 1, 0, head_width=hw, head_length=hl, width=bw, fc='red', ec='red')
time_text = ax.text(0.5, 0.85, '', transform=ax.transAxes, ha='center', va='center', fontsize=12, color='blue')
pulse_text = ax.text(0.5, 0.65, '', transform=ax.transAxes, ha='center', va='center', fontsize=12, color='red', weight='bold')

# Calculate the number of frames based on 0.1 second intervals
frame_interval = 0.1
frames = np.arange(0, time_steps[-1], frame_interval)
frame_indices = (frames / 0.001).astype(int)

# Update function for animation
def update(frame_index):
    global arrow
    # Remove the old arrow
    arrow.remove()
    
    # Determine the length and direction based on e_field_values
    length = e_field_values[frame_indices[frame_index]]
    
    # Draw a new arrow with the updated length
    arrow = ax.arrow(0, 0, length, 0, head_width=hw, head_length=hl, width=bw, fc='red', ec='red')
    
    # Update the text elements with the current time and pulse values
    time_text.set_text(f'Time: {int(time_steps[frame_indices[frame_index]])} (fs)')
    pulse_text.set_text(f'E-field: {e_field_values[frame_indices[frame_index]]:.1f} (V/Å)')
    
    return arrow, time_text, pulse_text

# Draw a box around the figure
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['right'].set_color('black')
ax.spines['top'].set_color('black')


# Create the animation with increased fps
animation = FuncAnimation(fig, update, frames=len(frames), interval=100)  # Set interval to 100 milliseconds (0.1 seconds)

writervideo = FFMpegWriter(fps=10)
animation.save('pulse_animation.mp4', writer=writervideo)
print("Successfully saved animation as pulse_animation.mp4")

