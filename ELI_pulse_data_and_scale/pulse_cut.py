def cut_pulse(input_file, output_file):
    # Read data from the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Process the data and multiply the 2nd and 4th column values by 2
    new_lines = []
    fs_num = 0.00
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue
        
        columns = line.strip().split('\t')
        print(columns)
        if len(columns) >= 4:
            if (fs_num <= (fs_to_cut + .001)):
                columns[1] = str(float(columns[1]))
                columns[3] = str(float(columns[3]))
            else:
                columns[1] = '0'
                columns[3] = '0'                

        new_line = '\t'.join(columns) + '\n'
        new_lines.append(new_line)
        fs_num += .001

    # Save the updated data to the output file
    with open(output_file, 'w') as file:
        file.writelines(new_lines)

# Input and output file paths
input_file = "lowf.txt"
output_file = "pulse_strong5_8_max_lf_cut.txt"
fs_to_cut = 8

# Call the function to perform the multiplication and save the updated data
cut_pulse(input_file, output_file)
print(f"File '{output_file}' has been created with the updated data.")
