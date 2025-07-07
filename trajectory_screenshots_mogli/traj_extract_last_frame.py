import os

# RUN THIS FILE IN ACES / CLUSTER TO GET XYZ FILES OF THE LAST FRAME

def filter_last_time_step(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Find the start index of the last time step
    start_index = 0
    for i, line in enumerate(lines):
        if line.startswith(" # iter"):
            start_index = i + 1

    # Write the last time step data to the output file
    with open(output_file, 'w') as outfile:
        outfile.writelines(lines[start_index - 2:])


# Example usage
for i in range(65):
    input_filename = f"r{i + 1}/trajectory.xyz"
    output_filename = f"last_frame/trajectory_r{i + 1}.xyz"

    # Check if the input file exists
    if os.path.isfile(input_filename):
        filter_last_time_step(input_filename, output_filename)
    else:
        print(f"File not found: {input_filename}. Skipping...")