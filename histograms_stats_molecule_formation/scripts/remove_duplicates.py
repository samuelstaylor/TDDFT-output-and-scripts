import csv

# Read the file and process lines
def remove_duplicates(input_file, output_file):
    seen = set()
    unique_lines = []

    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            # Convert the line list to a tuple so it can be added to a set
            line_tuple = tuple(line)
            # Check if the line starts with 'd' and is a duplicate
            if line_tuple[0].startswith('d'):
                if line_tuple not in seen:
                    seen.add(line_tuple)
                    unique_lines.append(line)
            else:
                unique_lines.append(line)
    
    # Write the unique lines to the output file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(unique_lines)

# Usage
input_file = 'moleculeFormations.csv'
output_file = 'moleculeFormationsNoDup.csv'
remove_duplicates(input_file, output_file)
