#!/bin/bash -l
#
#SBATCH -n 1
#SBATCH -t 05:00:00
#SBATCH -J FluTeIn
#SBATCH -p cosma7
#SBATCH -A dp004
#SBATCH --exclusive

# Load Module
module unload python
module load python/3.6.5

# Run
python3 create_ew_input.py

