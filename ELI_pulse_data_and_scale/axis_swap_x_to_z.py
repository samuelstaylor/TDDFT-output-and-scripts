# Read the original data file

input_file = r"ELI_pulse_data_and_scale\pulse6.dat"
output_file= r"ELI_pulse_data_and_scale\z-axis\pulse_6.0.dat"

with open(input_file, 'r') as file:
    lines = file.readlines()

# Open a new file to write the modified data
with open(output_file, 'w') as new_file:
    # Write the first line (number of entries) as is
    new_file.write(lines[0])
    
    # Process each subsequent line
    for line in lines[1:]:
        # Split the line into columns
        columns = line.split()
        
        # Swap the second and fourth columns
        columns[1], columns[3] = columns[3], columns[1]
        
        # Write the modified line to the new file
        new_file.write('\t'.join(columns) + '\n')
