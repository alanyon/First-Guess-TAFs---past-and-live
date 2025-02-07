"""
Master script calling all other modules relating to TAF generation.

Functions:
    main: Main function.
"""
import os
import pandas as pd
import pickle

import common.configs as co
import data_extraction.bust_adjust as ba
import data_extraction.extract_sort_data as ex
import generate.generate_taf as ge

# Define environment constants
TAF_START = os.environ['TAF_START']
SORTED_DATA = os.environ['SORTED_DATA']
ICAO = os.environ['ICAO']


def main():
    """
    Calls other modules to generate TAFs.
    """
    # Directory containing IMPROVER data files
    pickle_dir = f'{SORTED_DATA}/{TAF_START}'

    # If no directory exists, exit
    if not os.path.exists(pickle_dir):
        print(f'No data found for {TAF_START}. Exiting...')
        return

    # Load IMPROVER data from pickle file
    site_df = pd.read_pickle(f'{pickle_dir}/{ICAO}.pkl')

    # Generate TAF
    nice_taf, ver_taf, bench = ge.taf_gen(site_df)

    # Save to pickle files
    with open(f'{pickle_dir}/{ICAO}_tafs.pkl', 'wb') as f:
        pickle.dump([nice_taf, ver_taf, bench], f)


if __name__ == "__main__":

    main()
