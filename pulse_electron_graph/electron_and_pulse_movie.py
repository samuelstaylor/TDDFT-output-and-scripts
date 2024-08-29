import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

class ElectronPulseAnimation(object):
    def __init__(self, electron_num, time_pulse, values_pulse):
        self.values_pulse = values_pulse
        self.electron_num = electron_num
        self.time_pulse = time_pulse

        # set up parameters
        self.niter = len(time_pulse)
        self.xpos = 0
        self.xmax = time_pulse[-1]

    def init(self):
        # initialiser for animator
        self.electrons.set_data([], [])
        self.pulse.set_data([], [])
        self.background_electrons.set_data([], [])
        self.background_pulse.set_data([], [])
        return self.electrons, self.pulse, self.background_electrons, self.background_pulse

    def animate(self, i):
        # update the plot
        if i < len(self.time_pulse):
            self.electrons.set_data(self.time_pulse[:i], self.electron_num[:i])
            self.pulse.set_data(self.time_pulse[:i], self.values_pulse[:i])
            self.background_electrons.set_data(self.time_pulse, self.electron_num)
            self.background_pulse.set_data(self.time_pulse, self.values_pulse)
        patches = [self.background_pulse, self.background_electrons, self.pulse, self.electrons]    
        return patches

    def run(self):
        # create plot elements
        fig, ax = plt.subplots()
        ax.set_xlabel('Time (fs)', fontsize=12, weight='bold')
        ax.set_ylabel('Electric Field (V/Å)', color='tab:red', fontsize=12, weight='bold')
        ax2 = ax.twinx()
        ax2.set_ylabel('Number of Electrons', color='tab:blue', fontsize=12, weight='bold')
        
        # initialize the plot data
        self.electrons, = ax2.plot([], [], color='tab:blue', label='Number of Electrons')
        self.pulse, = ax.plot([], [], color='tab:red', alpha=0.5, label='Electric Field')
        self.background_electrons, = ax2.plot([], [], color='tab:blue', alpha=0.1)
        self.background_pulse, = ax.plot([], [], color='tab:red', alpha=0.1)

        # set up the axes
        ax.set_xlim(0, self.xmax)
        ax.set_ylim(min(self.values_pulse) - 1, max(self.values_pulse) + 1)
        ax2.set_ylim(min(self.electron_num) - 1, max(self.electron_num) + 1)
        ax.tick_params(axis='y', labelcolor='tab:red', which='both', direction='in', width=2, length=6, labelsize=10)
        ax2.tick_params(axis='y', labelcolor='tab:blue', which='both', direction='in', width=2, length=6, labelsize=10)

        #ax.legend(loc='upper left')
        #ax2.legend(loc='upper right')

        # create the animator
        self.anim = FuncAnimation(fig, self.animate, init_func=self.init, frames=self.niter + 1, interval=1, blit=True)

        plt.grid(False)
        plt.title('Number of Electrons in Butane Coulomb Explosion', fontsize=14, weight='bold')

        plt.show()

        
        # Save the animation using FFmpeg
        writervideo = FFMpegWriter(fps=60)
        self.anim.save('electron_pulse_animation.mp4', writer=writervideo)
        print("Animation saved as electron_pulse_animation.mp4")



def main():
    # Read data from files
    electron_num = []
    time_pulse = []
    values_pulse = []

    with open('pulse.dat', 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) > 1:
                if float(parts[0]) > 120:
                    break
                time_pulse.append(float(parts[0]))
                values_pulse.append(float(parts[1]))

    with open('info.txt', 'r') as file:
        line_counter = -1  # the line you are at in the file equals this number + 1
        added_data_counter = 0
        for line in file:
            line_counter += 1
            parts = line.split()
            if (line_counter == (int(1000 * (time_pulse[added_data_counter])))):
                electron_num.append(float(parts[2]))
                added_data_counter += 1          
            if (added_data_counter >= len(time_pulse)):
                break

    # Run the animation
    animation = ElectronPulseAnimation(electron_num, time_pulse, values_pulse)
    animation.run()

if __name__ == "__main__":
    main()
