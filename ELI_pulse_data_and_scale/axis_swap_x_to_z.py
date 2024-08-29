# Read the original data file
with open('pulse7_5.dat', 'r') as file:
    lines = file.readlines()

# Open a new file to write the modified data
with open('pulse7_5_z.dat', 'w') as new_file:
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
