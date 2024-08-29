#NOT PROPERLY WORKING
import csv

# Read the file and process lines
def remove_duplicates(input_file, output_file):
    seen = set()
    unique_lines = []
    line_num=0

    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            line_num+=1
            # Convert the line list to a tuple so it can be added to a set
            line_tuple = tuple(line)
            # Check if the line starts with 'd' and is a duplicate
            if line_tuple[0].lower().startswith('d'):
                if line_tuple not in seen:
                    seen.add(line_tuple)
                    unique_lines.append(line)
                else:
                    print("Duplicate found at line:",line_num)
            else:
                unique_lines.append(line)
    
    # Write the unique lines to the output file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(unique_lines)
        
    if (line_num==len(unique_lines)):
        print('No duplicate lines found.')


# Usage
input_file = 'histograms_stats_molecule_formation\scripts\moleculeFormations.csv'
output_file = 'histograms_stats_molecule_formation\scripts\moleculeFormationsND.csv'
remove_duplicates(input_file, output_file)
