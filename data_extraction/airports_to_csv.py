"""
Script to save airport information required for TAF generation to a csv
file.
"""
import csv

# Site numbers, names, opening hours, TAF frequency, TAF length, TAF
# type and bench for each airport - starred lists are opening hours
TITLES = ['site_number', 'airport_name', 'icao', 's_week_start', 's_week_end',
          's_sat_start', 's_sat_end', 's_sun_start', 's_sun_end', 's_ph_start',
          's_ph_end', 'w_week_start', 'w_week_end', 'w_sat_start', 'w_sat_end',
          'w_sun_start', 'w_sun_end', 'w_ph_start', 'w_ph_end', 'taf_freq',
          'taf_len', 'rules', 'bench', 'country_code']
OPEN_24_7 = [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99]
SITES = [
    [3803, 'St Marys', 'EGHE',
     *[7, 18, 7, 18, None, None, 7, 18, 8, 17, 8, 18, None, None, 8, 17],
     3, 9, 'civil', 'civil_av1', 'ENG'],
    [352206, 'Lands End', 'EGHC',
     *[6, 18, 6, 18, None, None, 9, 18, 8, 18, 8, 12, None, None, 8, 18],
     3, 9, 'civil', 'civil_av1', 'ENG'],
    [3817, 'Newquay', 'EGHQ', *OPEN_24_7, 3, 9, 'civil', 'civil_av1', 'ENG'],
    [3844, 'Exeter', 'EGTE',
     *[9, 4, 9, 17, 9, 17, 9, 4, 10, 4, None, None, 12, 15, 9, 4],
     3, 9, 'civil', 'civil_av1', 'ENG'],
    [3862, 'Bournemouth', 'EGHH',
     *[5, 23, 5, 1, 5, 21, 5, 23, 6, 22, 6, 22, 6, 22, 6, 22],
     3, 9, 'civil', 'civil_av1', 'ENG'],
    [3, 'Southampton', 'EGHI',
     *[5, 22, 5, 22, 6, 22, 6, 22, 6, 23, 6, 23, 7, 23, 7, 23],
     3, 9, 'civil', 'civil_av1', 'ENG'],
    [99038, 'Gloucester', 'EGBJ',
     *[7, 19, 7, 19, 8, 19, 8, 19, 8, 20, 8, 19, 8, 19, 8, 19], 3, 9,
     'civil', 'civil_av1', 'ENG'],
    [3716, 'St Athan', 'EGSY',
     *[8, 16, 8, 16, 8, 16, 8, 16, 9, 17, 9, 17, 9, 17, 9, 17],
     3, 9, 'civil', 'civil_av1', 'ENG'],
    [9, 'Birmingham', 'EGBB', *OPEN_24_7, 6, 24, 'civil', 'civil_av1', 'ENG'],
    [18, 'East_Midlands', 'EGNX', *OPEN_24_7, 6, 24, 'civil', 'civil_av1',
     'ENG'],
    [3492, 'Norwich', 'EGSH', *OPEN_24_7, 3, 9, 'offshore', 'civil_av2',
     'ENG'],
    [3220, 'Carlisle', 'EGNC',
     *[6, 18, 6, 18, 6, 18, 6, 18, 9, 18, 9, 18, 9, 18, 9, 18],
     3, 9, 'civil', 'civil_av2', 'ENG'],
    [63, 'Caernarfon', 'EGCK', *OPEN_24_7, 3, 9, 'civil', 'civil_av2', 'WLS'],
    [3318, 'Blackpool', 'EGNH',
     *[6, 20, 6, 20, 6, 20, 6, 20, 7, 21, 7, 21, 7, 21, 7, 21],
     3, 9, 'offshore', 'civil_av2', 'ENG'],
    [98, 'Warton', 'EGNO',
     *[6, 18, None, None, None, None, 6, 18, 8, 19, None, None, None, None, 8,
       19],
     3, 9, 'civil', 'civil_av2', 'ENG'],
    [3321, 'Hawarden', 'EGNR',
     *[5, 20, 7, 18, 7, 18, 5, 20, 6, 21, 8, 19, 8, 19, 6, 21],
     3, 9, 'civil', 'civil_av2', 'WLS'],
    [37, 'Durham Teeside', 'EGNV',
     *[5, 21, 5, 21, 5, 21, 5, 21, 8, 21, None, None, 12, 20, 8, 21],
     3, 9, 'civil', 'civil_av2', 'ENG'],
    [22, 'Humberside', 'EGNJ', *OPEN_24_7, 3, 9, 'offshore', 'civil_av2',
     'ENG'],
    [3334, 'Manchester_Ringway', 'EGCC', *OPEN_24_7, 6, 30, 'civil',
     'civil_av2', 'ENG'],
    [3246, 'Newcastle', 'EGNT', *OPEN_24_7, 6, 24, 'civil', 'civil_av2',
     'ENG'],
    [301603, 'Doncaster', 'EGCN', *OPEN_24_7, 6, 24, 'civil', 'civil_av2',
     'ENG'],
    [26, 'Liverpool', 'EGGP', *OPEN_24_7, 6, 24, 'offshore', 'civil_av2',
     'ENG'],
    [25, 'Leeds Bradford', 'EGNM', *OPEN_24_7, 6, 24, 'civil', 'civil_av2',
     'ENG'],
    [3026, 'Stornoway', 'EGPO', *OPEN_24_7, 3, 9, 'civil', 'civil_av3', 'SCT'],
    [3022, 'Benbecula', 'EGPL',
     *[3, 17, 3, 15, 3, 18, 3, 18, 3, 18, 3, 15, 3, 18, 3, 18],
     3, 9, 'offshore', 'civil_av3', 'SCT'],
    [3100, 'Tiree', 'EGPU',
     *[6, 18, 6, 18, 14, 18, 6, 18, 6, 19, 6, 19, 14, 18, 6, 19],
     3, 9, 'civil', 'civil_av3', 'SCT'],
    [301886, 'Oban', 'EGEO',
     *[7, 17, 9, 17, 9, 17, 9, 17, 8, 17, 8, 14, 10, 17, 10, 17],
     3, 9, 'civil', 'civil_av3', 'SCT'],
    [3003, 'Sumburgh', 'EGPB', *OPEN_24_7, 3, 9, 'offshore', 'civil_av3',
     'SCT'],
    [3017, 'Kirkwall', 'EGPA', *OPEN_24_7, 3, 9, 'offshore', 'civil_av3',
     'SCT'],
    [3075, 'Wick', 'EGPC', *OPEN_24_7, 3, 9, 'offshore', 'civil_av3', 'SCT'],
    [23, 'Inverness', 'EGPE', *OPEN_24_7, 3, 9, 'offshore', 'civil_av3',
     'SCT'],
    [17, 'Dundee', 'EGPN',
     *[6, 20, 8, 16, 8, 20, 8, 21, 9, 21, 9, 16, 9, 21, 9, 21],
     3, 9, 'civil', 'civil_av3', 'SCT'],
    [3105, 'Islay', 'EGPI',
     *[3, 18, 3, 18, 3, 18, 3, 18, 3, 19, 3, 18, 3, 18, 3, 18],
     3, 9, 'civil', 'civil_av3', 'SCT'],
    [3111, 'Campbeltown', 'EGEC',
     *[7, 17, None, None, 16, 18, 7, 17, 8, 18, None, None, None, None, 8, 18],
     3, 9, 'civil', 'civil_av3', 'SCT'],
    [3091, 'Aberdeen', 'EGPD', *OPEN_24_7, 6, 24, 'offshore', 'civil_av3',
     'SCT'],
    [3160, 'Edinburgh', 'EGPH', *OPEN_24_7, 6, 24, 'civil', 'civil_av3',
     'SCT'],
    [3136, 'Prestwick', 'EGPK', *OPEN_24_7, 6, 24, 'civil', 'civil_av3',
     'SCT'],
    [3140, 'Glasgow', 'EGPF', *OPEN_24_7, 6, 24, 'civil', 'civil_av3', 'SCT'],
    [352417, 'Southend', 'EGMC', *OPEN_24_7, 3, 9, 'civil', 'heathrow_om',
     'ENG'],
    [5, 'London City', 'EGLC',
     *[3, 21, 3, 12, 3, 21, 3, 21, 3, 22, 3, 13, 3, 22, 3, 22],
     3, 9, 'civil', 'heathrow_om', 'ENG'],
    [5, 'London City (long)', 'EGLC', *OPEN_24_7, 6, 24, 'civil',
     'heathrow_om', 'ENG'],
    [350426, 'Biggin Hill', 'EGKB',
     *[5, 22, 7, 21, 7, 21, 7, 21, 6, 23, 8, 22, 8, 22, 8, 22],
     3, 9, 'civil', 'heathrow_om', 'ENG'],
    [3768, 'Farnborough', 'EGLF',
     *[6, 23, 7, 19, 7, 19, 7, 19, 7, 23, 8, 20, 8, 20, 8, 20],
     3, 9, 'civil', 'heathrow_om', 'ENG'],
    [3876, 'Shoreham', 'EGKA',
     *[7, 19, 8, 19, 8, 18, 7, 19, 8, 20, 9, 20, 9, 19, 9, 19],
     3, 9, 'civil', 'heathrow_om', 'ENG'],
    [6, 'Lydd', 'EGMD', *OPEN_24_7, 3, 9, 'civil', 'heathrow_om', 'ENG'],
    [12, 'Cambridge', 'EGSC',
     *[7, 17, None, None, None, None, 7, 17, 8, 18, 8, 18, 8, 18, 8, 18],
     3, 9, 'civil', 'heathrow_om', 'ENG'],
    [7, 'Cranfield', 'EGTC',
     *[7, 18, 8, 17, 8, 17, 8, 17, 8, 19, 9, 18, 9, 18, 9, 18],
     3, 9, 'civil', 'heathrow_om', 'ENG'],
    [127, 'Oxford', 'EGTK',
     *[5, 22, 5, 22, 5, 22, 5, 22, 6, 23, 6, 23, 6, 23, 6, 23],
     3, 9, 'civil', 'heathrow_om', 'ENG'],
    [3776, 'Gatwick', 'EGKK', *OPEN_24_7, 6, 30, 'civil', 'heathrow_om',
     'ENG'],
    [3772, 'Heathrow', 'EGLL', *OPEN_24_7, 6, 30, 'civil', 'heathrow_som',
     'ENG'],
    [350927, 'Londonderry', 'EGAE',
     *[6, 21, 6, 16, 10, 18, 6, 21, 6, 21, 6, 16, 10, 18, 6, 21],
     3, 9, 'civil', 'aldergrove', 'NIR'],
    [8, 'Belfast City', 'EGAC',
     *[5, 21, 5, 16, 5, 21, 5, 21, 5, 21, 5, 21, 5, 21, 5, 21],
     3, 9, 'civil', 'aldergrove', 'NIR'],
    [3917, 'Belfast International', 'EGAA', *OPEN_24_7, 6, 24, 'civil',
     'aldergrove', 'NIR'],
    [3683, 'Stansted', 'EGSS', *OPEN_24_7, 6, 30, 'civil', 'team_leader',
     'ENG'],
    [3715, 'Cardiff', 'EGFF', *OPEN_24_7, 6, 24, 'civil', 'team_leader',
     'ENG'],
    [11, 'Bristol', 'EGGD', *OPEN_24_7, 6, 24, 'civil', 'team_leader', 'ENG'],
    [300957, 'Luton', 'EGGW', *OPEN_24_7, 6, 24, 'civil', 'team_leader',
     'ENG'],
    [3649, 'Brize Norton', 'EGVN', *OPEN_24_7, 3, 18, 'defence', None, 'ENG'],
    [15, 'Cosford', 'EGWC', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3068, 'Lossiemouth', 'EGQS', *OPEN_24_7, 3, 18, 'defence', None, 'SCT'],
    [3171, 'Leuchars', 'EGQL', *OPEN_24_7, 3, 9, 'defence', None, 'SCT'],
    [3224, 'Spadeadam', 'EGOM', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3257, 'Leeming', 'EGXE', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3302, 'Valley', 'EGOV', *OPEN_24_7, 3, 9, 'defence', None, 'WLS'],
    [3373, 'Scampton', 'EGXP', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3377, 'Waddington', 'EGXW', *OPEN_24_7, 3, 18, 'defence', None, 'ENG'],
    [3391, 'Coningsby', 'EGXC', *OPEN_24_7, 3, 18, 'defence', None, 'ENG'],
    [3414, 'Shawbury', 'EGOS', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3462, 'Wittering', 'EGXT', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3482, 'Marham', 'EGYM', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3590, 'Wattisham', 'EGUW', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3658, 'Benson', 'EGUB', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3672, 'Northolt', 'EGWU', *OPEN_24_7, 3, 18, 'defence', None, 'ENG'],
    [3746, 'Boscombe Down', 'EGDM', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3749, 'Middle Wallop', 'EGVP', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3761, 'Odiham', 'EGVO', *OPEN_24_7, 3, 12, 'defence', None, 'ENG'],
    [3809, 'Culdrose', 'EGDR', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [3853, 'Yeovilton', 'EGDY', *OPEN_24_7, 3, 9, 'defence', None, 'ENG'],
    [301042, 'Woodvale', 'EGOW', *OPEN_24_7, 3, 9, 'defence', None, 'ENG']
]


def main():
    """
    Writes info to csv file.
    """
    csv_path = ('/net/home/h04/alanyon/first_guess_TAFs/improver/'
                'data_extraction/taf_info.csv')
    with open(csv_path, 'w', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(TITLES)
        for row in SITES:
            writer.writerow(row)


if __name__ == "__main__":
    main()
