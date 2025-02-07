"""
Master script calling all other modules relating to data extraction.

Functions:
    main: Main function.
"""
import os
import pandas as pd
import pickle

import data_extraction.bust_adjust as ba
import data_extraction.extract_sort_data as ex

# Define environment constants
TAF_START = os.environ['TAF_START']
SORTED_DATA = os.environ['SORTED_DATA']


def main():
    """
    Calls other modules to extract IMPROVER data.
    """
    # Extract all relevant IMPROVER data, and required TAF variables
    (param_dfs_missing_times,
     airport_info, taf_dts) = ex.get_imp_data(TAF_START)

    # Create directory to store extracted data if necessary
    pickle_dir = f'{SORTED_DATA}/{TAF_START}'
    if not os.path.exists(pickle_dir):
        os.makedirs(pickle_dir)

    # Filter data for each airport and collect
    for _, site_info in airport_info.iterrows():

        # Ignore defence for now
        if site_info['rules'] == 'defence':
            continue

        # Get data for airport
        site_df = ex.get_site_data(param_dfs_missing_times, site_info, taf_dts)

        # If no data found, move to next airport
        if site_df.empty:
            continue

        # Predict busts and adjust data accordingly
        site_df = ba.adjust_site_df(site_df)

        # For distinguishing London city long TAF from short TAF
        if site_info['airport_name'] == 'London City (long)':
            icao = 'EGLC_long'
        else:
            icao = site_info['icao']
        
        # Save data to pickle file
        with open(f'{pickle_dir}/{icao}.pkl', 'wb') as f:
            pickle.dump(site_df, f)


if __name__ == "__main__":
    main()
