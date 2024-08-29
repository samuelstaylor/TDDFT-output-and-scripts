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
        outfile.writelines(lines[start_index-2:])

# Example usage
for i in range(3):
    input_filename = f"C4H10/kinked/pulse_7_5r{i+1}/trajectory.xyz"
    output_filename = f"C4H10/kinked/lframe_traj/lframe_traj_r{i+1}.xyz"
    filter_last_time_step(input_filename, output_filename)
