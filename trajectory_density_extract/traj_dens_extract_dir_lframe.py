# Creates separate files for the last frame of every trajectory file in a directory
# Go to the directory where there script is located and type python3 <file name> to run the script.
import os
import re


def traj_filter_last_time_step(traj_input_file, traj_output_file):
    with open(traj_input_file, 'r') as infile:
        lines = infile.readlines()

    # Find the start index of the last time step
    start_index = 0
    for i, line in enumerate(lines):
        if line.startswith(" # iter"):
            start_index = i + 1

    # Write the last time step data to the output file
    with open(traj_output_file, 'w') as outfile:
        outfile.writelines(lines[start_index-2:])
        
def density_extract(dens_dat_input_file, dens_bov_input_file, dens_dat_output_file, dens_bov_output_file):
    with open(dens_dat_input_file, 'rb') as dat_infile:
        dat_lines = dat_infile.readlines()
    
    with open(dens_dat_output_file, 'wb') as dat_outfile:
        dat_outfile.writelines(dat_lines)
    
    with open(dens_bov_input_file, 'r') as bov_infile:
        bov_lines = bov_infile.readlines()
        
    for i, line in enumerate(bov_lines):
        if line.startswith(" DATA_FILE:"):
            bov_lines[i] = " DATA_FILE: " + str(dens_dat_output_file.split('/')[-1]) + "\n"
            break
    
    with open(dens_bov_output_file, 'w') as bov_outfile:
        bov_outfile.writelines(bov_lines)
    
#finds the density.bov and density.dat number for the final frame
def find_last_traj_dens_val(traj_input_filename):
    with open(traj_input_filename, 'r') as infile:
        lines = infile.readlines()

    # Find the start index of the last time step
    for line in lines:
        if line.startswith(" # iter"):
            match = re.search(r"# iter =\s*(\d+)", line)
            if match:
                iter_value = int(match.group(1))
                
    return iter_value


# Example usage

def main():
    start = 1
    end = 5
    input_path_form = "C4H10/kinked/pulse_7_5runs/pulse_7_5r"
    output_path_form = "C4H10/kinked/pulse_7_5runs/lframe_traj_dens/traj_dens_r"
    valid_num_runs = 0
    for i in range(start-1, end):
        r_val = str(i+1)
    
        traj_input_filename = input_path_form + r_val + "/trajectory.xyz"
        traj_output_filename = output_path_form + r_val + "/trajectory.xyz"
        
        iter_value = find_last_traj_dens_val(traj_input_filename)

        last_dens_val = "00" + str(int((iter_value)/500))

        
        if not os.path.exists(output_path_form + r_val):
            os.makedirs(output_path_form + r_val)
        
    
        dens_dat_input_filename = input_path_form + r_val + "/dens" + last_dens_val + ".dat"
        dens_dat_output_filename = output_path_form + r_val + "/dens" + last_dens_val + ".dat"
        dens_bov_input_filename = input_path_form + r_val + "/dens" + last_dens_val + ".bov"
        dens_bov_output_filename = output_path_form + r_val + "/dens" + last_dens_val + ".bov"
            
        traj_filter_last_time_step(traj_input_filename, traj_output_filename)
        density_extract(dens_dat_input_filename, dens_bov_input_filename, dens_dat_output_filename, dens_bov_output_filename)

        valid_num_runs += 1
        print("r", r_val, "...")
        
    print("Successfully completed for", valid_num_runs, "runs")

if __name__ == '__main__':
    main()