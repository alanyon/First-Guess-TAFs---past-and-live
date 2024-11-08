"""
Master script calling all other modules relating to TAF generation.

Functions:
    main: Main function.
"""
import os
import pickle

import common.configs as co
import data_extraction.bust_adjust as ba
import data_extraction.extract_sort_data as ex
import generate.generate_taf as ge

# Define environment constants
TAF_START = os.environ['TAF_START']


def main():
    """
    Calls other modules to generate TAFs.
    """
    # Define path that data will be stored in
    d_file = f'{co.TEST_DIR}/{TAF_START}'

    # If data already extracted, use that
    if os.path.exists(d_file):
        with open(f'{co.TEST_DIR}/{TAF_START}', 'rb') as file_object:
            unpickler = pickle.Unpickler(file_object)
            param_dfs_missing_times, airport_info, taf_dts = unpickler.load()

    # Otherwise, need to extract data from MASS
    else:

        # Extract all relevant IMPROVER data, and required TAF variables
        (param_dfs_missing_times,
         airport_info, taf_dts) = ex.get_imp_data(TAF_START)

        # Save as csv file for testing
        with open(f'{co.TEST_DIR}/{TAF_START}', 'wb') as f_object:
            pickle.dump([param_dfs_missing_times, airport_info, taf_dts],
                        f_object)

    # Filter data for each airport and collect
    for _, site_info in airport_info.iterrows():

        # Ignore defence for now
        if site_info['rules'] == 'defence':
            continue

        # # FOR TESTING
        # if site_info['icao'] != 'EGEC':
        #     continue

        print(f'Processing {site_info["icao"]}...')

        # Get data for airport
        site_df = ex.get_site_data(param_dfs_missing_times, site_info, taf_dts)

        # If no data found, move to next airport
        if site_df.empty:
            continue

        # Predict busts and adjust data accordingly
        site_df = ba.adjust_site_df(site_df)

        # Generate TAF
        ge.taf_gen(site_df)


if __name__ == "__main__":
    main()
