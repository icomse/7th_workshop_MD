#!/bin/bash
#SBATCH --job-name=phase-test
#SBATCH --output=%j.o
#SBATCH --error=%j.e
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=RM-shared
#SBATCH --time=02:00:00
#SBATCH --account=see220002p

singularity exec --nv /ocean/projects/see220002p/shared/icomse_latest.sif python day2_phasediagram.py

