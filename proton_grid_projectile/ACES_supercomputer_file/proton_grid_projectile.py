import os
import shutil
import subprocess

# Function to update the dft.inp file
class Proton_grid_projectile():
    def __init__(self, d, n, m, grid_plane):
        self.num_atoms = None
        self.lines = []
        self.d = d  # distance between points on i to n axis
        # Number of iterations for i and j
        self.n = n  # Replace with your desired value for n
        self.m = m  # Replace with your desired value for m  
        self.grid_plane = grid_plane
        self.proton_line_index = None
        self.original_working_directory=os.getcwd()
        self.gs_path_line_index = None
        self.grid_dist_from_origin=0

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def read_original_dft_inp(self, file_path):
        with open(file_path, 'r') as file:
            self.lines = file.readlines()

        line_num = -1

        # Find the first integer in the file that is not preceded by a hashtag
        for line in self.lines:
            line_num += 1
            if not line.strip().startswith("#"):
                parts = line.split()
                for part in parts:
                    if part.isdigit():
                        self.num_atoms = int(part)
                        break
                if self.num_atoms is not None:
                    break

        if self.num_atoms is None:
            raise ValueError("No integer value found in the dft.inp file.")

        # Increment the number of atoms by 1
        self.num_atoms += 1
        self.lines[line_num] = f"{str(self.num_atoms)} 2 2 2\n"

        new_atom_line = "0.000000\t0.000000\t0.000000 1 1\n"
        # Find the correct insertion index
        for i in range(len(self.lines) - 2, -1, -1):
            stripped_line = self.lines[i].strip()
            if stripped_line and self.is_float(stripped_line.split()[0]):
                self.proton_line_index = i + 1
                break

        if self.proton_line_index is None:
            raise ValueError("No suitable insertion point found in the dft.inp file.")

        # Insert the new atom line at the found index
        self.lines.insert(self.proton_line_index, new_atom_line)

    def update_dft_inp(self, file_path, i, j, d):
        # Calculate the new atom position
        if self.grid_plane=="xy":
            new_atom_x = i * d
            new_atom_y = j * d / 2 - d
            new_atom_z = self.grid_dist_from_origin
        if self.grid_plane=="xz":
            new_atom_x = i * d
            new_atom_y = self.grid_dist_from_origin
            new_atom_z = j * d / 2 - d
        if self.grid_plane=="yz":
            new_atom_x = self.grid_dist_from_origin
            new_atom_y = i * d
            new_atom_z = j * d / 2 - d

        # Add the new atom to the end of the atom list
        new_atom_line = f"{new_atom_x: .6f}\t{new_atom_y: .6f}\t{new_atom_z: .6f} 1 1\n"
        self.lines[self.proton_line_index] = new_atom_line

        # Write the updated lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(self.lines)
            
    def read_original_control_inp(self, file_path):
        with open(file_path, 'r') as file:
            self.lines = file.readlines()
        
        # Find the correct insertion index
        for i in range(0, len(self.lines), 1):
            stripped_line = self.lines[i].strip()
            if stripped_line and stripped_line.lower().startswith("gs_path"):
                self.gs_path_line_index = i
                break

        if self.gs_path_line_index is None:
            raise ValueError("No suitable insertion point found in the dft.inp file.")

            
    def update_control_inp(self, file_path, gs_rel_path,i,j):
        gs_abs_path = os.path.abspath(gs_rel_path)
        new_atom_line = f"gs_path={gs_abs_path}{self.grid_plane[0]}{i}{self.grid_plane[1]}{j}\n"
        self.lines[self.gs_path_line_index] = new_atom_line

        # Write the updated lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(self.lines)
            
        

    def run(self, new_dir, i, j, execute=True):
        # Path to the job script
        job_script_path = os.path.join(new_dir, "job_script.sh")

        # Read the job script file
        with open(job_script_path, 'r') as file:
            job_script_lines = file.readlines()

        # Modify the job name line
        job_script_lines[1] = f"#SBATCH --job-name=C2H2_grid_{self.grid_plane[0]}{i}{self.grid_plane[1]}{j}\n"

        # Write the updated job script back to the file
        with open(job_script_path, 'w') as file:
            file.writelines(job_script_lines)

        new_abs_path = os.path.abspath(new_dir)
        # Calculate the relative path and count how many levels to go up
        relative_path = os.path.relpath(new_abs_path, start=self.original_working_directory)
        num_levels_up = relative_path.count(os.sep)  # Count the number of directory separators
    
        # Change directory to the new directory
        os.chdir(new_dir)

        # Optionally execute the job script using sbatch
        if execute:
            subprocess.run(["sbatch", "job_script.sh"])
        else:
            print(" 'sbatch job_script'")

        os.chdir("..")
        for _ in range(num_levels_up):
            os.chdir("..")


def ground_state_grid(d=0.6025963854,n=1,m=1,grid_plane="xy",grid_dist_from_origin=5,
                      original_gs_dir="proton_grid_projectile/C2H2/ground_state/C2H2_gs/",
                      grid_gs_name_form="proton_grid_projectile/C2H2/ground_state/C2H2_proton_",execute=False):
    
    proton_grid_projectile = Proton_grid_projectile(d, n, m, grid_plane)
    proton_grid_projectile.grid_dist_from_origin = grid_dist_from_origin
    original_dft_inp = original_gs_dir + "dft.inp"
    proton_grid_projectile.read_original_dft_inp(original_dft_inp)

    # Loop through i and j, create new directories, and update dft.inp
    for i in range(0, n + 1):
        for j in range(0, m + 1):
            # Create the new directory name
            new_dir = grid_gs_name_form + f"{proton_grid_projectile.grid_plane[0]}{i}{proton_grid_projectile.grid_plane[1]}{j}"

            # Check if the directory exists
            if not os.path.exists(new_dir):
                # Copy the original directory to the new directory
                shutil.copytree(original_gs_dir, new_dir)

            # Path to the dft.inp file in the new directory
            dft_inp_path = os.path.join(new_dir, "dft.inp")

            # Update the dft.inp file
            proton_grid_projectile.update_dft_inp(dft_inp_path, i, j, d)
            print(dft_inp_path, "created and updated.")

            # Run the job script in the new directory
            proton_grid_projectile.run(new_dir, i, j,execute=execute)

    print("Directories and dft.inp files have been successfully updated.")
        

def tddft_grid(d=1,n=1,m=1,grid_plane="xy",
               original_tddft_copy_dir = "proton_grid_projectile/C2H2/C2H2_copy/",
               grid_gs_name_form="proton_grid_projectile/C2H2/ground_state/C2H2_proton_",
               grid_tddft_name_form="proton_grid_projectile/C2H2/C2H2_proton_",execute=False):
    
    proton_grid_projectile = Proton_grid_projectile(d, n, m, grid_plane)

    original_control_inp = original_tddft_copy_dir + "control.inp"

    proton_grid_projectile.read_original_control_inp(original_control_inp)

    # Loop through i and j, create new directories, and update dft.inp
    for i in range(0, n + 1):
        for j in range(0, m + 1):
            # Create the new directory name
            new_dir = grid_tddft_name_form + f"{proton_grid_projectile.grid_plane[0]}{i}{proton_grid_projectile.grid_plane[1]}{j}"

            # Check if the directory exists
            if not os.path.exists(new_dir):
                # Copy the original directory to the new directory
                shutil.copytree(original_tddft_copy_dir, new_dir)

            # Path to the control.inp file in the new directory
            control_inp_path = os.path.join(new_dir, "control.inp")

            # Update the control.inp file
            proton_grid_projectile.update_control_inp(control_inp_path,grid_gs_name_form,i,j)
            print(control_inp_path, "created and updated.")

            # Run the job script in the new directory
            proton_grid_projectile.run(new_dir, i, j, execute=execute)

    print("Directories and dft.inp files have been successfully updated.")


def main():
    # NOTE: SAM -- make it so that boltzmann can be ran and generate the velocity.inp file for the copy file before copying.
    n=3
    m=4
    d=0.6025963854
    
    original_gs_dir="ground_state/C2H2_gs/"
    original_tddft_copy_dir="C2H2_copy/"
    grid_gs_name_form="ground_state/C2H2_proton_gs_" #the x{i}y{j} will be appended to the name
    grid_tddft_name_form="C2H2_proton_"
    grid_plane="yz"
    grid_dist_from_origin = 5
    
    run_mode="ground_state"
    #run_mode="tddft"
    
    execute=True
    
    # NOTE: CHECK THE FORMULA FOR THE ATOM GRID POSITIONS IN THE METHOD: update_dft_inp()
    
    if (run_mode.lower().startswith("g")):
        ground_state_grid(d=d,n=n,m=m,grid_plane=grid_plane,grid_dist_from_origin=grid_dist_from_origin,
                          original_gs_dir=original_gs_dir,grid_gs_name_form=grid_gs_name_form,execute=execute)
    elif (run_mode.lower().startswith("t")):
        tddft_grid(d=d,n=n,m=m,grid_plane=grid_plane,original_tddft_copy_dir=original_tddft_copy_dir,
                   grid_gs_name_form=grid_gs_name_form,grid_tddft_name_form=grid_tddft_name_form,execute=execute)

if __name__ == '__main__':
    main()
