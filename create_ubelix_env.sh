#!/bin/bash

# Load the Anaconda module
module load Anaconda3
eval "$(conda shell.bash hook)"

# Create a new environment for MIALab
conda create --name mialab python=3.11.0

# Activate the new environment
conda activate mialab

# Install the MIALab dependencies
pip install -r requirements.txt

pip show numpy 

pip show pymia