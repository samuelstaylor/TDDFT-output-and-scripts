# Python script to convert Wolfram vectors to the desired format

def convert_wolfram_to_format(wolfram_file, output_file):
    with open(wolfram_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()
        
        # Write the number of points
        outfile.write(lines[0])
        
        # Write the header
        outfile.write(" # IP FORMATTED TO KALMAN CODE\n")
        
        # Process each vector line
        for line in lines[2:]:
            if line.strip():  # Skip empty lines
                parts = line.split(maxsplit=1)
                if len(parts) < 2:
                    continue  # Skip lines that don't have a label and vector
                label = parts[0]
                vector = parts[1].strip('{}').replace('}', '').split(',')
                # Ensure all components (x, y, z) are included
                if len(vector) == 3:  # Check if the vector has 3 components
                    try:
                        formatted_vector = [f"{float(v.strip()): .9E}" for v in vector]
                        outfile.write(f" {label:<4} {' '.join(formatted_vector)}\n")
                    except ValueError as e:
                        print(f"Error processing line: {line.strip()}")
                        print(f"Details: {e}")
                        continue


# Input and output file paths
wolfram_file = 'wolfram-to-cluster-format/wolfram-vectors.txt'
output_file = 'wolfram-to-cluster-format/converted_format.txt'

# Perform the conversion
convert_wolfram_to_format(wolfram_file, output_file)

print(f"Conversion complete. Output written to {output_file}")