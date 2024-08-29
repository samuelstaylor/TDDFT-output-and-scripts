file_name = "pulse7_5.dat"

# Initialize max absolute value to zero
max_abs_value = 0

# Open the file and iterate through lines
with open(file_name, 'r') as file:
    for line in file:
        # Split each line by tab to get columns
        columns = line.split('\t')
        # Check if there are at least two columns and the second one is a valid float
        if len(columns) >= 2:
            try:
                # Convert the second column to float
                value = float(columns[1])
                # Update max absolute value if the absolute value of the current value is greater
                if abs(value) > max_abs_value:
                    max_abs_value = abs(value)
            except ValueError:
                # Skip line if the second column is not a valid float
                pass

# Print the max absolute value
print("Max value in terms of magnitude:", max_abs_value)
