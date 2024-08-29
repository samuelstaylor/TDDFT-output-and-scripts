# Open the input file
mult_num = 5.5

with open('pulse1.dat', 'r') as infile:
    # Read the content of the file
    lines = infile.readlines()

# Process the lines and multiply the last three columns by 10
processed_lines = []
for line in lines[1:]:  # Skip the first line (header)
    values = line.split()
    multiplied_values = [float(values[0])] + [float(val) * mult_num for val in values[1:]]
    processed_lines.append('\t'.join(map(str, multiplied_values)))

# Write the processed data to the output file (pulse10.dat)
with open('pulse' + str(mult_num) + '.dat', 'w') as outfile:
    # Write the header
    outfile.write(lines[0])
    # Write the processed lines
    outfile.write('\n'.join(processed_lines))

print("Data has been processed and written to output file")
