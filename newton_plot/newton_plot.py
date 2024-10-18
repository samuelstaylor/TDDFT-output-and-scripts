# Python class to generate Newton Plots for coulomb explosion imaging experiments given a moleculeFormations.csv file
# Author: Samuel S. Taylor

import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import MultipleLocator
import os
import matplotlib as mpl

EPSILON = 1e-10

# Set global font to Times New Roman
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['axes.labelsize'] = 14  # increase label font size
mpl.rcParams['xtick.labelsize'] = 12  # increase x tick font size
mpl.rcParams['ytick.labelsize'] = 12  # increase y tick font size
mpl.rcParams['legend.fontsize'] = 12  # Legend font size
# either make axis label 14, then ticks and legend 12 # for c4h10
# or make axis label 16, then ticks and legend 14     # otherwise

class NewtonPlot:
    def __init__(self, SHOW_PLOT=False,SHOW_TITLE=False,SHOW_LEGEND=False):
        # Constants
        self.show_plot = SHOW_PLOT
        self.show_title = SHOW_TITLE
        self.show_legend = SHOW_LEGEND
        self.h_mass = 1.00794  # in g/mol
        self.c_mass = 12.0107  # in g/mol
        self.o_mass = 15.9994  # in g/mol
        self.n_mass = 14.0067  # in g/mol
        self.axis_subdivide = 5  # Number of sub-divisions on each axis
        
        # Dictionary for fragments and data
        self.fragments_x_vel_data = {}
        self.fragments_y_vel_data = {}
        self.fragments_z_vel_data = {}
        
        # Lists for carbon velocities in A/fs
        self.carbon_x_velocities = []
        self.carbon_y_velocities = []
        self.carbon_z_velocities = []

        # Lists for hydrogen velocities in A/fs
        self.hydrogen_x_velocities = []
        self.hydrogen_y_velocities = []
        self.hydrogen_z_velocities = []
        
        # Lists for oxygen velocities in A/fs
        self.oxygen_x_velocities = []
        self.oxygen_y_velocities = []
        self.oxygen_z_velocities = []

        # Lists for nitrogen velocities in A/fs
        self.nitrogen_x_velocities = []
        self.nitrogen_y_velocities = []
        self.nitrogen_z_velocities = []
        
        # Lists for normalized velocities
        self.carbon_x_velocities_norm = []
        self.carbon_y_velocities_norm = []
        self.carbon_z_velocities_norm = []
        self.hydrogen_x_velocities_norm = []
        self.hydrogen_y_velocities_norm = []
        self.hydrogen_z_velocities_norm = []
        self.oxygen_x_velocities_norm = []
        self.oxygen_y_velocities_norm = []
        self.oxygen_z_velocities_norm = []
        self.nitrogen_x_velocities_norm = []
        self.nitrogen_y_velocities_norm = []
        self.nitrogen_z_velocities_norm = []

        # Lists for momentum in A/fs * g/mol
        self.carbon_x_momentum = []
        self.carbon_y_momentum = []
        self.carbon_z_momentum = []
        self.hydrogen_x_momentum = []
        self.hydrogen_y_momentum = []
        self.hydrogen_z_momentum = []
        self.oxygen_x_momentum = []
        self.oxygen_y_momentum = []
        self.oxygen_z_momentum = []
        self.nitrogen_x_momentum = []
        self.nitrogen_y_momentum = []
        self.nitrogen_z_momentum = []
        
        # Lists for momentum completely normalized element-wise
        self.carbon_x_momentum_norm = []
        self.carbon_y_momentum_norm = []
        self.carbon_z_momentum_norm = []
        self.hydrogen_x_momentum_norm = []
        self.hydrogen_y_momentum_norm = []
        self.hydrogen_z_momentum_norm = []
        self.oxygen_x_momentum_norm = []
        self.oxygen_y_momentum_norm = []
        self.oxygen_z_momentum_norm = []
        self.nitrogen_x_momentum_norm = []
        self.nitrogen_y_momentum_norm = []
        self.nitrogen_z_momentum_norm = []
        

    def process_data(self, input_file):
        with open(input_file, mode='r') as file:
            csv_reader = csv.reader(file)
            
            # Edit the csv_reader so that every row only contains elements with no spaces
            lines = list(csv_reader)
            line_skip_num = 9 # this is the number of the info block size. how many lines to skip for every read
            
            for i in range(0, len(lines),line_skip_num):
                fragments_line = lines[i]
                x_vel_line = lines[i + 4]
                y_vel_line = lines[i + 5]
                z_vel_line = lines[i + 6]

                fragments = [frag.split('[')[0].strip() for frag in fragments_line[1:] if frag.strip()]
                x_velocities = [float(x_vel.strip()) for x_vel in x_vel_line[1:] if x_vel.strip()]
                y_velocities = [float(y_vel.strip()) for y_vel in y_vel_line[1:] if y_vel.strip()]
                z_velocities = [float(z_vel.strip()) for z_vel in z_vel_line[1:] if z_vel.strip()]

                for fragment, x_vel, y_vel, z_vel in zip(fragments, x_velocities, y_velocities, z_velocities):
                    # if it is not in one, its not in any
                    if fragment not in self.fragments_x_vel_data:
                        self.fragments_x_vel_data[fragment] = []
                        self.fragments_y_vel_data[fragment] = []
                        self.fragments_z_vel_data[fragment] = []

                    self.fragments_x_vel_data[fragment].append(x_vel)
                    self.fragments_y_vel_data[fragment].append(y_vel)
                    self.fragments_z_vel_data[fragment].append(z_vel)


        # Read the CSV file and extract velocities
        self.carbon_x_velocities = self.fragments_x_vel_data['C']
        self.carbon_y_velocities = self.fragments_y_vel_data['C']
        self.carbon_z_velocities = self.fragments_z_vel_data['C']

        self.hydrogen_x_velocities = self.fragments_x_vel_data['H']
        self.hydrogen_y_velocities = self.fragments_y_vel_data['H']
        self.hydrogen_z_velocities = self.fragments_z_vel_data['H']
        
        self.oxygen_x_velocities = self.fragments_x_vel_data.get('O', [])
        self.oxygen_y_velocities = self.fragments_y_vel_data.get('O', [])
        self.oxygen_z_velocities = self.fragments_z_vel_data.get('O', [])

        self.nitrogen_x_velocities = self.fragments_x_vel_data.get('N', [])
        self.nitrogen_y_velocities = self.fragments_y_vel_data.get('N', [])
        self.nitrogen_z_velocities = self.fragments_z_vel_data.get('N', [])
        
        # Check if the folder exists
        if not os.path.exists('images'):
            # If the folder does not exist, create it
            os.makedirs('images')
            print("Folder 'images' created.")
        else:
            print("Folder 'images' already exists.")
        
        self.normalize_vel_data()
        self.calculate_momentum()

    def normalize_vel_data(self):
        # Normalize Carbon x-direction velocities
        c_x_vel_max = abs(max(self.carbon_x_velocities, default=1))
        c_x_vel_max_temp = abs(min(self.carbon_x_velocities, default=1))
        if c_x_vel_max_temp > c_x_vel_max:
            c_x_vel_max = c_x_vel_max_temp
        self.carbon_x_velocities_norm = [vel / c_x_vel_max for vel in self.carbon_x_velocities]
        
        # Normalize Carbon y-direction velocities
        c_y_vel_max = abs(max(self.carbon_y_velocities, default=1))
        c_y_vel_max_temp = abs(min(self.carbon_y_velocities, default=1))
        if c_y_vel_max_temp > c_y_vel_max:
            c_y_vel_max = c_y_vel_max_temp
        self.carbon_y_velocities_norm = [vel / c_y_vel_max for vel in self.carbon_y_velocities]
        
        # Normalize Carbon z-direction velocities
        c_z_vel_max = abs(max(self.carbon_z_velocities, default=1))
        c_z_vel_max_temp = abs(min(self.carbon_z_velocities, default=1))
        if c_z_vel_max_temp > c_z_vel_max:
            c_z_vel_max = c_z_vel_max_temp
        self.carbon_z_velocities_norm = [vel / c_z_vel_max for vel in self.carbon_z_velocities]
        
        # Normalize Hydrogen x-direction velocities
        h_x_vel_max = abs(max(self.hydrogen_x_velocities, default=1))
        h_x_vel_max_temp = abs(min(self.hydrogen_x_velocities, default=1))
        if h_x_vel_max_temp > h_x_vel_max:
            h_x_vel_max = h_x_vel_max_temp
        self.hydrogen_x_velocities_norm = [vel / h_x_vel_max for vel in self.hydrogen_x_velocities]
        
        # Normalize Hydrogen y-direction velocities
        h_y_vel_max = abs(max(self.hydrogen_y_velocities, default=1))
        h_y_vel_max_temp = abs(min(self.hydrogen_y_velocities, default=1))
        if h_y_vel_max_temp > h_y_vel_max:
            h_y_vel_max = h_y_vel_max_temp
        self.hydrogen_y_velocities_norm = [vel / h_y_vel_max for vel in self.hydrogen_y_velocities]
        
        # Normalize Hydrogen z-direction velocities
        h_z_vel_max = abs(max(self.hydrogen_z_velocities, default=1))
        h_z_vel_max_temp = abs(min(self.hydrogen_z_velocities, default=1))
        if h_z_vel_max_temp > h_z_vel_max:
            h_z_vel_max = h_z_vel_max_temp
        self.hydrogen_z_velocities_norm = [vel / h_z_vel_max for vel in self.hydrogen_z_velocities]

        # Normalize Oxygen x-direction velocities
        o_x_vel_max = abs(max(self.oxygen_x_velocities, default=1))
        o_x_vel_max_temp = abs(min(self.oxygen_x_velocities, default=1))
        if o_x_vel_max_temp > o_x_vel_max:
            o_x_vel_max = o_x_vel_max_temp
        self.oxygen_x_velocities_norm = [vel / o_x_vel_max for vel in self.oxygen_x_velocities]
        
        # Normalize Oxygen y-direction velocities
        o_y_vel_max = abs(max(self.oxygen_y_velocities, default=1))
        o_y_vel_max_temp = abs(min(self.oxygen_y_velocities, default=1))
        if o_y_vel_max_temp > o_y_vel_max:
            o_y_vel_max = o_y_vel_max_temp
        self.oxygen_y_velocities_norm = [vel / o_y_vel_max for vel in self.oxygen_y_velocities]
        
        # Normalize Oxygen z-direction velocities
        o_z_vel_max = abs(max(self.oxygen_z_velocities, default=1))
        o_z_vel_max_temp = abs(min(self.oxygen_z_velocities, default=1))
        if o_z_vel_max_temp > o_z_vel_max:
            o_z_vel_max = o_z_vel_max_temp
        self.oxygen_z_velocities_norm = [vel / o_z_vel_max for vel in self.oxygen_z_velocities]

        # Normalize Nitrogen x-direction velocities
        n_x_vel_max = abs(max(self.nitrogen_x_velocities, default=1))
        n_x_vel_max_temp = abs(min(self.nitrogen_x_velocities, default=1))
        if n_x_vel_max_temp > n_x_vel_max:
            n_x_vel_max = n_x_vel_max_temp
        self.nitrogen_x_velocities_norm = [vel / n_x_vel_max for vel in self.nitrogen_x_velocities]
        
        # Normalize Nitrogen y-direction velocities
        n_y_vel_max = abs(max(self.nitrogen_y_velocities, default=1))
        n_y_vel_max_temp = abs(min(self.nitrogen_y_velocities, default=1))
        if n_y_vel_max_temp > n_y_vel_max:
            n_y_vel_max = n_y_vel_max_temp
        self.nitrogen_y_velocities_norm = [vel / n_y_vel_max for vel in self.nitrogen_y_velocities]
        
        # Normalize Nitrogen z-direction velocities
        n_z_vel_max = abs(max(self.nitrogen_z_velocities, default=1))
        n_z_vel_max_temp = abs(min(self.nitrogen_z_velocities, default=1))
        if n_z_vel_max_temp > n_z_vel_max:
            n_z_vel_max = n_z_vel_max_temp
        self.nitrogen_z_velocities_norm = [vel / n_z_vel_max for vel in self.nitrogen_z_velocities]


    def calculate_momentum(self):
        # Momentums in A/fs * g/mol
        self.carbon_x_momentum = [vel * self.c_mass for vel in self.carbon_x_velocities]
        self.carbon_y_momentum = [vel * self.c_mass for vel in self.carbon_y_velocities]
        self.carbon_z_momentum = [vel * self.c_mass for vel in self.carbon_z_velocities]
        self.hydrogen_x_momentum = [vel * self.h_mass for vel in self.hydrogen_x_velocities]
        self.hydrogen_y_momentum = [vel * self.h_mass for vel in self.hydrogen_y_velocities]
        self.hydrogen_z_momentum = [vel * self.h_mass for vel in self.hydrogen_z_velocities]
        self.oxygen_x_momentum = [vel * self.o_mass for vel in self.oxygen_x_velocities]
        self.oxygen_y_momentum = [vel * self.o_mass for vel in self.oxygen_y_velocities]
        self.oxygen_z_momentum = [vel * self.o_mass for vel in self.oxygen_z_velocities]
        self.nitrogen_x_momentum = [vel * self.n_mass for vel in self.nitrogen_x_velocities]
        self.nitrogen_y_momentum = [vel * self.n_mass for vel in self.nitrogen_y_velocities]
        self.nitrogen_z_momentum = [vel * self.n_mass for vel in self.nitrogen_z_velocities]

        # List of all the max values needed to normalize all the momentum lists
        c_maximums = []
        
        c_maximums.append(abs(max(self.carbon_x_momentum, default=1)))
        c_maximums.append(abs(min(self.carbon_x_momentum, default=1)))
        c_maximums.append(abs(max(self.carbon_y_momentum, default=1)))
        c_maximums.append(abs(min(self.carbon_y_momentum, default=1)))
        c_maximums.append(abs(max(self.carbon_z_momentum, default=1)))
        c_maximums.append(abs(min(self.carbon_z_momentum, default=1)))
        
        c_absolute_max_val = max(c_maximums)
        
        h_maximums = []
        
        h_maximums.append(abs(max(self.hydrogen_x_momentum, default=1)))
        h_maximums.append(abs(min(self.hydrogen_x_momentum, default=1)))
        h_maximums.append(abs(max(self.hydrogen_y_momentum, default=1)))
        h_maximums.append(abs(min(self.hydrogen_y_momentum, default=1)))
        h_maximums.append(abs(max(self.hydrogen_z_momentum, default=1)))
        h_maximums.append(abs(min(self.hydrogen_z_momentum, default=1)))
        
        h_absolute_max_val = max(h_maximums)

        o_maximums = []
        
        o_maximums.append(abs(max(self.oxygen_x_momentum, default=1)))
        o_maximums.append(abs(min(self.oxygen_x_momentum, default=1)))
        o_maximums.append(abs(max(self.oxygen_y_momentum, default=1)))
        o_maximums.append(abs(min(self.oxygen_y_momentum, default=1)))
        o_maximums.append(abs(max(self.oxygen_z_momentum, default=1)))
        o_maximums.append(abs(min(self.oxygen_z_momentum, default=1)))
        
        o_absolute_max_val = max(o_maximums)

        n_maximums = []
        
        n_maximums.append(abs(max(self.nitrogen_x_momentum, default=1)))
        n_maximums.append(abs(min(self.nitrogen_x_momentum, default=1)))
        n_maximums.append(abs(max(self.nitrogen_y_momentum, default=1)))
        n_maximums.append(abs(min(self.nitrogen_y_momentum, default=1)))
        n_maximums.append(abs(max(self.nitrogen_z_momentum, default=1)))
        n_maximums.append(abs(min(self.nitrogen_z_momentum, default=1)))
        
        n_absolute_max_val = max(n_maximums)

        # Create the normalized lists of momentum
        self.carbon_x_momentum_norm = [val / c_absolute_max_val for val in self.carbon_x_momentum]
        self.carbon_y_momentum_norm = [val / c_absolute_max_val for val in self.carbon_y_momentum]
        self.carbon_z_momentum_norm = [val / c_absolute_max_val for val in self.carbon_z_momentum]
        self.hydrogen_x_momentum_norm = [val / h_absolute_max_val for val in self.hydrogen_x_momentum]
        self.hydrogen_y_momentum_norm = [val / h_absolute_max_val for val in self.hydrogen_y_momentum]
        self.hydrogen_z_momentum_norm = [val / h_absolute_max_val for val in self.hydrogen_z_momentum]
        self.oxygen_x_momentum_norm = [val / o_absolute_max_val for val in self.oxygen_x_momentum]
        self.oxygen_y_momentum_norm = [val / o_absolute_max_val for val in self.oxygen_y_momentum]
        self.oxygen_z_momentum_norm = [val / o_absolute_max_val for val in self.oxygen_z_momentum]
        self.nitrogen_x_momentum_norm = [val / n_absolute_max_val for val in self.nitrogen_x_momentum]
        self.nitrogen_y_momentum_norm = [val / n_absolute_max_val for val in self.nitrogen_y_momentum]
        self.nitrogen_z_momentum_norm = [val / n_absolute_max_val for val in self.nitrogen_z_momentum]

    def plot_x_y_velocities(self, normalize=False, graph_name_tag='', graph_xy_title='', alpha=0.03,
                            lim_2d_left=-1,lim_2d_right=1,lim_2d_bottom=-1,lim_2d_top=1):
        if normalize:
            carbon_x_vel = self.carbon_x_velocities_norm
            carbon_y_vel = self.carbon_y_velocities_norm
            hydrogen_x_vel = self.hydrogen_x_velocities_norm
            hydrogen_y_vel = self.hydrogen_y_velocities_norm
            oxygen_x_vel = self.oxygen_x_velocities_norm
            oxygen_y_vel = self.oxygen_y_velocities_norm
            nitrogen_x_vel = self.nitrogen_x_velocities_norm
            nitrogen_y_vel = self.nitrogen_y_velocities_norm
        else:
            carbon_x_vel = self.carbon_x_velocities
            carbon_y_vel = self.carbon_y_velocities
            hydrogen_x_vel = self.hydrogen_x_velocities
            hydrogen_y_vel = self.hydrogen_y_velocities
            oxygen_x_vel = self.oxygen_x_velocities
            oxygen_y_vel = self.oxygen_y_velocities
            nitrogen_x_vel = self.nitrogen_x_velocities
            nitrogen_y_vel = self.nitrogen_y_velocities

        plt.scatter(hydrogen_x_vel, hydrogen_y_vel, color='r', alpha=alpha, label='Hydrogen')
        plt.scatter(carbon_x_vel, carbon_y_vel, color='b', alpha=alpha, label='Carbon')
        plt.scatter(oxygen_x_vel, oxygen_y_vel, color='g', alpha=alpha, label='Oxygen')
        plt.scatter(nitrogen_x_vel, nitrogen_y_vel, color='y', alpha=alpha, label='Nitrogen')
        plt.xlabel('X Velocity (Å/fs)')
        plt.ylabel('Y Velocity (Å/fs)')
        plt.xlim(lim_2d_left, lim_2d_right)
        plt.ylim(lim_2d_bottom, lim_2d_top)
        if self.show_legend:
            plt.legend()
        
        # Add light vertical and horizontal lines at each of the tick marks
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
        
        if normalize:
            if self.show_title:
                plt.title(graph_xy_title + ' Normalized')
            plt.tight_layout()
            plt.savefig(f'images/x_y_velocities_norm_{graph_name_tag}.png')
        else:
            if self.show_title:
                plt.title(graph_xy_title)
            plt.tight_layout()
            plt.savefig(f'images/x_y_velocities_{graph_name_tag}.png')
        
        if self.show_plot:
            plt.show()
        plt.close()

    def plot_x_z_velocities(self, normalize=False, graph_name_tag='', graph_xz_title='', alpha=0.03,
                            lim_2d_left=-1,lim_2d_right=1,lim_2d_bottom=-1,lim_2d_top=1):
        if normalize:
            carbon_x_vel = self.carbon_x_velocities_norm
            carbon_z_vel = self.carbon_z_velocities_norm
            hydrogen_x_vel = self.hydrogen_x_velocities_norm
            hydrogen_z_vel = self.hydrogen_z_velocities_norm
            oxygen_x_vel = self.oxygen_x_velocities_norm
            oxygen_z_vel = self.oxygen_z_velocities_norm
            nitrogen_x_vel = self.nitrogen_x_velocities_norm
            nitrogen_z_vel = self.nitrogen_z_velocities_norm
        else:
            carbon_x_vel = self.carbon_x_velocities
            carbon_z_vel = self.carbon_z_velocities
            hydrogen_x_vel = self.hydrogen_x_velocities
            hydrogen_z_vel = self.hydrogen_z_velocities
            oxygen_x_vel = self.oxygen_x_velocities
            oxygen_z_vel = self.oxygen_z_velocities
            nitrogen_x_vel = self.nitrogen_x_velocities
            nitrogen_z_vel = self.nitrogen_z_velocities

        plt.scatter(hydrogen_x_vel, hydrogen_z_vel, color='r', alpha=alpha, label='Hydrogen')
        plt.scatter(carbon_x_vel, carbon_z_vel, color='b', alpha=alpha, label='Carbon')
        plt.scatter(oxygen_x_vel, oxygen_z_vel, color='g', alpha=alpha, label='Oxygen')
        plt.scatter(nitrogen_x_vel, nitrogen_z_vel, color='y', alpha=alpha, label='Nitrogen')
        plt.xlabel('X Velocity (Å/fs)')
        plt.ylabel('Z Velocity (Å/fs)')
        plt.xlim(lim_2d_left, lim_2d_right)
        plt.ylim(lim_2d_bottom, lim_2d_top)
        if self.show_legend:
            plt.legend()

        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

        if normalize:
            if self.show_title:
                plt.title(graph_xz_title + ' Normalized')
            plt.tight_layout()
            plt.savefig(f'images/x_z_velocities_norm_{graph_name_tag}.png')
        else:
            if self.show_title:
                plt.title(graph_xz_title)
            plt.tight_layout()
            plt.savefig(f'images/x_z_velocities_{graph_name_tag}.png')
        
        if self.show_plot:
            plt.show()
        plt.close()

    def plot_y_z_velocities(self, normalize=False, graph_name_tag='', graph_yz_title='', alpha=0.03,
                            lim_2d_left=-1,lim_2d_right=1,lim_2d_bottom=-1,lim_2d_top=1):
        if normalize:
            carbon_y_vel = self.carbon_y_velocities_norm
            carbon_z_vel = self.carbon_z_velocities_norm
            hydrogen_y_vel = self.hydrogen_y_velocities_norm
            hydrogen_z_vel = self.hydrogen_z_velocities_norm
            oxygen_y_vel = self.oxygen_y_velocities_norm
            oxygen_z_vel = self.oxygen_z_velocities_norm
            nitrogen_y_vel = self.nitrogen_y_velocities_norm
            nitrogen_z_vel = self.nitrogen_z_velocities_norm
        else:
            carbon_y_vel = self.carbon_y_velocities
            carbon_z_vel = self.carbon_z_velocities
            hydrogen_y_vel = self.hydrogen_y_velocities
            hydrogen_z_vel = self.hydrogen_z_velocities
            oxygen_y_vel = self.oxygen_y_velocities
            oxygen_z_vel = self.oxygen_z_velocities
            nitrogen_y_vel = self.nitrogen_y_velocities
            nitrogen_z_vel = self.nitrogen_z_velocities

        plt.scatter(hydrogen_y_vel, hydrogen_z_vel, color='r', alpha=alpha, label='Hydrogen')
        plt.scatter(carbon_y_vel, carbon_z_vel, color='b', alpha=alpha, label='Carbon')
        plt.scatter(oxygen_y_vel, oxygen_z_vel, color='g', alpha=alpha, label='Oxygen')
        plt.scatter(nitrogen_y_vel, nitrogen_z_vel, color='y', alpha=alpha, label='Nitrogen')
        plt.xlabel('Y Velocity (Å/fs)')
        plt.ylabel('Z Velocity (Å/fs)')
        plt.xlim(lim_2d_left, lim_2d_right)
        plt.ylim(lim_2d_bottom, lim_2d_top)
        if self.show_legend:
            plt.legend()
 
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
       
        if normalize:
            if self.show_title:
                plt.title(graph_yz_title + ' Normalized')
            plt.tight_layout()
            plt.savefig(f'images/y_z_velocities_norm_{graph_name_tag}.png')
        else:
            if self.show_title:
                plt.title(graph_yz_title)
            plt.tight_layout()
            plt.savefig(f'images/y_z_velocities_{graph_name_tag}.png')
        
        if self.show_plot:
            plt.show()
        plt.close()

    def plot_3d_projections_basic(self):
        # from: https://stackoverflow.com/questions/26739670/plotting-the-projection-of-3d-plot-in-three-planes-using-contours
        # Convert the carbon velocities lists to NumPy arrays for easier manipulation
        X = np.array(self.carbon_x_velocities)
        Y = np.array(self.carbon_y_velocities)
        Z = np.array(self.carbon_z_velocities)
        
        # Create a new figure for the first 3D plot
        plt.figure()
        ax1 = plt.subplot(111, projection='3d')  # Create a 3D subplot

        # Scatter plot of the carbon velocities in 3D space
        ax1.scatter(X, Y, Z, c='b', marker='.', alpha=0.2)  # Plot with blue dots, slightly transparent
        ax1.set_xlabel('X velocity (Å/fs)')  # Set the label for the X-axis
        ax1.set_ylabel('Y velocity (Å/fs)')  # Set the label for the Y-axis
        ax1.set_zlabel('Z velocity (Å/fs)')  # Set the label for the Z-axis
        
        if self.show_title:
            ax1.set_title('Basic 3d Image of carbon velocities')


        # Create a new figure for the second 3D plot
        plt.figure()
        ax2 = plt.subplot(111, projection='3d')  # Create another 3D subplot

        plt.hot()  # Use the 'hot' colormap

        # Calculate constant arrays for the projections
        cx = np.ones_like(X) * ax1.get_xlim3d()[0]  # Constant X for YZ projection at the left edge of the plot
        cy = np.ones_like(X) * ax1.get_ylim3d()[1]  # Constant Y for XZ projection at the top edge of the plot
        cz = np.ones_like(Z) * ax1.get_zlim3d()[0]  # Constant Z for XY projection at the bottom edge of the plot

        # Scatter plots for the projections onto the XY, XZ, and YZ planes
        ax2.scatter(X, Y, cz, c=Z, marker='.', lw=0, alpha=0.2)  # XY projection, color by Z
        ax2.scatter(X, cy, Z, c=-Y, marker='.', lw=0, alpha=0.2)  # XZ projection, color by negative Y
        ax2.scatter(cx, Y, Z, c=X, marker='.', lw=0, alpha=0.2)  # YZ projection, color by X
        
        # Set the limits of the second plot to be the same as the first plot
        ax2.set_xlim3d(ax1.get_xlim3d())
        ax2.set_ylim3d(ax1.get_ylim3d())
        ax2.set_zlim3d(ax1.get_zlim3d())
        
        # Set axis labels for the second plot
        ax2.set_xlabel('X velocity (Å/fs)')
        ax2.set_ylabel('Y velocity (Å/fs)')
        ax2.set_zlabel('Z velocity (Å/fs)')
        
        if self.show_title:
            ax2.set_title('Basic 3D projections of carbon velocities')

        # Save the figure as a PNG file
        plt.tight_layout()
        plt.savefig('images/3d_projections_basic.png')
        
        # Display the plot
        if self.show_plot:
            plt.show()

    def plot_3d_projections_1_limits(self,graph_name_tag="",
                                     graph_scatter_title="3D Scatter Plot of Velocities",
                                     graph_projection_title="3D Projection of Velocities",
                                     alpha=0.03, lim_3d_x_lower=-1, lim_3d_x_upper=1,
                                     lim_3d_y_lower=-1,lim_3d_y_upper=1,
                                     lim_3d_z_lower=-1,lim_3d_z_upper=1):
        # Convert the carbon velocities lists to NumPy arrays for easier manipulation
        
        C_X = np.array(self.carbon_x_velocities)
        C_Y = np.array(self.carbon_y_velocities)
        C_Z = np.array(self.carbon_z_velocities)
        
        H_X = np.array(self.hydrogen_x_velocities)
        H_Y = np.array(self.hydrogen_y_velocities)
        H_Z = np.array(self.hydrogen_z_velocities)
        
        O_X = np.array(self.oxygen_x_velocities)
        O_Y = np.array(self.oxygen_y_velocities)
        O_Z = np.array(self.oxygen_z_velocities)
        
        N_X = np.array(self.nitrogen_x_velocities)
        N_Y = np.array(self.nitrogen_y_velocities)
        N_Z = np.array(self.nitrogen_z_velocities)
        
        # Create a new figure for the first 3D plot
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111, projection='3d')  # Create a 3D subplot

        # Scatter plot of the carbon velocities in 3D space
        ax1.scatter(H_X, H_Y, H_Z, c='r', marker='.', label='Hydrogen', alpha=alpha)  # Plot with red dots, slightly transparent
        ax1.scatter(C_X, C_Y, C_Z, c='b', marker='.', label='Carbon', alpha=alpha)  # Plot with blue dots, slightly transparent
        ax1.scatter(O_X, O_Y, O_Z, c='g', marker='.', label='Oxygen', alpha=alpha)  # Plot with blue dots, slightly transparent
        ax1.scatter(N_X, N_Y, N_Z, c='y', marker='.', label='Nitrogen', alpha=alpha)  # Plot with red dots, slightly transparent

        ax1.set_xlabel('X Velocity (Å/fs)', fontweight='bold')  # Set the label for the X-axis
        ax1.set_ylabel('Y Velocity (Å/fs)', fontweight='bold')  # Set the label for the Y-axis
        ax1.set_zlabel('Z Velocity (Å/fs)', fontweight='bold')  # Set the label for the Z-axis
        ax1.set_xlim3d(lim_3d_x_lower, lim_3d_x_upper)
        ax1.set_ylim3d(lim_3d_y_lower, lim_3d_y_upper)
        ax1.set_zlim3d(lim_3d_z_lower, lim_3d_z_upper)
        if self.show_title:
            ax1.set_title(graph_scatter_title)
        
        # Set major ticks to show only every other tick
        ax1.set_xticks(np.arange(lim_3d_x_lower, lim_3d_x_upper + EPSILON, 
                     (abs(lim_3d_x_upper) + abs(lim_3d_x_lower)) / self.axis_subdivide))
        ax1.set_yticks(np.arange(lim_3d_x_lower, lim_3d_x_upper+EPSILON, 
                     (abs(lim_3d_y_upper) + abs(lim_3d_y_lower)) / self.axis_subdivide))
        ax1.set_zticks(np.arange(lim_3d_x_lower, lim_3d_x_upper+EPSILON, 
                     (abs(lim_3d_z_upper) + abs(lim_3d_z_lower)) / self.axis_subdivide))

        # Set minor ticks
        ax1.xaxis.set_minor_locator(MultipleLocator((abs(lim_3d_x_upper) + abs(lim_3d_x_lower)) / (2*self.axis_subdivide)))
        ax1.yaxis.set_minor_locator(MultipleLocator((abs(lim_3d_y_upper) + abs(lim_3d_y_lower)) / (2*self.axis_subdivide)))
        ax1.zaxis.set_minor_locator(MultipleLocator((abs(lim_3d_z_upper) + abs(lim_3d_z_lower)) / (2*self.axis_subdivide)))
        
        if self.show_legend:
            plt.legend()

        # Save the first figure
        plt.tight_layout()
        plt.savefig(f'images/3d_scatter_plot_{graph_name_tag}.png')
        plt.close()
        
        # NOW PLOT THE PROJECTIONS
        
        # Create a new figure for the second 3D plot
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111, projection='3d')  # Create another 3D subplot

        plt.hot()  # Use the 'hot' colormap

        # Calculate constant arrays for the projections of carbon
        cx = np.ones_like(C_X) * lim_3d_x_lower  # Constant X for YZ projection at the left edge of the plot
        cy = np.ones_like(C_Y) * lim_3d_y_upper  # Constant Y for XZ projection at the top edge of the plot
        cz = np.ones_like(C_Z) * lim_3d_z_lower  # Constant Z for XY projection at the bottom edge of the plot
        
        # Calculate constant arrays for the projections of hydrogen
        c_hx = np.ones_like(H_X) * lim_3d_x_lower  # Constant X for YZ projection at the left edge of the plot
        c_hy = np.ones_like(H_Y) * lim_3d_y_upper  # Constant Y for XZ projection at the top edge of the plot
        c_hz = np.ones_like(H_Z) * lim_3d_z_lower  # Constant Z for XY projection at the bottom edge of the plot
        
        c_ox = np.ones_like(O_X) * lim_3d_x_lower  # Constant X for YZ projection at the left edge of the plot
        c_oy = np.ones_like(O_Y) * lim_3d_y_upper  # Constant Y for XZ projection at the top edge of the plot
        c_oz = np.ones_like(O_Z) * lim_3d_z_lower  # Constant Z for XY projection at the bottom edge of the plot

        c_nx = np.ones_like(N_X) * lim_3d_x_lower  # Constant X for YZ projection at the left edge of the plot
        c_ny = np.ones_like(N_Y) * lim_3d_y_upper  # Constant Y for XZ projection at the top edge of the plot
        c_nz = np.ones_like(N_Z) * lim_3d_z_lower  # Constant Z for XY projection at the bottom edge of the plot

        
        # Scatter plots for the projections onto the XY, XZ, and YZ planes of hydrogen
        ax2.scatter(H_X, H_Y, c_hz, c='r', marker='.', lw=0, alpha=alpha)  # XY projection, color by Z
        ax2.scatter(H_X, c_hy, H_Z, c='r', marker='.', lw=0, alpha=alpha)  # XZ projection, color by negative Y
        ax2.scatter(c_hx, H_Y, H_Z, c='r', marker='.', lw=0, alpha=alpha)  # YZ projection, color by X
        
        # Scatter plots for the projections onto the XY, XZ, and YZ planes of oxygen
        ax2.scatter(O_X, O_Y, c_oz, c='g', marker='.', lw=0, alpha=alpha)  # XY projection, color by Z
        ax2.scatter(O_X, c_oy, O_Z, c='g', marker='.', lw=0, alpha=alpha)  # XZ projection, color by negative Y
        ax2.scatter(c_ox, O_Y, O_Z, c='g', marker='.', lw=0, alpha=alpha)  # YZ projection, color by X

        # Scatter plots for the projections onto the XY, XZ, and YZ planes of nitrogen
        ax2.scatter(N_X, N_Y, c_nz, c='y', marker='.', lw=0, alpha=alpha)  # XY projection, color by Z
        ax2.scatter(N_X, c_ny, N_Z, c='y', marker='.', lw=0, alpha=alpha)  # XZ projection, color by negative Y
        ax2.scatter(c_nx, N_Y, N_Z, c='y', marker='.', lw=0, alpha=alpha)  # YZ projection, color by X

        # Scatter plots for the projections onto the XY, XZ, and YZ planes of carbon
        ax2.scatter(C_X, C_Y, cz, c='b', marker='.', lw=0, alpha=alpha)  # XY projection, color by Z
        ax2.scatter(C_X, cy, C_Z, c='b', marker='.', lw=0, alpha=alpha)  # XZ projection, color by negative Y
        ax2.scatter(cx, C_Y, C_Z, c='b', marker='.', lw=0, alpha=alpha)  # YZ projection, color by X
        
        # Set the limits of the second plot to be the same as the first plot
        ax2.set_xlim3d(lim_3d_x_lower, lim_3d_x_upper)
        ax2.set_ylim3d(lim_3d_y_lower, lim_3d_x_upper)
        ax2.set_zlim3d(lim_3d_z_lower, lim_3d_x_upper)
        
        # Set major ticks to show only every other tick
        ax2.set_xticks(np.arange(lim_3d_x_lower, lim_3d_x_upper+EPSILON, 
                        (abs(lim_3d_x_upper) + abs(lim_3d_x_lower)) / self.axis_subdivide))
        ax2.set_yticks(np.arange(lim_3d_x_lower, lim_3d_x_upper+EPSILON, 
                        (abs(lim_3d_y_upper) + abs(lim_3d_y_lower)) / self.axis_subdivide))
        ax2.set_zticks(np.arange(lim_3d_x_lower, lim_3d_x_upper+EPSILON, 
                        (abs(lim_3d_z_upper) + abs(lim_3d_z_lower)) / self.axis_subdivide))

        # Set minor ticks
        ax2.xaxis.set_minor_locator(MultipleLocator((abs(lim_3d_x_upper) + abs(lim_3d_x_lower)) / (2*self.axis_subdivide)))
        ax2.yaxis.set_minor_locator(MultipleLocator((abs(lim_3d_y_upper) + abs(lim_3d_y_lower)) / (2*self.axis_subdivide)))
        ax2.zaxis.set_minor_locator(MultipleLocator((abs(lim_3d_z_upper) + abs(lim_3d_z_lower)) / (2*self.axis_subdivide)))

        # Set axis labels for the second plot
        ax2.set_xlabel('X Velocity (Å/fs)', fontweight='bold')
        ax2.set_ylabel('Y Velocity (Å/fs)', fontweight='bold')
        ax2.set_zlabel('Z Velocity (Å/fs)', fontweight='bold')
        if self.show_title:
            ax2.set_title(graph_projection_title)

        # Save the second figure
        plt.tight_layout()
        
        plt.savefig(f'images/3d_projections_{graph_name_tag}.png')
        
        # Display the plots
        if self.show_plot:
            plt.show()
        
        plt.close()
            
            
    def plot_2d_projections(self, normalize=False,graph_name_tag="",
                                    graph_xy_title="Carbon and Hydrogen X,Y Velocities",
                                    graph_xz_title="Carbon and Hydrogen X,Z Velocities",
                                    graph_yz_title="Carbon and Hydrogen Y,Z Velocities",
                                    alpha=0.03, lim_2d_left=-1,lim_2d_right=1,
                                    lim_2d_bottom=-1,lim_2d_top=1):
        # Plot all of the 2-D NORMALIZED velocity projections
        self.plot_x_y_velocities(normalize=normalize,graph_name_tag=graph_name_tag,graph_xy_title=graph_xy_title,
                                 alpha=alpha,lim_2d_left=lim_2d_left,lim_2d_right=lim_2d_right,
                                 lim_2d_bottom=lim_2d_bottom,lim_2d_top=lim_2d_top)
        self.plot_x_z_velocities(normalize=normalize,graph_name_tag=graph_name_tag,graph_xz_title=graph_xz_title,
                                 alpha=alpha,lim_2d_left=lim_2d_left,lim_2d_right=lim_2d_right,
                                 lim_2d_bottom=lim_2d_bottom,lim_2d_top=lim_2d_top)
        self.plot_y_z_velocities(normalize=normalize,graph_name_tag=graph_name_tag,graph_yz_title=graph_yz_title,
                                 alpha=alpha,lim_2d_left=lim_2d_left,lim_2d_right=lim_2d_right,
                                 lim_2d_bottom=lim_2d_bottom,lim_2d_top=lim_2d_top)


def main():
    print("-=GENERATING NEWTON PLOT=-")
    newton_plot = NewtonPlot()
    data_mode = "c" # c for classical, q for quantum
    user_input_mode = False
    alpha = 0.2  #set alpha =0.2 for c4h10 and =0.03 for c2h2
    lim_2d_left=-1.0
    lim_2d_right=1.0
    lim_2d_bottom=-1.0
    lim_2d_top=1.0
    lim_3d_x_lower=-1.0
    lim_3d_x_upper=1.0
    lim_3d_y_lower=-1.0
    lim_3d_y_upper=1.0
    lim_3d_z_lower=-1.0
    lim_3d_z_upper=1.0
    newton_plot.axis_subdivide = 4    

    if (data_mode.lower().startswith('c')):
        #CLASSICAL INPUT FILE:
        input_file = 'newton_plot\\atom_info.csv'
 
        graph_name_tag="classical"
        
    if (data_mode.lower().startswith('q')):
        #QUANTUM INPUT FILE:
        input_file = 'newton_plot\\moleculeFormations_14.csv'
        graph_name_tag="quantum"

    if user_input_mode:
        input_file = input("Enter the path from current working directory to atom info file: ")
    print("Searching for input file: ", input_file)

    newton_plot.process_data(input_file)
    
    print("Generating Plots...")
    # 2-d velocity projections
    newton_plot.plot_2d_projections(normalize=False,
                                    graph_name_tag=graph_name_tag,
                                    graph_xy_title=f"Carbon and Hydrogen X,Y Velocities ({graph_name_tag})",
                                    graph_xz_title=f"Carbon and Hydrogen X,Z Velocities ({graph_name_tag})",
                                    graph_yz_title=f"Carbon and Hydrogen Y,Z Velocities ({graph_name_tag})",
                                    alpha=alpha, lim_2d_left=lim_2d_left, lim_2d_right=lim_2d_right,
                                    lim_2d_bottom=lim_2d_bottom,lim_2d_top=lim_2d_top)
    
    # 3-D scatter and projection plots    
    newton_plot.plot_3d_projections_1_limits(graph_name_tag=graph_name_tag,
                                             graph_scatter_title=f"3D Scatter Plot of Velocities ({graph_name_tag})",
                                             graph_projection_title=f"3D Projection of Velocities ({graph_name_tag})",
                                             alpha=alpha, lim_3d_x_lower=lim_3d_x_lower, lim_3d_x_upper=lim_3d_x_upper,
                                             lim_3d_y_lower=lim_3d_y_lower,lim_3d_y_upper=lim_3d_y_upper,
                                             lim_3d_z_lower=lim_3d_z_lower,lim_3d_z_upper=lim_3d_z_upper)
    
    print("FINSIHED: ALL PLOTS GENERATED")

if __name__ == '__main__':
    main()