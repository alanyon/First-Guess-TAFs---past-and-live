#!/bin/bash -l
export TAF_START=2023110609
export OUT_DIR=/net/home/h04/alanyon/public_html/tafs
export PYTHONPATH=$PYTHONPATH:~alanyon/first_guess_TAFs/past_and_live/
export ML_DIR=/data/users/alanyon/tafs/improver/verification/20230805-20241004_ml/pickles
CODE_DIR=/home/h04/alanyon/first_guess_TAFs/past_and_live

# Activate cloned sss environment
conda activate default_clone

# Navigate to code directory and run code
cd ${CODE_DIR}
python master/taf_master.py

# Deactivate environment
conda deactivate
