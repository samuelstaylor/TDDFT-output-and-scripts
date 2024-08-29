import matplotlib.pyplot as plt
import numpy as np


def determine_spread_factor(gdd_num):
    if (abs(gdd_num) > 900):
        return 7
    elif (abs(gdd_num) > 800):
        return 6
    elif (abs(gdd_num) > 600):
        return 5
    elif (abs(gdd_num) > 500):
        return 4
    elif (abs(gdd_num) > 400):
        return 3.5
    elif (abs(gdd_num) > 300):
        return 2.5
    elif (abs(gdd_num) > 200):
        return 2
    elif (abs(gdd_num) > 100):
        return 1.5
    return 1


def create_GDD_plots(gdd_num):
    # Read data from "time_axis(fs).txt"
    with open("time_axis(fs).txt", "r") as file:
        time_axis_data = [float(value) for value in file.readline().split(",")]

    # Read data from "0_GDD.txt"
    file_name = str(gdd_num) + "_GDD.txt"
    with open(file_name, "r") as file:
        e_field_data = [float(value) if value != 'NaN' else np.nan for value in file.readline().split(",")]


    # Set figure dimensions
    plt.figure(figsize=(13.64, 5.23))

    # Create a plot
    plt.plot(time_axis_data, e_field_data, linewidth=1)

    # Set labels and title
    plt.xlabel('Time (fs)', weight='bold')
    plt.ylabel('Electric Field (V/M)', weight='bold')
    title = "'Time dependent electric field (GDD=" + str(gdd_num) + " fs²)"
    plt.title(title, weight='bold')
    plt.xticks(fontweight='bold', )
    plt.yticks(fontweight='bold')

    plt.grid(True)
    #
    
    spread_factor = determine_spread_factor(gdd_num)
    plt.xlim(-(spread_factor*100) -1, (spread_factor*100)+1)
    

    output_file = "GDD=" + str(gdd_num) + ".png"
    plt.savefig(output_file)

    # Display the plot
    plt.close()
    
    
def main():
    gdd_num = 0
    create_GDD_plots(gdd_num)
    gdd_num += 20
    while (gdd_num <= 1000):
        create_GDD_plots(gdd_num)
        create_GDD_plots(-gdd_num)
        if (gdd_num < 200):
            gdd_num += 20
        else:
            gdd_num += 100


if __name__ == "__main__":
    main()