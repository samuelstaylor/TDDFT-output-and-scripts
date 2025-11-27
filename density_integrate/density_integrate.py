import numpy as np
import struct
import sys
from dataclasses import dataclass
from typing import List, Tuple, Optional

# ----------------------------
# Data structures
# ----------------------------

@dataclass
class Atom:
    symbol: str
    pos: np.ndarray  # shape (3,)


@dataclass
class Molecule:
    atoms: List[Atom]
    density_sum: float = 0.0  # accumulates raw density (per-volume unit)

    # Axis-aligned bounding box
    min_bounds: np.ndarray = None
    max_bounds: np.ndarray = None

    def __post_init__(self):
        self.recalculate_aabb()

    def recalculate_aabb(self):
        coords = np.array([a.pos for a in self.atoms])
        self.min_bounds = coords.min(axis=0)
        self.max_bounds = coords.max(axis=0)

    def increment_density_sum(self, amount: float):
        self.density_sum += amount

    def contains_point(self, pt: np.ndarray, radius: float) -> bool:
        # Equivalent to bounds.Contains(pt, radius)
        return np.all(pt >= (self.min_bounds - radius)) and np.all(pt <= (self.max_bounds + radius))

    def get_electron_density(self, voxel_volume: float) -> float:
        # Mirrors Molecule::GetElectronDensity(volume) => densitySum * volume
        return self.density_sum * voxel_volume


# ----------------------------
# XYZ readers
# ----------------------------

def iter_xyz_blocks(filename: str):
    """
    Yield (time_fs, atoms) for each block in trajectory.xyz.
    Assumes format:
      n_atoms
      # iter = ...  time[fs]= ...
      <n_atoms lines>
    """
    with open(filename, "r") as f:
        lines = [ln.rstrip("\n") for ln in f.readlines()]

    i = 0
    while i < len(lines):
        # Read number of atoms
        if not lines[i].strip():
            i += 1
            continue
        try:
            n_atoms = int(lines[i].strip())
        except ValueError:
            break
        header = lines[i + 1]
        time_fs = 0.0
        if "time[fs]=" in header:
            try:
                time_fs = float(header.split("time[fs]=")[1])
            except Exception:
                time_fs = 0.0
        atoms: List[Atom] = []
        for j in range(i + 2, i + 2 + n_atoms):
            parts = lines[j].split()
            symbol = parts[0]
            x, y, z = map(float, parts[1:])
            atoms.append(Atom(symbol=symbol, pos=np.array([x, y, z], dtype=float)))
        yield time_fs, atoms
        i = i + 2 + n_atoms


def read_xyz_at_time(filename: str, target_time_fs: float, tol: float = 1e-6) -> Tuple[List[Atom], float]:
    """
    Get atoms at the specified time from trajectory.xyz.
    If exact match not found within tol, raises ValueError.
    """
    closest: Optional[Tuple[float, List[Atom]]] = None
    min_diff = float("inf")
    for time_fs, atoms in iter_xyz_blocks(filename):
        diff = abs(time_fs - target_time_fs)
        if diff < min_diff:
            min_diff = diff
            closest = (time_fs, atoms)
        if diff <= tol:
            return atoms, time_fs
    if closest is None:
        raise ValueError("No blocks found in trajectory.xyz")
    if min_diff <= tol:
        return closest[1], closest[0]
    raise ValueError(f"No block at time {target_time_fs} fs (closest found {closest[0]} fs, diff {min_diff})")


# ----------------------------
# BOV + DAT readers
# ----------------------------

def bov_filename_for_time(base_path: str, time_fs: float) -> str:
    """
    Match the C++ naming convention:
      ending = "00" + std::to_string(uint32_t(step * 2)) + ".bov"
    Example: time 0.0 -> dens00000.bov, time 0.5 -> dens00001.bov
    """
    index = int(round(time_fs * 2.0))
    return f"{base_path}dens{index:05d}.bov"


def read_bov_header(filename: str):
    """Parse BOV header to extract grid info and byte offset."""
    params = {}
    with open(filename, "r") as f:
        for line in f:
            if ":" in line:
                key, val = line.split(":", 1)
                params[key.strip()] = val.strip()
    data_file = params["DATA_FILE"]
    nx, ny, nz = map(int, params["DATA_SIZE"].split())
    ox, oy, oz = map(float, params["BRICK_ORIGIN"].split())
    sx, sy, sz = map(float, params["BRICK_SIZE"].split())
    byte_offset = int(params.get("BYTE_OFFSET", "0"))
    # Prepend base path if DATA_FILE is just the filename
    # The C++ constructor does this; we emulate by joining based on BOV location.
    if "/" in filename or "\\" in filename:
        base_dir = filename[:max(filename.rfind("/"), filename.rfind("\\")) + 1]
        if not (data_file.startswith(base_dir)):
            data_file = base_dir + data_file
    return data_file, (nx, ny, nz), (ox, oy, oz), (sx, sy, sz), byte_offset


def read_dat_binary(filename: str, grid_size: Tuple[int, int, int], byte_offset: int) -> np.ndarray:
    """
    Read binary density values from .dat with optional byte offset.

    C++ DataGrid::GetFlatIndex:
      idx = z * (nx * ny) + y * nx + x
    So x is fastest, then y, then z. Reshape to (nz, ny, nx) then transpose to (nx, ny, nz).
    """
    nx, ny, nz = grid_size
    npts = nx * ny * nz
    with open(filename, "rb") as f:
        if byte_offset > 0:
            f.seek(byte_offset)
        data = f.read(4 * npts)
    arr = np.frombuffer(data, dtype="<f4")  # little-endian float
    if arr.size != npts:
        raise ValueError(f"Expected {npts} density values, got {arr.size}")
    arr = arr.reshape((nz, ny, nx))         # [z, y, x] with x fastest
    densities = np.transpose(arr, (2, 1, 0))  # -> [x, y, z]
    return densities


def generate_grid_coords(nx: int, ny: int, nz: int,
                         ox: float, oy: float, oz: float,
                         sx: float, sy: float, sz: float):
    """
    Node-centered grid coordinates exactly like BOV::GenerateGrid:
      dx = size / (N - 1)
      coord[i] = origin + i * dx
    """
    dx = sx / (nx - 1)
    dy = sy / (ny - 1)
    dz = sz / (nz - 1)
    x = ox + np.arange(nx) * dx
    y = oy + np.arange(ny) * dy
    z = oz + np.arange(nz) * dz
    gx, gy, gz = np.meshgrid(x, y, z, indexing="ij")
    return (gx, gy, gz), (dx, dy, dz)


# ----------------------------
# Density processing (C++ logic)
# ----------------------------

def process_density_point_radius(pt: np.ndarray, density: float,
                                 molecules: List[Molecule], density_radius: float):
    # Equivalent to DensityHelper::ProcessDensityPoint
    claimers = []
    for mol in molecules:
        if mol.contains_point(pt, density_radius):
            for atom in mol.atoms:
                if np.linalg.norm(pt - atom.pos) <= density_radius:
                    claimers.append(mol)
                    break
    if len(claimers) == 0:
        return
    dens_part = density / len(claimers)
    for mol in claimers:
        mol.increment_density_sum(dens_part)


def process_density_point_cody(pt: np.ndarray, density: float,
                               molecules: List[Molecule], max_density_distance: float):
    # Equivalent to DensityHelper::ProcessDensityPointCodyMethod
    closest_mol = None
    min_dist = np.inf
    for mol in molecules:
        for atom in mol.atoms:
            d = np.linalg.norm(pt - atom.pos)
            if d <= min_dist:
                min_dist = d
                closest_mol = mol
    if min_dist <= max_density_distance and closest_mol is not None:
        closest_mol.increment_density_sum(density)


def process_density_grid(densities: np.ndarray, grid_coords: Tuple[np.ndarray, np.ndarray, np.ndarray],
                         molecules: List[Molecule],
                         mode: str,
                         density_radius: float,
                         max_density_distance: float):
    nx, ny, nz = densities.shape
    gx, gy, gz = grid_coords
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                pt = np.array([gx[i, j, k], gy[i, j, k], gz[i, j, k]], dtype=float)
                rho = densities[i, j, k]  # raw density (per volume unit)
                if mode == "radius":
                    process_density_point_radius(pt, rho, molecules, density_radius)
                elif mode == "cody":
                    process_density_point_cody(pt, rho, molecules, max_density_distance)
                else:
                    raise ValueError(f"Unknown mode: {mode}")


# ----------------------------
# Orchestration for arbitrary time
# ----------------------------

def compute_atom_charges(base_path: str, target_time_fs: float,
                         mode: str = "cody",
                         maximum_density_distance: float = 10.0,
                         density_radius: float = 1.0):
    xyz_path = base_path + "trajectory.xyz"
    # Read atoms at requested time
    atoms, time_fs = read_xyz_at_time(xyz_path, target_time_fs, tol=1e-6)

    # One atom per molecule (per-atom densities)
    molecules = [Molecule([a]) for a in atoms]

    # Find matching BOV and DAT
    bov_path = bov_filename_for_time(base_path, time_fs)
    data_file, grid_size, origin, size, byte_offset = read_bov_header(bov_path)
    densities = read_dat_binary(data_file, grid_size, byte_offset)
    (gx, gy, gz), (dx, dy, dz) = generate_grid_coords(*grid_size, *origin, *size)
    voxel_volume = dx * dy * dz  # matches BOV::GetGridVolume

    # Process density points
    process_density_grid(densities, (gx, gy, gz), molecules,
                         mode=mode,
                         density_radius=density_radius,
                         max_density_distance=maximum_density_distance)

    # Convert accumulated per-volume to electrons via voxel volume
    per_atom_electrons = [mol.get_electron_density(voxel_volume) for mol in molecules]
    total_electrons = float(np.sum(per_atom_electrons))
    grid_total_electrons = float(np.sum(densities) * voxel_volume)

    return atoms, time_fs, per_atom_electrons, total_electrons, grid_total_electrons


def main():
    # Usage: python script.py [time_fs]
    # Defaults to 0.0 fs if not provided
    target_time_fs = 0.0
    if len(sys.argv) >= 2:
        target_time_fs = float(sys.argv[1])

    base_path = "./data/c2h2-traj-dens/"

    atoms, time_fs, per_atom_electrons, total_electrons, grid_total_electrons = compute_atom_charges(
        base_path=base_path,
        target_time_fs=target_time_fs,
        mode="cody",
        maximum_density_distance=10.0,
        density_radius=3.0
    )

    # Output in moleculeFormations.csv style
    print("C2H2_run,", ", ".join([f"{a.symbol}[{i}]" for i, a in enumerate(atoms)]) + ",")
    print("Densities,", ", ".join([f"{e:.12f}" for e in per_atom_electrons]) + ",")
    print("Time[fs],", ", ".join([f"{time_fs:.6f}" for _ in atoms]) + ",")
    print("Density Sum,", f"{total_electrons:.12f}")
    print(f"# Grid-integrated electrons (sanity check): {grid_total_electrons:.12f}")

if __name__ == "__main__":
    main()