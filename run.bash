#!/bin/bash -l
#SBATCH -n 1                     # Number of cores
#SBATCH -t 0-24:00:00            # Runtime in D-HH:MM:SS
#SBATCH -J FluteEW
#SBATCH -o ./logs/jobid_%j.out  # File to which STDOUT will be written
#SBATCH -e ./logs/jobid_%j.err  # File to which STDERR will be written
#SBATCH -p cosma7               # Partition to submit to
#SBATCH -A dp004
#SBATCH --exclusive

module load intel_comp/2018 intel_mpi/2018

./flute config-northeast

exit
