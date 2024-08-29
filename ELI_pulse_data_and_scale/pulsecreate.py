def read_file(file_path):
    with open(file_path, "r") as file:
        data = [float(value) for value in file.readline().split(",")]
    return data

def write_pulse_dat(time_data, gdd_data, output_file):
    with open(output_file, 'w') as file:
        number_of_points = len(time_data)
        file.write(f"{number_of_points}\n")
        for time, gdd in zip(time_data, gdd_data):
            file.write(f"{time:.3f}\t{gdd}\t0\t0\n")
            
            
def convert_M_to_A(e_field_data):
    meters_in_one_angstrom = 1e-10
    i = 0
    while i < len(e_field_data):
        if str(e_field_data[i]).lower() == 'nan':
            e_field_data[i] = 0
        e_field_data[i] = e_field_data[i] * meters_in_one_angstrom
        i +=1


def initialize_time(time_axis_data):
    shift_val = time_axis_data[0]
    i = 0
    while i < len(time_axis_data):
        time_axis_data[i] = time_axis_data[i] - shift_val
        i +=1


def shift_pulse(data, shift_factor):
    data = data[shift_factor:]
    return data

def main():
    # Replace 'GDD_0.txt' and 'time_axis(fs).txt' with your actual file paths
    gdd_file_path = 'GDD_text_files/0_GDD.txt'
    time_axis_file_path = 'time_axis(fs).txt'
    output_file_path = '0_GDD_pulse.dat'

    # Read files and create data lists
    time_axis_data = read_file(time_axis_file_path)    
    e_field_data = read_file(gdd_file_path)
    
    initialize_time(time_axis_data)
    convert_M_to_A(e_field_data)
    
    SHIFT = True
    if (SHIFT):
        index_shift_factor = 8180 
        index_shift_factor -=2
        time_axis_data = shift_pulse(time_axis_data, index_shift_factor)
        e_field_data = shift_pulse(e_field_data, index_shift_factor)
        initialize_time(time_axis_data)
    
    # write the lists to the file in tab-seperated table format
    write_pulse_dat(time_axis_data, e_field_data, output_file_path)

    print(f"Data has been written to {output_file_path}")

if __name__ == "__main__":
    main()