import re

# Function to extract the second column of the nth INFOLINE
def extract_nth_infoline(filename,n):
    with open(filename, 'r') as file:
        count = 0
        for line in file:
            if line.startswith("INFOLINE:"):
                count += 1
                if count == n:
                    # Extract the second column from INFOLINE
                    infoline_data = re.split(r'\s+', line.strip())
                    second_column_value = float(infoline_data[2])  # Extract the second column
                    return second_column_value
    return None

def main():
    # List to store the second column values from nth INFOLINE
    print("-= STARTING AVG. IONIZATION CALC. =-")
    
    second_column_values = []
    r_start=1
    r_final=50
    nth_infoline_to_extract=30000
    #EDIT THE FILENAME FORM BELOW
    
    # Loop through r1 to r10 and extract the nth INFOLINE from each file
    for i in range(r_start, r_final+1):
        filename = f"C3H8_7_5r{i}/monitor.out"
        value = extract_nth_infoline(filename, nth_infoline_to_extract)
        print("  r =", i, "electron num found")
        if value is not None:
            second_column_values.append(value)
        else:
            print(f"Error: Could not find the {nth_infoline_to_extract}th INFOLINE in {filename}")
    
    # Check if values were found for all files
    if len(second_column_values) == len(range(r_start,r_final+1)):
        # Calculate the average of the values
        average_value = sum(second_column_values) / len(second_column_values)
        
        # Write the result to a text file
        with open("avg_ionization.txt", "w") as outfile:
            outfile.write(f"Average of the second column values from the nth INFOLINE (num electrons): {average_value}\n")
        
        print(f"Average value saved to avg_ionization.txt: {average_value}")
    else:
        print("Error: Could not calculate the average, some INFOLINE data is missing.")

if __name__ == '__main__':
    main()
