import csv

def check_identical_lines(file_path):
    identical_lines_found = False
    with open(file_path, mode='r') as file:
        csv_reader = list(csv.reader(file))
        num_lines = len(csv_reader)
        
        for i in range(num_lines):
            for j in range(i + 1, num_lines):
                if len(csv_reader[i])!=0 and csv_reader[i] == csv_reader[j] and csv_reader[i][0][0].lower() == 'd':
                    identical_lines_found = True
                    print(f"Identical lines found: Line {i + 1} and Line {j + 1}")
        if not(identical_lines_found):
            print("No identical lines found.")

# Replace 'molFormations.csv' with the path to your CSV file if it's located elsewhere
check_identical_lines('histograms_stats_molecule_formation\\ch4\\moleculeFormations.csv')
