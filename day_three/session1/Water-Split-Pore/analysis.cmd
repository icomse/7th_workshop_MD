#!/bin/bash
#SBATCH -A see220002p 
#SBATCH -p RM-shared
#SBATCH -n 8
#SBATCH -N 1
#SBATCH -t 2:00:00


module load intel
module load intel-mpi

mpirun -n ${SLURM_JOB_CPUS_PER_NODE} ../../../shared/LAMMPS/bin/lmp_mpi -in in.water-conf-prod-nvt -v inFileName relaxed-$1H2O-$2.dat.out -v prodSteps 25000 -v tag water-slit-pore-n$1-$2-analysis -log log-n$1-$2-a.log
