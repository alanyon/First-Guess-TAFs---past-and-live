#!/bin/bash -l
CODE_DIR=~andre.lanyon/first_guess_tafs/past_and_live
export TAF_START=2025020700
export OUT_DIR=~andre.lanyon/public_html/tafs
export PYTHONPATH=$PYTHONPATH:$CODE_DIR
export ML_DIR=/data/users/andre.lanyon/tafs/ml_pickles
export SORTED_DATA=/data/users/andre.lanyon/tafs/sorted_data
export DATA_DIR=/data/scratch/andre.lanyon/tafs/improver_data
export MASS_DIR=moose:/adhoc/users/ppdev/OS45.2
export AIRPORT_INFO_FILE=$CODE_DIR/data_extraction/taf_info.csv
export ICAO=EGGD

# Activate cloned sss environment
conda activate default_clone

# Navigate to code directory and run code
cd ${CODE_DIR}
python master/extract_master.py
python master/taf_master.py
python master/save_tafs.py

# Deactivate environment
conda deactivate
