'''
This script is created on 2020 Nov. 20th
It's used for finding all the datas named `*/Tract_2.csv` under the folder `datas`
and to generate the output file path for each csv file
'''

import os
import re

def get_base_dir():
    # ensure the script operates under the folder datas
    base_dir = os.getcwd()
    # if the user is running script alone
    if os.path.basename(base_dir) == 'scripts':
        base_dir = os.path.dirname(base_dir)
    base_dir = os.path.join(base_dir, 'datas')
    return base_dir

def find_tract_csv(filepath):
    # interate over all the subfolders
    valid_csv = []
    for root, subfolders, files in os.walk(filepath):
        for file in files:
            if file == 'Tract_2.csv':
                valid_csv.append(os.path.join(root, file))
    return valid_csv

def generate_outpath(csvpath):
    # use os.path.split to avoind conflict between windows and macos
    pattern = re.compile(r'\D+')
    detail = os.path.basename(os.path.dirname(csvpath))
    outfilename = pattern.findall(os.path.basename(os.path.dirname(os.path.split(csvpath)[0])))[0]
    return outfilename + detail + '.csv'

# base_dir = get_base_dir()
# valid_csv = find_tract_csv(base_dir)
# for index, csv in enumerate(valid_csv):
#     print(os.path.join(base_dir, (str(index) + generate_outpath(csv))))