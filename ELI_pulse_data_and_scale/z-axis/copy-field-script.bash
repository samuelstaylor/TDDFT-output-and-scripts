#!/bin/bash

# List of pulse values
pulse_values=("7.5" "8" "8.5" "9" "9.5" "10" "10.5")
pulse_values=("7.5")

# Loop through each pulse value
for value in "${pulse_values[@]}"; do
    dir_name=$(printf "%.2f" "$value")  # Format directory name as 2 decimal places
    echo "Creating directory $dir_name..."

    # Copy the directory
    cp -r copy_field "$dir_name"

    # Copy and rename the pulse file
    pulse_file_path="../z-field/pulse_${value}.dat"
    if [ -f "$pulse_file_path" ]; then
        cp "$pulse_file_path" "$dir_name/copy_seed/pulse.dat"
        echo "Copied and renamed $pulse_file_path to $dir_name/copy_seed/pulse.dat"
    else
        echo "Warning: File $pulse_file_path not found!"
    fi
done
