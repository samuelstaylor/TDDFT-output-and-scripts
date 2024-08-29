import matplotlib.pyplot as plt

def read_data_file(file_path):
    time_values = []
    x_values = []
    y_values = []
    z_values = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines[1:]:  # Skip the first row
        if not line.strip():
            continue

        columns = line.strip().split('\t')
        time_values.append(float(columns[0]))
        x_values.append(float(columns[1]))
        y_values.append(float(columns[2]))
        z_values.append(float(columns[3]))

    return time_values, x_values, y_values, z_values

def plot_data(time, x, y, z):
    plt.figure(figsize=(10, 6))
    plt.plot(time, x, label='X')
    plt.plot(time, y, label='Y')
    plt.plot(time, z, label='Z')

    plt.xlabel('Time (femto seconds)')
    plt.ylabel('E-field (V/A)')
    plt.title('Graph of E-field X, Y, and Z with respect to Time')
    plt.legend()
    plt.grid()

    plt.show()

if __name__ == '__main__':
    input_file = 'pulse.dat'

    time_values, x_values, y_values, z_values = read_data_file(input_file)
    plot_data(time_values, x_values, y_values, z_values)
