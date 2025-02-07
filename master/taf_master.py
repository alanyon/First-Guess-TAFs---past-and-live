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
    # File containing IMPROVER data
    pickle_file = f'{SORTED_DATA}/{TAF_START}/{ICAO}.pkl'

    # If no pivkle file exists, exit
    if not os.path.exists(pickle_file):
        print(f'No data found for {ICAO}. Exiting...')
        return

    # Load IMPROVER data from pickle file
    site_df = pd.read_pickle(f'{pickle_file}')

    # Generate TAF and collect bench
    nice_taf, ver_taf, bench = ge.taf_gen(site_df)

    # Save TAF types and bench to pickle file
    with open(f'{pickle_file}_tafs.pkl', 'wb') as f:
        pickle.dump([nice_taf, ver_taf, bench], f)


if __name__ == "__main__":

    main()
