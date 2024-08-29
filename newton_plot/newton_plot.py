# Python class to generate Newton Plots for coulomb explosion imaging experiments given a moleculeFormations.csv file
# Author: Samuel S. Taylor

import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import MultipleLocator
import os

class NewtonPlot:
    def __init__(self, SHOW_PLOT=False):
        # Constants
        self.show_plot = SHOW_PLOT
        self.h_mass = 1.00794 # in g/mol
        self.c_mass =12.0107  # in g/mol
        
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
        
        # Lists for normalized velocities
        self.carbon_x_velocities_norm = []
        self.carbon_y_velocities_norm = []
        self.carbon_z_velocities_norm = []
        self.hydrogen_x_velocities_norm = []
        self.hydrogen_y_velocities_norm = []
        self.hydrogen_z_velocities_norm = []
        
        # Lists for momentum in A/fs * g/mol
        self.carbon_x_momentum = []
        self.carbon_y_momentum = []
        self.carbon_z_momentum = []
        self.hydrogen_x_momentum = []
        self.hydrogen_y_momentum = []
        self.hydrogen_z_momentum = []
        
        # Lists for momentum completely normalized element-wise
        self.carbon_x_momentum_norm = []
        self.carbon_y_momentum_norm = []
        self.carbon_z_momentum_norm = []
        self.hydrogen_x_momentum_norm = []
        self.hydrogen_y_momentum_norm = []
        self.hydrogen_z_momentum_norm = []


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
        c_x_vel_max = abs(max(self.carbon_x_velocities))
        c_x_vel_max_temp = abs(min(self.carbon_x_velocities))
        if c_x_vel_max_temp > c_x_vel_max:
            c_x_vel_max = c_x_vel_max_temp
        self.carbon_x_velocities_norm = [vel / c_x_vel_max for vel in self.carbon_x_velocities]
        
        # Normalize Carbon y-direction velocities
        c_y_vel_max = abs(max(self.carbon_y_velocities))
        c_y_vel_max_temp = abs(min(self.carbon_y_velocities))
        if c_y_vel_max_temp > c_y_vel_max:
            c_y_vel_max = c_y_vel_max_temp
        self.carbon_y_velocities_norm = [vel / c_y_vel_max for vel in self.carbon_y_velocities]
        
        # Normalize Carbon z-direction velocities
        c_z_vel_max = abs(max(self.carbon_z_velocities))
        c_z_vel_max_temp = abs(min(self.carbon_z_velocities))
        if c_z_vel_max_temp > c_z_vel_max:
            c_z_vel_max = c_z_vel_max_temp
        self.carbon_z_velocities_norm = [vel / c_z_vel_max for vel in self.carbon_z_velocities]
        
        # Normalize Hydrogen x-direction velocities
        h_x_vel_max = abs(max(self.hydrogen_x_velocities))
        h_x_vel_max_temp = abs(min(self.hydrogen_x_velocities))
        if h_x_vel_max_temp > h_x_vel_max:
            h_x_vel_max = h_x_vel_max_temp
        self.hydrogen_x_velocities_norm = [vel / h_x_vel_max for vel in self.hydrogen_x_velocities]
        
        # Normalize Hydrogen y-direction velocities
        h_y_vel_max = abs(max(self.hydrogen_y_velocities))
        h_y_vel_max_temp = abs(min(self.hydrogen_y_velocities))
        if h_y_vel_max_temp > h_y_vel_max:
            h_y_vel_max = h_y_vel_max_temp
        self.hydrogen_y_velocities_norm = [vel / h_y_vel_max for vel in self.hydrogen_y_velocities]
        
        # Normalize Hydrogen z-direction velocities
        h_z_vel_max = abs(max(self.hydrogen_z_velocities))
        h_z_vel_max_temp = abs(min(self.hydrogen_z_velocities))
        if h_z_vel_max_temp > h_z_vel_max:
            h_z_vel_max = h_z_vel_max_temp
        self.hydrogen_z_velocities_norm = [vel / h_z_vel_max for vel in self.hydrogen_z_velocities]


    def calculate_momentum(self):
        # Momentums in A/fs * g/mol
        self.carbon_x_momentum = [vel * self.c_mass for vel in self.carbon_x_velocities]
        self.carbon_y_momentum = [vel * self.c_mass for vel in self.carbon_y_velocities]
        self.carbon_z_momentum = [vel * self.c_mass for vel in self.carbon_z_velocities]
        self.hydrogen_x_momentum = [vel * self.h_mass for vel in self.hydrogen_x_velocities]
        self.hydrogen_y_momentum = [vel * self.h_mass for vel in self.hydrogen_y_velocities]
        self.hydrogen_z_momentum = [vel * self.h_mass for vel in self.hydrogen_z_velocities]

        # List of all the max values needed to normalize all the momentum lists
        c_maximums = []
        
        c_maximums.append(abs(max(self.carbon_x_momentum)))
        c_maximums.append(abs(min(self.carbon_x_momentum)))
        c_maximums.append(abs(max(self.carbon_y_momentum)))
        c_maximums.append(abs(min(self.carbon_y_momentum)))
        c_maximums.append(abs(max(self.carbon_z_momentum)))
        c_maximums.append(abs(min(self.carbon_z_momentum)))
        
        c_absolute_max_val = max(c_maximums)
        
        h_maximums = []
        
        h_maximums.append(abs(max(self.hydrogen_x_momentum)))
        h_maximums.append(abs(min(self.hydrogen_x_momentum)))
        h_maximums.append(abs(max(self.hydrogen_y_momentum)))
        h_maximums.append(abs(min(self.hydrogen_y_momentum)))
        h_maximums.append(abs(max(self.hydrogen_z_momentum)))
        h_maximums.append(abs(min(self.hydrogen_z_momentum)))
        
        h_absolute_max_val = max(h_maximums)

        
        # Create the normalized lists of momentum
        self.carbon_x_momentum_norm = [val/c_absolute_max_val for val in self.carbon_x_momentum]
        self.carbon_y_momentum_norm = [val/c_absolute_max_val for val in self.carbon_y_momentum]
        self.carbon_z_momentum_norm = [val/c_absolute_max_val for val in self.carbon_z_momentum]
        self.hydrogen_x_momentum_norm = [val/h_absolute_max_val for val in self.hydrogen_x_momentum]
        self.hydrogen_y_momentum_norm = [val/h_absolute_max_val for val in self.hydrogen_y_momentum]
        self.hydrogen_z_momentum_norm = [val/h_absolute_max_val for val in self.hydrogen_z_momentum]
        

    def plot_x_y_velocities(self,normalize=False,graph_name_tag='',graph_xy_title=''):
        
        if normalize:
            carbon_x_vel = self.carbon_x_velocities_norm
            carbon_y_vel = self.carbon_y_velocities_norm
            hydrogen_x_vel = self.hydrogen_x_velocities_norm
            hydrogen_y_vel = self.hydrogen_y_velocities_norm
        else:
            carbon_x_vel = self.carbon_x_velocities
            carbon_y_vel = self.carbon_y_velocities
            hydrogen_x_vel = self.hydrogen_x_velocities
            hydrogen_y_vel = self.hydrogen_y_velocities
            
        
        # Plot the velocities
        plt.figure(figsize=(10, 6))

        plt.scatter(carbon_x_vel, carbon_y_vel, color='blue', label='Carbon')
        plt.scatter(hydrogen_x_vel, hydrogen_y_vel, color='red', label='Hydrogen')

        plt.xlim(-1, 1)
        plt.ylim(-1,1)

        plt.xlabel('X Velocity [A/fs]')
        plt.ylabel('Y Velocity [A/fs]')
        plt.legend()
        plt.grid(True)
        if normalize:
            plt.title(graph_xy_title +' Normalized')
            plt.savefig(f'images/x_y_velocities_norm_{graph_name_tag}.png')
        else:
            plt.title(graph_xy_title)
            plt.savefig(f'images/x_y_velocities_{graph_name_tag}.png')
        if self.show_plot:
            plt.show()
        
    def plot_x_z_velocities(self,normalize=False,graph_name_tag='',graph_xz_title=''): 
        if normalize:
            carbon_x_vel = self.carbon_x_velocities_norm
            carbon_z_vel = self.carbon_z_velocities_norm
            hydrogen_x_vel = self.hydrogen_x_velocities_norm
            hydrogen_z_vel = self.hydrogen_z_velocities_norm
        else:
            carbon_x_vel = self.carbon_x_velocities
            carbon_z_vel = self.carbon_z_velocities
            hydrogen_x_vel = self.hydrogen_x_velocities
            hydrogen_z_vel = self.hydrogen_z_velocities
            
        
        # Plot the velocities
        plt.figure(figsize=(10, 6))

        plt.scatter(carbon_x_vel, carbon_z_vel, color='blue', label='Carbon')
        plt.scatter(hydrogen_x_vel, hydrogen_z_vel, color='red', label='Hydrogen')

        plt.xlim(-1, 1)
        plt.ylim(-1,1)

        plt.xlabel('Y Velocity [A/fs]')
        plt.ylabel('Z Velocity [A/fs]')
        plt.legend()
        plt.grid(True)
        if normalize:
            plt.title(graph_xz_title +' Normalized')
            plt.savefig(f'images/x_z_velocities_norm_{graph_name_tag}.png')
        else:
            plt.title(graph_xz_title)
            plt.savefig(f'images/x_z_velocities_{graph_name_tag}.png')
        if self.show_plot:
            plt.show()

    def plot_y_z_velocities(self,normalize=False,graph_name_tag='',graph_yz_title=''): 
        if normalize:
            carbon_y_vel = self.carbon_y_velocities_norm
            carbon_z_vel = self.carbon_z_velocities_norm
            hydrogen_y_vel = self.hydrogen_y_velocities_norm
            hydrogen_z_vel = self.hydrogen_z_velocities_norm
        else:
            carbon_y_vel = self.carbon_y_velocities
            carbon_z_vel = self.carbon_z_velocities
            hydrogen_y_vel = self.hydrogen_y_velocities
            hydrogen_z_vel = self.hydrogen_z_velocities
            
        
        # Plot the velocities
        plt.figure(figsize=(10, 6))

        plt.scatter(carbon_y_vel, carbon_z_vel, color='blue', label='Carbon')
        plt.scatter(hydrogen_y_vel, hydrogen_z_vel, color='red', label='Hydrogen')

        plt.xlim(-1, 1)
        plt.ylim(-1,1)

        plt.xlabel('Y Velocity [A/fs]')
        plt.ylabel('Z Velocity [A/fs]')
        plt.legend()
        plt.grid(True)
        if normalize:
            plt.title(graph_yz_title +' Normalized')
            plt.savefig(f'images/y_z_velocities_norm_{graph_name_tag}.png')
        else:
            plt.title(graph_yz_title)
            plt.savefig(f'images/y_z_velocities_{graph_name_tag}.png')
        if self.show_plot:
            plt.show()

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
        
        ax2.set_title('Basic 3D projections of carbon velocities')

        # Save the figure as a PNG file
        plt.savefig('images/3d_projections_basic.png')
        
        # Display the plot
        if self.show_plot:
            plt.show()

    def plot_3d_projections_1_limits(self,graph_name_tag="",
                                     graph_scatter_title="3D Scatter Plot of Velocities",
                                     graph_projection_title="3D Projection of Velocities",
                                     alpha=0.03):
        # Convert the carbon velocities lists to NumPy arrays for easier manipulation
        
        C_X = np.array(self.carbon_x_velocities)
        C_Y = np.array(self.carbon_y_velocities)
        C_Z = np.array(self.carbon_z_velocities)
        
        H_X = np.array(self.hydrogen_x_velocities)
        H_Y = np.array(self.hydrogen_y_velocities)
        H_Z = np.array(self.hydrogen_z_velocities)
        
        # Create a new figure for the first 3D plot
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111, projection='3d')  # Create a 3D subplot

        # Scatter plot of the carbon velocities in 3D space
        ax1.scatter(C_X, C_Y, C_Z, c='b', marker='.', label='Carbon', alpha=alpha)  # Plot with blue dots, slightly transparent
        ax1.scatter(H_X, H_Y, H_Z, c='r', marker='.', label='Hydrogen', alpha=alpha)  # Plot with red dots, slightly transparent

        ax1.set_xlabel('X Velocity (Å/fs)', fontweight='bold')  # Set the label for the X-axis
        ax1.set_ylabel('Y Velocity (Å/fs)', fontweight='bold')  # Set the label for the Y-axis
        ax1.set_zlabel('Z Velocity (Å/fs)', fontweight='bold')  # Set the label for the Z-axis
        ax1.set_xlim3d(-1, 1)
        ax1.set_ylim3d(-1, 1)
        ax1.set_zlim3d(-1, 1)
        ax1.set_title(graph_scatter_title)
        
        # Set major ticks to show only every other tick
        ax1.set_xticks(np.arange(-1, 1.1, 0.5))
        ax1.set_yticks(np.arange(-1, 1.1, 0.5))
        ax1.set_zticks(np.arange(-1, 1.1, 0.5))

        # Set minor ticks
        ax1.xaxis.set_minor_locator(MultipleLocator(0.25))
        ax1.yaxis.set_minor_locator(MultipleLocator(0.25))
        ax1.zaxis.set_minor_locator(MultipleLocator(0.25))
        
        plt.legend()

        # Save the first figure
        plt.savefig(f'images/3d_scatter_plot_{graph_name_tag}.png')
        
        # Create a new figure for the second 3D plot
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111, projection='3d')  # Create another 3D subplot

        plt.hot()  # Use the 'hot' colormap

        # Calculate constant arrays for the projections of carbon
        cx = -np.ones_like(C_X)  # Constant X for YZ projection at the left edge of the plot
        cy = np.ones_like(C_Y)   # Constant Y for XZ projection at the top edge of the plot
        cz = -np.ones_like(C_Z)  # Constant Z for XY projection at the bottom edge of the plot
        
        # Calculate constant arrays for the projections of hydrogen
        c_hx = -np.ones_like(H_X)  # Constant X for YZ projection at the left edge of the plot
        c_hy = np.ones_like(H_Y)   # Constant Y for XZ projection at the top edge of the plot
        c_hz = -np.ones_like(H_Z)  # Constant Z for XY projection at the bottom edge of the plot

        # Scatter plots for the projections onto the XY, XZ, and YZ planes of carbon
        ax2.scatter(C_X, C_Y, cz, c='b', marker='.', lw=0, alpha=alpha)  # XY projection, color by Z
        ax2.scatter(C_X, cy, C_Z, c='b', marker='.', lw=0, alpha=alpha)  # XZ projection, color by negative Y
        ax2.scatter(cx, C_Y, C_Z, c='b', marker='.', lw=0, alpha=alpha)  # YZ projection, color by X
        
        # Scatter plots for the projections onto the XY, XZ, and YZ planes of hydrogen
        ax2.scatter(H_X, H_Y, cz, c='r', marker='.', lw=0, alpha=alpha)  # XY projection, color by Z
        ax2.scatter(H_X, cy, H_Z, c='r', marker='.', lw=0, alpha=alpha)  # XZ projection, color by negative Y
        ax2.scatter(cx, H_Y, H_Z, c='r', marker='.', lw=0, alpha=alpha)  # YZ projection, color by X

        # Set the limits of the second plot to be the same as the first plot
        ax2.set_xlim3d(-1, 1)
        ax2.set_ylim3d(-1, 1)
        ax2.set_zlim3d(-1, 1)
        
        # Set major ticks to show only every other tick
        ax2.set_xticks(np.arange(-1, 1.1, 0.5))
        ax2.set_yticks(np.arange(-1, 1.1, 0.5))
        ax2.set_zticks(np.arange(-1, 1.1, 0.5))

        # Set minor ticks
        ax2.xaxis.set_minor_locator(MultipleLocator(0.25))
        ax2.yaxis.set_minor_locator(MultipleLocator(0.25))
        ax2.zaxis.set_minor_locator(MultipleLocator(0.25))

        # Set axis labels for the second plot
        ax2.set_xlabel('X Velocity (Å/fs)', fontweight='bold')
        ax2.set_ylabel('Y Velocity (Å/fs)', fontweight='bold')
        ax2.set_zlabel('Z Velocity (Å/fs)', fontweight='bold')
        ax2.set_title(graph_projection_title)

        # Save the second figure
        plt.savefig(f'images/3d_projections_{graph_name_tag}.png')
        
        # Display the plots
        if self.show_plot:
            plt.show()
            
            
    def plot_2d_projections(self, normalize=False,graph_name_tag="",
                                    graph_xy_title="Carbon and Hydrogen X,Y Velocities",
                                    graph_xz_title="Carbon and Hydrogen X,Z Velocities",
                                    graph_yz_title="Carbon and Hydrogen Y,Z Velocities"):
        # Plot all of the 2-D NORMALIZED velocity projections
        self.plot_x_y_velocities(normalize=normalize,graph_name_tag=graph_name_tag,graph_xy_title=graph_xy_title)
        self.plot_x_z_velocities(normalize=normalize,graph_name_tag=graph_name_tag,graph_xz_title=graph_xz_title)
        self.plot_y_z_velocities(normalize=normalize,graph_name_tag=graph_name_tag,graph_yz_title=graph_yz_title)


def main():
    print("-=GENERATING NEWTON PLOT=-")
    newton_plot = NewtonPlot()
    data_mode = "quantum"
    user_input_mode = False
    
    if (data_mode.lower().startswith('q')):
        #QUANTUM INPUT FILE:
        input_file = 'newton_plot/moleculeFormations_14.csv'  
        graph_name_tag="quantum"

    if (data_mode.lower().startswith('c')):
        #CLASSICAL INPUT FILE:
        input_file = 'newton_plot/atom_info.csv'
        graph_name_tag="classical"

    
    if user_input_mode:
        input_file = input("Enter the path from current working directory to atom info file: ")
    print("Searching for input file: ", input_file)

    newton_plot.process_data(input_file)
   
    # 2-d velocity projections
    newton_plot.plot_2d_projections(normalize=False,
                                    graph_name_tag=graph_name_tag,
                                    graph_xy_title=f"Carbon and Hydrogen X,Y Velocities ({graph_name_tag})",
                                    graph_xz_title=f"Carbon and Hydrogen X,Z Velocities ({graph_name_tag})",
                                    graph_yz_title=f"Carbon and Hydrogen Y,Z Velocities ({graph_name_tag})")
    
    # 3-D scatter and projection plots    
    newton_plot.plot_3d_projections_1_limits(graph_name_tag=graph_name_tag,
                                             graph_scatter_title=f"3D Scatter Plot of Velocities ({graph_name_tag})",
                                             graph_projection_title=f"3D Projection of Velociteis ({graph_name_tag})")
    

if __name__ == '__main__':
    main()