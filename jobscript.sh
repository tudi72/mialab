#!/bin/bash

# SLURM Settings
#SBATCH --job-name="MIALAB_SLURM"
#SBATCH --time=02:00:00
#SBATCH --mem-per-cpu=128G
#SBATCH --partition=epyc2
#SBATCH --qos=job_cpu
#SBATCH --mail-user=tudorita.zaharia@students.unibe.ch
#SBATCH --mail-type=ALL
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

# Load Anaconda3
module load Anaconda3
eval "$(conda shell.bash hook)"

# Load your environment
conda activate mialab

# Run your code
srun python3 pipeline.py
