import os
import shutil

def copy_and_update(r_start, r_end, dir_name, copy_dir):
    # Define the range of copies to create
    
    # Source directory to copy
    source_dir = copy_dir

    # File paths
    seeds_file = "seeds.txt"
    control_file_name = "control.inp"
    job_file_name = "job.pbs"

    # Read seeds from the seeds.txt file
    with open(seeds_file, 'r') as f:
        seeds = f.readlines()

    # Ensure there are enough seeds
    if len(seeds) < r_end:
        raise ValueError("Not enough seeds in seeds.txt for the number of copies requested.")

    # Iterate to create the specified number of copies
    for r_val in range(r_start, r_end + 1):
        # New directory name
        new_dir = dir_name + str(r_val)

        # Check if the directory already exists
        if os.path.exists(new_dir):
            print("Directory", new_dir, "already exists, skipping copy")
            return "Fail"
        else:
            # Copy the directory
            shutil.copytree(source_dir, new_dir)
            print("Copied", source_dir, "to", new_dir)

        # Get the seed value for this directory
        seed = seeds[r_val - 1].strip()  # Read the corresponding line and strip any extra whitespace
        print("Seed for", new_dir, ":", seed)

        # Path to the job.pbs and control.inp files in the new directory
        job_file_path = os.path.join(new_dir, job_file_name)
        control_file_path = os.path.join(new_dir, control_file_name)

        # Read the job.pbs file
        with open(job_file_path, 'r') as f1:
            lines_f1 = f1.readlines()

        # Read the control.inp file
        with open(control_file_path, 'r') as f2:
            lines_f2 = f2.readlines()

        # Modify the job name line in the job.pbs file
        with open(job_file_path, 'w') as f1:
            for line in lines_f1:
                if line.startswith("#PBS -N C2H6_r"):
                    line = "#PBS -N C2H6_r" + str(r_val) + "\n"
                f1.write(line)

        # Modify the ion_velocity_init_seed line in the control.inp file
        with open(control_file_path, 'w') as f2:
            for line in lines_f2:
                if line.startswith("ion_velocity_init_seed="):
                    line = "ion_velocity_init_seed=" + seed + "\n"
                f2.write(line)
        
        print("Updated job name in", job_file_path)
        print("Updated ion_velocity_init_seed in", control_file_path)

    print("All directories copied and updated.")
    return "Success"

def main():
    r_start = 3
    r_end = 12
    copy_and_update(r_start,r_end)
    
if __name__ == "__main__":
    main()