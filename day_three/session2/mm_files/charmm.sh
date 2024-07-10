#!/bin/bash
#SBATCH --job-name=ff_parameters
#SBATCH --output=%j.o
#SBATCH --error=%j.e
#SBATCH --nodes=1
#SBATCH -n 16
#SBATCH --partition=RM-shared
#SBATCH --time=01:00:00
#SBATCH --account=see220002p

/ocean/projects/see220002p/shared/charmm/build/charmm -i step1_build.inp -o step1_build.out
/ocean/projects/see220002p/shared/charmm/build/charmm -i step2_water.inp -o step2_water.out
/ocean/projects/see220002p/shared/charmm/build/charmm -i step3_dihe.inp -o step3_dihe.out
