import csv
import numpy as np
import os


def parse_trajectory(filename):
    """Parses trajectory.xyz and returns frames as (time, coords) tuples."""
    frames = []
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    i = 0
    while i < len(lines):
        try:
            num_atoms = int(lines[i])
        except ValueError:
            i += 1
            continue

        header = lines[i + 1]
        if "time[fs]=" not in header:
            i += 1
            continue

        time = float(header.split("time[fs]=")[-1])

        coords = []
        for j in range(num_atoms):
            parts = lines[i + 2 + j].split()
            atom = parts[0]
            x, y, z = map(float, parts[1:])
            coords.append((atom, np.array([x, y, z])))

        frames.append((time, coords))
        i += num_atoms + 2

    return frames


def compute_velocities(frames):
    """Computes velocities between last two frames (excluding 'Xx' atoms)."""
    if len(frames) < 2:
        raise ValueError("File must contain at least two frames.")

    time1, coords1 = frames[-2]
    time2, coords2 = frames[-1]
    dt = time2 - time1

    filtered1 = [c for c in coords1 if c[0] != 'Xx']
    filtered2 = [c for c in coords2 if c[0] != 'Xx']

    if len(filtered1) != len(filtered2):
        raise ValueError("Mismatch in number of atoms between frames.")

    velocities = []
    for (_, pos1), (_, pos2) in zip(filtered1, filtered2):
        v = (pos2 - pos1) / dt
        velocities.append(v)

    velocities = np.array(velocities)
    speeds = np.linalg.norm(velocities, axis=1)
    return velocities, speeds


def export_csv(velocities, speeds, output_file="moleculeFormations.csv"):
    """Exports velocities and speeds to CSV."""
    rows = [
        ["X Velocity[A/fs]"] + list(velocities[:, 0]),
        ["Y Velocity[A/fs]"] + list(velocities[:, 1]),
        ["Z Velocity[A/fs]"] + list(velocities[:, 2]),
        ["Speed[A/fs]"] + list(speeds)
    ]

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def main():
    print("=== Molecule Velocity Calculator ===")
    traj_path = input("Enter the full path to your trajectory.xyz file: ").strip().strip('"').strip("'")

    if not os.path.isfile(traj_path):
        print(f"Error: File not found at '{traj_path}'")
        return

    print("\nReading trajectory file...")
    frames = parse_trajectory(traj_path)
    print(f"Found {len(frames)} frames. Using the last two for velocity calculations.")

    velocities, speeds = compute_velocities(frames)

    output_file = os.path.join(os.path.dirname(traj_path), "moleculeFormations.csv")
    export_csv(velocities, speeds, output_file)

    print(f"\n✅ Done! Exported results to:\n{output_file}")


if __name__ == "__main__":
    main()
