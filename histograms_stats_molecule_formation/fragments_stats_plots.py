import csv
import matplotlib.pyplot as plt
import numpy as np
import re
import os


# Do you want the histogram to display the number of charges opposed to valence electrons?
VALENCE_ELECTRONS_TO_CHARGES = True
INCLUDE_HYDROGEN = True

def custom_sort(val):
    hydrocarbon, electrons = val
    if hydrocarbon == "H":
        return (0, 0, 0)
    match = re.match(r"C(\d*)(H(\d*))?", hydrocarbon)
    if match:
        carbons = int(match.group(1)) if match.group(1) else 1
        hydrogens = 0 if match.group(2) is None else (int(match.group(3)) if match.group(3) else 1)
        if hydrogens == 0:
            return (1, carbons, 0)
        return (2, carbons, hydrogens)
    return (3, 0, 0)  # Default case, should not happen with valid input

def custom_sort_frags(hydrocarbon):
    if hydrocarbon == "H":
        return (0, 0, 0)
    match = re.match(r"C(\d*)(H(\d*))?", hydrocarbon)
    if match:
        carbons = int(match.group(1)) if match.group(1) else 1
        hydrogens = 0 if match.group(2) is None else (int(match.group(3)) if match.group(3) else 1)
        if hydrogens == 0:
            return (1, carbons, 0)
        return (2, carbons, hydrogens)
    return (3, 0, 0)  # Default case, should not happen with valid input

def process_fragments(filepath,line_skip_num=9):
     # line_skip_num is how many lines to skip to get to next frag and dens info

    fragments_data = {}
    
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        lines = list(reader)
    
    for i in range(0, len(lines),line_skip_num):
        fragments_line = lines[i]
        densities_line = lines[i + 1]

        fragments = [frag.split('[')[0].strip() for frag in fragments_line[1:] if frag.strip()]
        densities = [float(density.strip()) for density in densities_line[1:] if density.strip()]

        for fragment, density in zip(fragments, densities):
            if fragment not in fragments_data:
                fragments_data[fragment] = []
            fragments_data[fragment].append(density)
    print("Number of simulations:", (len(lines)/line_skip_num))
    return fragments_data

def valence_to_charges(fragment_charges):
        
    # Dictionary to store neutral molecule valence electron counts
    C_valence_electrons = 4
    H_electrons = 1

    neutral_counts_no_sub = {
        "C":    (1 * C_valence_electrons) + (0 * H_electrons),
        "H":    (0 * C_valence_electrons) + (1 * H_electrons),
        "CH":   (1 * C_valence_electrons) + (1 * H_electrons),
        "CH2":  (1 * C_valence_electrons) + (2 * H_electrons),
        "CH3":  (1 * C_valence_electrons) + (3 * H_electrons),
        "C2":   (2 * C_valence_electrons) + (0 * H_electrons),
        "C2H":  (2 * C_valence_electrons) + (1 * H_electrons),
        "C2H2": (2 * C_valence_electrons) + (2 * H_electrons),
        "C2H3": (2 * C_valence_electrons) + (3 * H_electrons),
        "C2H4": (2 * C_valence_electrons) + (4 * H_electrons),
        "C2H5": (2 * C_valence_electrons) + (5 * H_electrons),
        "C3":   (3 * C_valence_electrons) + (0 * H_electrons),
        "C3H":  (3 * C_valence_electrons) + (1 * H_electrons),
        "C3H2": (3 * C_valence_electrons) + (2 * H_electrons),
        "C3H3": (3 * C_valence_electrons) + (3 * H_electrons),
        "C3H4": (3 * C_valence_electrons) + (4 * H_electrons),
        "C3H5": (3 * C_valence_electrons) + (5 * H_electrons),
        "C3H6": (3 * C_valence_electrons) + (6 * H_electrons),
        "C3H7": (3 * C_valence_electrons) + (7 * H_electrons),
        "C4":   (4 * C_valence_electrons) + (0 * H_electrons),
        "C4H":  (4 * C_valence_electrons) + (1 * H_electrons),
        "C4H2": (4 * C_valence_electrons) + (2 * H_electrons),
        "C4H3": (4 * C_valence_electrons) + (3 * H_electrons),
        "C4H4": (4 * C_valence_electrons) + (4 * H_electrons),
        "C4H5": (4 * C_valence_electrons) + (5 * H_electrons),
        "C4H6": (4 * C_valence_electrons) + (6 * H_electrons),
        "C4H7": (4 * C_valence_electrons) + (7 * H_electrons),
        "C4H8": (4 * C_valence_electrons) + (8 * H_electrons),
        "C4H9": (4 * C_valence_electrons) + (9 * H_electrons),
        "C4H10":(4 * C_valence_electrons) + (10 * H_electrons)

    }

    #neutral_counts= {}
    
    
    # for molecule in neutral_counts_no_sub:
    #     neutral_counts[subscript_numbers(molecule)] = neutral_counts_no_sub[molecule]

    # Calculate charges and store them in a dictionary
    for key, array in fragment_charges.items():
        updated_values = [neutral_counts_no_sub[key] - x for x in array]
        fragment_charges[key] = updated_values

def subscript_numbers(molecule):
    subscript_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return molecule.translate(subscript_map)

def rev_subscript_numbers(molecule):
    reverse_map = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
    return molecule.translate(reverse_map)

def plot_charge_states(fragments_data_passed,fig_name="frag_charge_states.png"):
    include_hydrogen_in_this_plot = False
    
    fragments_data = fragments_data_passed.copy()
    if not(include_hydrogen_in_this_plot):
        fragments_data.pop("H")
        
    # Fragment names
    fragments = list(fragments_data.keys())
    
    # Calculate the minimum and maximum electron to set up the bins
    min_charge = min(min(charge) for charge in fragments_data.values() if charge)
    max_charge = max(max(charge) for charge in fragments_data.values() if charge)
    min_charge = ((min_charge * 10) // 1 ) / 10 #round charges off to 1 decimal
    max_charge = ((max_charge * 10) // 1 ) / 10

    eps=1E-9 #eps to include the charges that are equal to the max_charge
    bin_size = .2
    bins = np.arange(min_charge, max_charge + bin_size + eps, bin_size)  # Bins of size 0.2 up to the maximum electron
    labels = [f"{bins[i]:.1f} to {bins[i+1]:.1f}" for i in range(len(bins) - 1)]
    colors = plt.cm.viridis(np.linspace(0, 1, len(labels)))

    total_num_fragments = 0
    for key in fragments_data.values():
        for _ in key:
            total_num_fragments += 1

    # Prepare data for plotting
    bar_data = {label: [] for label in labels}  # Initialize dictionary for each label
    fragments = list(fragments_data.keys())
    for fragment in fragments:
        # Bin the data for each fragment
        counts, _ = np.histogram(fragments_data[fragment], bins=bins)
        for label, count in zip(labels, counts):
            bar_data[label].append((count/total_num_fragments) * 100)

    # Plotting
    bar_width = 0.8
    r = np.arange(len(fragments))  # the label locations
    bottoms = np.zeros(len(fragments))

    plt.figure(figsize=(12, 8))
    legend_labels = []
    legend_colors = []
    total_counts = np.zeros(len(fragments))


    for label, color in zip(labels, colors):
        if any(bar_data[label]):  # Check if any count is greater than zero
            bars = plt.bar(r, bar_data[label], color=color, edgecolor='white', width=bar_width, bottom=bottoms, label=label)
            bottoms += np.array(bar_data[label])  # Update the bottoms for the stacked bar
            total_counts += np.array(bar_data[label])  # Track total counts for each fragment
            legend_labels.append(label)
            legend_colors.append('black')

    # Add the labels for the total counts
    for x, total in zip(r, total_counts):
        if total > 0:
            plt.text(x, total, f'{float(total):.1f}', ha='center', va='bottom', fontweight='bold')

    # Set ylim to leave whitespace at the top
    max_y = max(total_counts)
    plt.ylim(0, max_y * 1.1)  # Increase y limit by 10%

    #plt.xlabel('Fragments', fontsize=16, fontweight='bold')
    plt.ylabel('Frequency (%)', fontsize=16, fontweight='bold')
    #plt.title('Fragment Product Frequency and Charge States', fontweight='bold', fontsize=20)
    
    sorted_fragments = sorted(fragments, key=custom_sort_frags)
    subscripted_fragments = [subscript_numbers(frag) for frag in sorted_fragments]
    plt.xticks(r, subscripted_fragments, rotation=45, fontsize='12',fontweight='bold')
    plt.yticks(fontweight='bold', fontsize='12')
    if legend_labels:  # Add legend only if there are labels to show
        plt.legend(title='Fragments Charge States', loc='upper right', title_fontsize='13', fontsize='11', labels=legend_labels, labelcolor=legend_colors)

    plt.tick_params(axis='y', direction='in')

    plt.tight_layout(pad=1.0)  # Adjust layout with a bit more padding
    plt.savefig(fig_name, format='png')  # Save as PNG
    plt.close()

def plot_fragment_counts_and_averages_log(fragments_data, fig_name = 'frag_charge_averages.png', log_scale=True):
    # Extract fragment names
    fragments = list(fragments_data.keys())
    counts = []
    averages = []
    total_num_frags = 0
    
    # Calculate counts and averages for each fragment
    for fragment in fragments:
        # if fragment == "H":
        #     counts.append(0)
        # else:
        #     count = len(fragments_data[fragment])
        #     counts.append(count)
        #     total_num_frags += count

        count = len(fragments_data[fragment])
        counts.append(count)
        total_num_frags += count
        
        charge_sum = sum(fragments_data[fragment])
        num_frag = len([x for x in fragments_data[fragment] if x != 0])
        if num_frag != 0:
            average = charge_sum / num_frag
            averages.append(average)
    
    frequency = [(x / total_num_frags) * 100 for x in counts]
    counts = frequency

    # Create the bar chart
    plt.figure(figsize=(10, 6))

    sorted_fragments = sorted(fragments, key=custom_sort_frags)

    sorted_counts = [counts[fragments.index(frag)] for frag in sorted_fragments]
    sorted_averages = [averages[fragments.index(frag)] for frag in sorted_fragments]
    
    bars_counts = plt.bar(sorted_fragments, sorted_counts, color='tab:blue', edgecolor='black', linewidth=.1, label='Frequency')
    abs_averages = [abs(x) for x in sorted_averages]
    bars_averages = plt.bar(sorted_fragments, abs_averages, color='#b0dce4', edgecolor='black', linewidth=.1, bottom=sorted_counts, label='Average Charge')

    #plt.xlabel('Fragments', fontsize=12, fontweight='bold')
    plt.ylabel('Frequency (%)', fontsize=12, fontweight='bold')
    plt.title('Fragment Product Frequency and Average Charge', fontsize=14, fontweight='bold')
    
    # Convert fragment names to their subscripted versions
    subscripted_fragments = [subscript_numbers(frag) for frag in sorted_fragments]
    plt.xticks(rotation=45, ha="right", fontsize=10, fontweight='bold')
    plt.xticks(ticks=range(len(subscripted_fragments)), labels=subscripted_fragments)

    plt.yticks(fontweight='bold')
    #plt.legend(loc='upper right')

    # Adding labels within each bar for counts
    for bar, count in zip(bars_counts, sorted_counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height - height * 0.05, f'{count:.1f}', ha='center', va='top', fontweight='bold', color='white', fontsize=7)

    # Adding labels on top of each bar for averages
    for bar, average, count in zip(bars_averages, sorted_averages, sorted_counts):
        plt.text(bar.get_x() + bar.get_width() / 2, count + abs(average), f'{average:.1f}', ha='center', va='bottom', fontweight='bold', color='black', fontsize=7)
    
    # Adding horizontal lines at each tick mark
    for tick in plt.gca().get_yticks():
        plt.axhline(y=tick, color='gray', linestyle='--', linewidth=0.5)
    
    # Apply log scale to y-axis if log_scale is True
    if log_scale:
        plt.yscale('log')
    
    plt.ylim(0.1, 100)
    plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
    plt.savefig(fig_name, format='png')  # Save as PNG
    plt.close()


def plot_fragment_counts_and_averages_two_ax(fragments_data, fig_name='frag_charge_averages.png',hydrogen_charge_scale_factor=10):
    # Extract fragment names
    fragments = list(fragments_data.keys())
    counts = []
    averages = []
    total_num_frags = 0
    hydrogen_counts = 0
    hydrogen_average = 0
    
    r = np.arange(len(fragments))  # the label locations
    
    # Calculate counts and averages for each fragment
    for fragment in fragments:
        count = len(fragments_data[fragment])
        counts.append(count)
        total_num_frags += count
        
        if fragment == "H":
            hydrogen_counts += count
        
        charge_sum = sum(fragments_data[fragment])
        num_frag = len([x for x in fragments_data[fragment] if x != 0])
        if num_frag != 0:
            average = charge_sum / num_frag
            averages.append(average)
            if fragment == "H":
                hydrogen_average = average
    
    print("Total number of fragments", total_num_frags)
    frequency = [(x / total_num_frags) * 100 for x in counts]
    hydrogen_frequency = (hydrogen_counts / total_num_frags) * 100
    counts = frequency
    print("Total frequency of fragments",sum(counts))
    
    sorted_fragments = sorted(fragments, key=custom_sort_frags)
    
    # Create / filter data for the graphs
    sorted_counts = [counts[fragments.index(frag)] for frag in sorted_fragments]
    sorted_averages = [averages[fragments.index(frag)] for frag in sorted_fragments]
    
    # Separate hydrogen data
    hydrogen_index = sorted_fragments.index("H") if "H" in sorted_fragments else None
    if hydrogen_index is not None:
        hydrogen_count = sorted_counts[hydrogen_index]
        hydrogen_average_charge = sorted_averages[hydrogen_index]
        sorted_counts[hydrogen_index] = 0  # Set to zero to exclude from ax1
        sorted_averages[hydrogen_index] = 0
    else:
        hydrogen_count = 0
        hydrogen_average_charge = 0
    
    # Create the bar chart
    fig, ax1 = plt.subplots(figsize=(10, 6))  # Create y-axis (Hydrogen axis) first
    
    #ax1.set_xlabel('Fragments', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Hydrogen Frequency (%)', fontsize=12, fontweight='bold', color='tab:orange')
    max_hydrogen_height = hydrogen_count + abs(hydrogen_average_charge)
    ax1.set_ylim(0, max_hydrogen_height * 1.15)

    # Plot hydrogen bar on the primary y-axis
    if hydrogen_index is not None:
        hydrogen_bars_count = ax1.bar(["H"], [hydrogen_count], color='tab:orange', edgecolor='black',linewidth=.1, label='Hydrogen Frequency')
        hydrogen_bars_average = ax1.bar(["H"], [abs(hydrogen_average_charge) * hydrogen_charge_scale_factor], 
                                        color='#ffc240', edgecolor='black',linewidth=.1, bottom=[hydrogen_count], label='Hydrogen Average Charge')

        # Adding labels within the hydrogen bar for counts
        for bar in hydrogen_bars_count:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2, height - height * 0.05, f'{hydrogen_count:.1f}', ha='center', va='top', fontweight='bold', color='white', fontsize=7)

        # Adding labels on top of the hydrogen bar for averages
        for bar in hydrogen_bars_average:
            ax1.text(bar.get_x() + bar.get_width() / 2, hydrogen_count + (abs(hydrogen_average_charge) * hydrogen_charge_scale_factor), f'{hydrogen_average_charge:.1f}', ha='center', va='bottom', fontweight='bold', color='black', fontsize=7)


    # Create primary y-axis for other fragments
    ax2 = ax1.twinx()

    bars_counts = ax2.bar(sorted_fragments, sorted_counts, color='tab:blue', edgecolor='black',linewidth=.1,label='Fragment Frequency')
    abs_averages = [abs(x) for x in sorted_averages]
    bars_averages = ax2.bar(sorted_fragments, abs_averages, color='#b0dce4', edgecolor='black',linewidth=.1,bottom=sorted_counts, label='Fragment Average Charge')

    ax2.set_ylabel('Frequency (%)', fontsize=12, fontweight='bold', color='tab:blue')
    #ax2.set_title('Fragment Product Frequency and Average Charge', fontsize=14, fontweight='bold')
    plt.xticks(r, fragments, rotation=45, fontweight='bold')
    subscripted_fragments = [subscript_numbers(frag) for frag in sorted_fragments]
    ax2.set_xticks(range(len(subscripted_fragments)))
    ax1.set_xticklabels(subscripted_fragments, rotation=45, ha="right", fontsize=10, fontweight='bold')
    
    ax1.tick_params(axis='y', direction='in')
    ax2.tick_params(axis='y', direction='in')


    ax2.tick_params(axis='y', which='both', labelsize=10, labelcolor='black', direction='in', length=5, width=1, colors='black', grid_color='gray', grid_alpha=0.5)
    
    # Adding labels within each bar for counts
    for bar, count in zip(bars_counts, sorted_counts):
        height = bar.get_height()
        if height != 0:
            ax2.text(bar.get_x() + bar.get_width() / 2, height - height * 0.05, f'{count:.1f}', ha='center', va='top', fontweight='bold', color='white', fontsize=7)

    # Adding labels on top of each bar for averages
    for bar, average, count in zip(bars_averages, sorted_averages, sorted_counts):
        height = bar.get_height()
        if height != 0:
            ax2.text(bar.get_x() + bar.get_width() / 2, count + abs(average), f'{average:.1f}', ha='center', va='bottom', fontweight='bold', color='black', fontsize=7)
    
    

    
    # Set y-axis limits for the other fragments
    non_hydrogen_counts = [count for frag, count in zip(sorted_fragments, sorted_counts) if frag != "H"]
    max_count = max(non_hydrogen_counts) if non_hydrogen_counts else 0
    ax2.set_ylim(0, max_count * 1.25)  # A little over the highest bar

   
    #Add both legends to the top right without overlapping
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    combined_handles = handles1 + handles2
    combined_labels = labels1 + labels2
    ax1.legend(combined_handles, combined_labels, loc='upper right', bbox_to_anchor=(1, 1))

    fig.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
    plt.savefig(fig_name, format='png')  # Save as PNG
    plt.close()
    
    
import matplotlib.pyplot as plt
import numpy as np

def plot_hydrogen(fragments_data, fig_name='hydrogen_charge_distribution.png'):
    hydrogen_key = "H"
    bin_size = 0.05

    if hydrogen_key in fragments_data:
        hydrogen_charges = fragments_data[hydrogen_key]
        
        # Calculate the total number of hydrogen charges
        total_hydrogen = len(hydrogen_charges)
        
        # Create the histogram
        plt.figure(figsize=(10, 6))
        counts, bins, patches = plt.hist(hydrogen_charges, bins=np.arange(min(hydrogen_charges), max(hydrogen_charges) + bin_size, bin_size), edgecolor='black', color='tab:blue', density=True)

        # Convert counts to percentage
        counts = counts * bin_size * 100
        
        sum = 0
        # Plot the histogram with the frequency percentages
        for count, patch in zip(counts, patches):
            patch.set_height(count)
            sum += count
            plt.text(patch.get_x() + patch.get_width() / 2, count, f'{count:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        print("Sum of frequencies for hydrogen histogram:", sum)
        
        # Set x-ticks and labels for each bar
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        plt.xticks(bin_centers, [f'{center:.2f}' for center in bin_centers], rotation=45, fontsize=10)
        plt.tick_params(axis='y', direction='in')


        plt.xlabel('Charge', fontsize=12, fontweight='bold')
        plt.ylabel('Hydrogen Frequency (%)', fontsize=12, fontweight='bold')
        plt.title('Distribution of Hydrogen Charge States', fontsize=14, fontweight='bold')
        plt.ylim(0, max(counts) * 1.1)

        plt.tight_layout()
        plt.savefig(fig_name, format='png')
        plt.close()
    else:
        print("No hydrogen data available.")
       

def plot_hydrogen_boxplot(fragments_data, fig_name):
    hydrogen_key = "H"

    if hydrogen_key in fragments_data:
        hydrogen_charges = fragments_data[hydrogen_key]
        
        # Create the horizontal boxplot
        plt.figure(figsize=(10, 6))
        boxprops = dict(facecolor='white', color='black')
        whiskerprops = dict(color='black')
        capprops = dict(color='black')
        medianprops = dict(color='black')
        flierprops = dict(marker='.', color='black', markersize=5)

        plt.boxplot(hydrogen_charges, vert=False, patch_artist=True, notch=True, 
                    boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops, 
                    medianprops=medianprops, flierprops=flierprops)

        plt.xlabel('Charge', fontsize=12, fontweight='bold')
        plt.title('Boxplot of Hydrogen Charge States', fontsize=14, fontweight='bold')
        
        # Remove y-axis tick marks and labels
        plt.gca().yaxis.set_ticks([])
        plt.gca().set_yticklabels([])

        plt.ylim(.5, 1.5)

        plt.xticks(fontweight='bold')
        plt.tight_layout()
        plt.savefig(fig_name, format='png')
        plt.close()
    else:
        print("No hydrogen data available.")


def main():
    print("-= GENERATING STATISTIC PLOTS =-")
    # Usage
    input_file_path = 'histograms_stats_molecule_formation/x_polarized/moleculeFormations.csv'
    print("READING IN DATA FROM FILE:",input_file_path)
    fragments_data = process_fragments(input_file_path,line_skip_num=3)
    
    # Set the output file directory to match the input file's directory
    output_file_directory = os.path.dirname(input_file_path)
    
    if VALENCE_ELECTRONS_TO_CHARGES:
        valence_to_charges(fragments_data)
    
    fragments_data = dict(sorted(fragments_data.items(), key=custom_sort))
    
    # Create plots with file names including the output directory
    plot_charge_states(fragments_data, fig_name=os.path.join(output_file_directory, "frag_charge_states.png"))
    plot_fragment_counts_and_averages_log(fragments_data, fig_name=os.path.join(output_file_directory, "frag_charge_averages_log.png"), log_scale=True)
    plot_fragment_counts_and_averages_two_ax(fragments_data, fig_name=os.path.join(output_file_directory, "frag_charge_averages_two_axes.png"),
                                                                                   hydrogen_charge_scale_factor=6)
    plot_hydrogen(fragments_data, fig_name=os.path.join(output_file_directory, 'hydrogen_charge_distribution.png'))
    plot_hydrogen_boxplot(fragments_data, fig_name=os.path.join(output_file_directory, 'hydrogen_charge_boxplot.png'))
    
    print("SUCCESSFULLY CREATED ALL FIGURES IN:",output_file_directory)
    
if __name__ == '__main__':
    main()
