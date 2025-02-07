"""
Scrip to save TAFs to txt files.

Functions:
    main: Main function.
"""
import os
import pickle

# Define environment constants
TAF_START = os.environ['TAF_START']
SORTED_DATA = os.environ['SORTED_DATA']
OUT_DIR = os.environ['OUT_DIR']


def main():
    """
    Calls other modules to extract IMPROVER data.
    """
    # Get date and time from TAF_START
    taf_date, taf_time = TAF_START[:-2], TAF_START[-2:]

    # Define directory paths
    pickle_dir = f'{SORTED_DATA}/{TAF_START}'
    output_dir = f'{OUT_DIR}/output/{taf_date}'

    # If no directory exists, exit
    if not os.path.exists(pickle_dir):
        print(f'No data found for {TAF_START}. Exiting...')
        return

    # Create a new output directory and update html page if necessary
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        update_html(taf_date)

    # Loop through all files in directory
    for file in os.listdir(pickle_dir):

        # Only need the taf files
        if 'tafs' not in file:
            continue

        # Load TAF in both formats and bench
        with open(f'{pickle_dir}/{file}', 'rb') as f:
            nice_taf, ver_taf, bench = pickle.load(f)

        # Write to txt files
        bench_file = f'{output_dir}/{taf_time}Z_{bench}_improver.txt'
        ver_file = f'{output_dir}/{taf_time}Z_verification.txt'

        # Write out to text files
        with open(bench_file, 'a', encoding='utf-8') as b_file:
            b_file.write(nice_taf)
        with open(ver_file, 'a', encoding='utf-8') as v_file:
            v_file.write(ver_taf)


def update_html(date):
    """
    Updates html file displaying TAF output.

    Args:
        date (str): Date of TAFs.
    Returns:
        None
    """
    # File name of html file
    fname = f'{OUT_DIR}/html/taf_output.html'

    # Read in existing file, getting 2 lists of lines from the file, split
    # where an extra line is required
    with open(fname, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    first_lines = lines[:-86]
    last_lines = lines[-86:]

    # Edit html file and append/edit the required lines
    first_lines[-1] = first_lines[-1].replace(' selected="selected"', '')
    first_lines.append('                    <option selected="selected" '
                       f'value="{date}">{date}</option>\n')
    last_lines[-31] = last_lines[-31].replace(last_lines[-31][31:39], date)
    last_lines[-19] = last_lines[-19].replace(last_lines[-19][31:39], date)

    # Concatenate the lists together
    new_lines = first_lines + last_lines

    # Re-write the lines to a new file
    with open(fname, 'w', encoding='utf-8') as o_file:
        for line in new_lines:
            o_file.write(line)


if __name__ == "__main__":
    main()
