#!/bin/bash
#SBATCH --job-name=phase-test
#SBATCH --output=%j-%a.o
#SBATCH --error=%j-%a.e
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=RM-shared
#SBATCH --time=00:30:00
#SBATCH --account=see220002p

singularity exec /ocean/projects/see220002p/shared/icomse_latest.sif python3 array_phase_diagram.py $SLURM_ARRAY_TASK_ID

