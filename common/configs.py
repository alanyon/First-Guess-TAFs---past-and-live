"""
Constants used throughout TAF generation code.
"""
# Define a sentinel value for errors in multiprocessing
ERROR_SENTINEL = "ERROR_OCCURRED"
IMPROVER_PARAMETERS = {
    'height_AGL_at_cloud_base_where_cloud_cover_2p5_oktas':
        {'data_type': 'percentiles',
         'short_name': 'cld_3',
         'units': 'ft',
         'fname_start': 'spotperc_extract_',
         'fname_start_alt': 'spotperc_extract_'},
    'height_AGL_at_cloud_base_where_cloud_cover_4p5_oktas':
        {'data_type': 'percentiles',
         'short_name': 'cld_5',
         'units': 'ft',
         'fname_start': 'spotperc_extract_',
         'fname_start_alt': 'spotperc_extract_'},
    'precip_rate_in_vicinity':
        {'data_type': 'percentiles',
         'short_name': 'precip_rate',
         'units': 'mm hr-1',
         'fname_start': 'spotperc_extract_',
         'fname_start_alt': 'spotperc_extract_'},
    'visibility_at_screen_level_in_vicinity':
        {'data_type': 'percentiles',
         'short_name': 'vis',
         'units': 'm',
         'fname_start': 'spotperc_extract_',
         'fname_start_alt': 'spotperc_extract_'},
    'weather_symbols-PT01H':
        {'data_type': 'deterministic',
         'short_name': 'sig_wx',
         'units': '1',
         'fname_start': 'weather_symbols_spot_',
         'fname_start_alt': 'latestspotperc_'},
    'wind_gust_at_10m_max-PT01H':
        {'data_type': 'percentiles',
         'short_name': 'wind_gust',
         'units': 'knots',
         'fname_start': 'spotperc_extract_',
         'fname_start_alt': 'spotperc_extract_'},
    'wind_direction_at_10m':
        {'data_type': 'deterministic',
         'short_name': 'wind_dir',
         'units': 'degrees',
         'fname_start': 'spotperc_extract_',
         'fname_start_alt': 'spotperc_extract_'},
    'wind_speed_at_10m':
        {'data_type': 'percentiles',
         'short_name': 'wind_mean',
         'units': 'knots',
         'fname_start': 'spotperc_extract_',
         'fname_start_alt': 'spotperc_extract_'},
    'temperature_at_screen_level':
        {'data_type': 'percentiles',
         'short_name': 'temp',
         'units': 'celsius',
         'fname_start': 'spotperc_extract_',
         'fname_start_alt': 'spotperc_extract_'},
    'lightning_flash_accumulation_in_vicinity-PT01H':
        {'data_type': 'probabilities',
         'short_name': 'lightning',
         'units': None,
         'fname_start': 'spot_extract_',
         'fname_start_alt': 'spot_extract_'}
}
PERCENTILES = [30, 40, 50, 60, 70]
PARAM_NAMES = {'wind': ['wind_dir', 'wind_mean', 'wind_gust'],
               'vis': ['vis', 'vis_cat', 'sig_wx'],
               'cld': ['cld_3', 'cld_5', 'cld_cat']}
WX_KEYS = {'wind': ['wind_dir', 'wind_mean', 'wind_gust'],
           'vis': ['vis', 'vis_cat', 'implied_sig_wx', 'sig_wx'],
           'cld': ['clds', 'cld_cat']}

# Dictionary giving significant weather TAF codes from Best Data codes
SIG_WX_DICT = {30: 'TSRA', 29: 'TSRA', 28: 'TSRA', 27: 'SN', 26: 'SHSN',
               25: 'SHSN', 24: '-SN', 23: '-SHSN', 22: '-SHSN', 21: 'SHGS',
               20: 'SHGS', 19: 'SHGS', 18: 'RASN', 17: 'SHRASN', 16: 'SHRASN',
               15: 'RA', 14: 'SHRA', 13: 'SHRA', 12: '-RA', 11: 'DZ',
               10: '-SHRA', 9: '-SHRA', 8: '', 7: '', 6: 'FG', 5: 'BR',
               4: '', 3: '', 2: '', 1: '', 0: ''}
NON_PRECIP_CODES = ['FZFG', 'FG', 'BR', 'HZ', '', 'NSW']
PRECIP_CODES = ['+SHSN', '+SN', '+SHRASN', '+RASN', '+TSRA', '+SHGS', '+SHRA',
                '+RA', '+DZ', 'SHSN', 'SN', 'SHRASN', 'RASN', 'TSRA', 'SHGS',
                'SHRA', 'RA', 'DZ', '-SHSN', '-SN', '-SHRASN', '-RASN',
                '-TSRA', '-SHGS', '-SHRA', '-RA', '-DZ']
TS_CODES = ['+TSRA', 'TSRA', '-TSRA']
HVY_CODES = ['+SHSN', '+SN', '+SHRASN', '+RASN', '+SHGS', '+SHRA', '+RA']

# Ordering priority of change groups
PRIORITY_DICT = {'base': 0, 'BECMG': 1, 'TEMPO': 2, 'PROB40': 3,
                 'PROB40 TEMPO': 4, 'PROB30': 5, 'PROB30 TEMPO': 6}

PROB_DICT = {'TEMPO': 100, 'PROB40': 40, 'PROB40 TEMPO': 40, 'PROB30': 30,
             'PROB30 TEMPO': 30}

# ML constants
PARAM_COLS = [
    'precip_rate_30.0', 'precip_rate_50.0', 'precip_rate_70.0', 
    'wind_dir_30.0', 'wind_dir_50.0', 'wind_dir_70.0', 'temp_30.0', 
    'temp_50.0', 'temp_70.0', 'wind_mean_30.0', 'wind_mean_50.0', 
    'wind_mean_70.0', 'wind_gust_30.0', 'wind_gust_50.0', 'wind_gust_70.0', 
    'month', 'day', 'hour', 'lead', 'vis_cat_30.0', 'vis_cat_50.0', 
    'vis_cat_70.0', 'cld_cat_30.0', 'cld_cat_50.0', 'cld_cat_70.0'
]

# Bench strings
BENCHES = ['civil_av1', 'civil_av2', 'civil_av3', 'heathrow_om',
           'heathrow_som', 'aldergrove', 'team_leader', 'defence']

# Add empty string to benches to cover all benches
ALL_BENCHES = BENCHES + ['']
