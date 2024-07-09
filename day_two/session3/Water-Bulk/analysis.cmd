#!/bin/bash
#SBATCH -A see220002p 
#SBATCH -p RM-shared
#SBATCH -n 8
#SBATCH -N 1
#SBATCH -t 2:00:00

module load intel-compiler
module load intel-mpi
module load intel-mkl

mpirun -n ${SLURM_JOB_CPUS_PER_NODE} /ocean/projects/see220002p/shared/LAMMPS/bin/lmp_mpi  -in in.$1-prod-general -v T_target $2 -v P_target $3 -v nSteps $4   -log log-$1-T$2-P$3-n$4.log
