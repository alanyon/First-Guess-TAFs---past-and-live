"""
Extracts operational TAFs from metDB and saves them out to text files.

Functions:
    main: Main function.
    get_op_taf: Reads in TAF from metdb.
    nice_format: Changes raw TAF into correctly formatted string.

Written by Andre Lanyon, March 2020.
"""
import os
from datetime import datetime, timezone
import re
import metdb
# Local imports
import common.configs as co

# Get environment variables
DATE_TIME = os.environ['TAF_START']
OUT_DIR = os.environ['OUT_DIR']
METDB_EMAIL = os.environ['METDB_EMAIL']

# Get valid date/time and valid data directory
VDT = datetime.strptime(DATE_TIME, '%Y%m%d%H')
VALID_TIME = VDT.strftime('%H')
VALID_DATE = VDT.strftime('%Y%m%d')
DATE_OUT_DIR = f'{OUT_DIR}/output/{VALID_DATE}'
# Time now
ISSUE_DT = datetime.now(timezone.utc)
# Get day of month of required issue time
DAY = int(DATE_OUT_DIR[-2:])

# Fix to increase the number of characters in the TAF string
metdb.subtypes.DTYPE_MAPS["TAFS"][u"TAF_RPT_TXT"]="S500"


def main():
    """
    Finds appropriate operationally issued issued TAFs and writes to 
    text files.
    """
    # Get latest TAFs from metdb
    latest_tafs = metdb.obs(METDB_EMAIL, 'TAFS', 
                            keywords=['PLATFORM EG', 'LATEST'],
                            elements=['ICAO_ID', 'TAF_RPT_TXT'])

    # Loop through benches, look in appropriate first guess output files 
    # and find relevant issued TAFs to compare against
    for bench in co.ALL_BENCHES:
 
        # Add in underscore for all except all benches file
        if bench:
            bench = bench + '_'

        # File name of first guess TAF file
        fg_taf_fname = f'{DATE_OUT_DIR}/{VALID_TIME}Z_{bench}improver.txt'

         # File name of issued TAFs to be displayed on html page
        is_taf_fname = f'{DATE_OUT_DIR}/{VALID_TIME}Z_{bench}issue.txt'

        # Only proceed if first guess TAF file exists
        if not os.path.exists(fg_taf_fname):
            continue

        # Read in generated TAF file
        with open(fg_taf_fname, 'r') as fg_taf_file:
            fg_taf_lines = fg_taf_file.readlines()

        # Get ICAO codes and airport names for all first guess TAFs
        icaos, names = [], []
        for ind, line in enumerate(fg_taf_lines):

            # Move on if not a TAF line
            if not 'TAF' in line:
                continue

            # Add ICAO and name to lists
            icao = line[4:8]
            icaos.append(icao)
            name = fg_taf_lines[ind-2][:-2]
            names.append(name)

            # Get operational TAF from metdb and format correctly
            op_taf = get_op_taf(latest_tafs, icao, name)

            # Now write taf to text file
            with open(is_taf_fname, 'a') as op_tafs_file:
                op_tafs_file.write(op_taf)


def get_op_taf(latest_tafs, icao, name):
    """
    Reads in TAF from metdb.

    Args:
        raw_tafs (bytes): Raw TAF bytes object
        icao (str): ICAO airport indicator
        name (str): Name of airport
    Returns:
        taf(str): Issued TAF    
    """
    # Get TAF for specific ICAO
    raw_taf = False
    for latest_taf in latest_tafs:
        if latest_taf[0].decode('utf-8').strip() == icao:
            raw_taf = latest_taf[1]
            break
    
    # Change to easily readable string
    taf = nice_format(raw_taf, icao, name)

    return taf


def nice_format(raw_taf, icao, name):
    """
    Changes raw TAF bytes object a string, in the same format as first 
    guess TAFs.

    Args:
        taf (bytes): Raw TAF bytes object
        icao (str): ICAO airport indicator
        name (str): Name of airport
    Returns:
        taf (str): Formatted TAF
    """
    # Return appropriate string if no TAF found
    no_taf_str = (f'\n{name}\n\nTAF for {icao} not available \n\n\n\n\n\n\n\n'
                  '\n\n\n')
    if not raw_taf:
        taf = no_taf_str
        return taf
    
    # Remove unnecessary info and change from bytes to string
    decoded_taf = raw_taf[44:].decode('utf-8')
    taf = '\nTAF {}='.format(decoded_taf)

    # Get start date and time of TAF found in metdb
    taf_start_day = int(taf[18:20])
    taf_start_time = int(taf[20:22])

    # Only continue if metdb time is for the same TAF period as first 
    # guess TAF
    # if taf_start_day == DAY and taf_start_time == int(VALID_TIME):
    if 1==1:
        # Remove whitespace at the end of the TAF
        taf = re.sub('  +', '', taf)

        # Write in same format as first guess tafs
        if 'BECMG' in taf:
            taf = taf.replace('BECMG', '\n     BECMG')

        # This part is done to distinguish TEMPOs with PROB30/40
        # TEMPOs
        if 'PROB30 TEMPO' in taf:
            taf = taf.replace('PROB30 TEMPO',
                                '\n     PROB30TEMPO')
        if 'PROB40 TEMPO' in taf:
            taf = taf.replace('PROB40 TEMPO',
                                '\n     PROB40TEMPO')
        if ' TEMPO' in taf:
            taf = taf.replace(' TEMPO', '\n     TEMPO')
        if 'PROB30 ' in taf:
            taf = taf.replace('PROB30 ', '\n     PROB30 ')
        if 'PROB40 ' in taf:
            taf = taf.replace('PROB40 ', '\n     PROB40 ')

        # This changes PROB30/40 TEMPOs back to how they should be
        if 'PROB30TEMPO' in taf:
            taf = taf.replace('PROB30TEMPO', 'PROB30 TEMPO')
        if 'PROB40TEMPO' in taf:
            taf = taf.replace('PROB40TEMPO', 'PROB40 TEMPO')

        # Put in extra lines for comparison to first guess TAFs
        num_extra_lines = 12 - taf.count('\n')
        taf += num_extra_lines * '\n'

        # Add in name
        taf = f'\n{name}\n{taf}'

    # Otherwise, return appropriate string
    else:
        taf = no_taf_str

    return taf


if __name__ == "__main__":
    main()
