import os
import subprocess

def submit_jobs(r_start, r_end, dir_name):
    # List of directories to process
    directories = []  # Add your directories here

    for r_val in range(r_start, r_end + 1):
        directories.append(dir_name + str(r_val))

    # Command to run in each directory
    command = "qsub job.pbs"

    # Iterate over each directory
    for directory in directories:
        # Check if the directory exists
        if os.path.isdir(directory):
            try:
                # Change to the directory
                os.chdir(directory)
                print("Changed to directory:", directory)

                # Execute the command
                result = subprocess.call(command, shell=True)
                
                # Check the result
                if result == 0:
                    print("Successfully executed 'qsub job.pbs' in", directory)
                else:
                    print("Failed to execute 'qsub job.pbs' in", directory, "with return code", result)
            
            except Exception as e:
                print("An error occurred in", directory, ":", e)

            finally:
                # Change back to the original directory
                os.chdir('..')
                print("Returned to parent directory")

        else:
            print("Directory", directory, "does not exist")

    print("Job submission process complete.")


def main():
    r_start = 2
    r_end = 13
    submit_jobs(r_start, r_end)
    
if __name__ == "__main__":
    main()
