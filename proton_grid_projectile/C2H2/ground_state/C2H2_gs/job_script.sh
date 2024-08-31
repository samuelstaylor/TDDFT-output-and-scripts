#!/bin/bash
#SBATCH --job-name=C2H2_gs
# # SBATCH --account=account_name
#SBATCH --partition=cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=5GB
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=167:59:59

module load intel/2023.07
module load GCC/13.2.0
module load FFTW/3.3.10

dftdir=/scratch/user/u.st199789/dft/mask_volkov_3d/release

cd $SLURM_SUBMIT_DIR

$dftdir/dft > output 2> error