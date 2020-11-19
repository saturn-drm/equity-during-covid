'''
This script is created on 2020 Nov. 18th
It's meant for cleaning the first-hand csv datas downloaded from ArcGIS webserver
after cleaning, all gis data should contain 2894 rows.
'''


import pandas
import json
import os

import findpath


# define parent class for all data
class DataSet():

    # file path
    def __init__(self, filepath):
        self.filepath = filepath

    # join dataframes
    @staticmethod
    def join_data(sourcedata, joiningdata, setindex, joinindex, subset=None, inplace=False):
        return sourcedata.join(joiningdata.set_index(setindex), on=joinindex).dropna(subset=subset, inplace=inplace)
    
    # change the columns orders
    @staticmethod
    def rearrange_col(data, collist):
        for i in range(len(collist)):
            coltomove = data.pop(collist[i])
            data.insert(i + 1, collist[i], coltomove)
        return data

    # save data
    def save_csv_data(self, data):
        data.to_csv(self.filepath, index=False)


# define child class for csv data
class CsvData(DataSet):

    # read file
    def read_file(self):
        self.data = pandas.read_csv(self.filepath)
    
    # drop the columns of Margin of Error
    def drop_Margin_of_Error(self):
        col_to_drop = []
        for column in self.data.columns:
            if 'Margin of Error' in column:
                col_to_drop.append(column)
        self.data = self.data.drop(columns=col_to_drop, inplace=False)
    
    # select the rows for NY
    def select_NY(self, colname='State', colcontent='New York'):
        self.data = self.data[self.data[colname] == colcontent]


# define child class for geojson data
class GeoData(DataSet):

    # read file
    def read_file(self):
        with open(self.filepath) as f:
            self.data = json.load(f)
        
    # store all the ZCTA used in geodata
    def zcta_modzcta(self):
        tmp = {}
        for geoj in self.data['features']:
            if geoj['properties']['modzcta'] != '99999':
                for item in geoj['properties']['zcta'].split(', '):
                    tmp[item] = geoj['properties']['modzcta']
        self.geoj_df = pandas.DataFrame(tmp.items(), columns=['ZCTA5', 'modzcta'])


# define child class for txt data
class TxtData(DataSet):

    # read file
    def read_file(self):
        self.data = pandas.read_csv(self.filepath, converters={'ZCTA5': lambda x: str(x)})

    # select the 2 columns
    def select_2_col(self):
        self.data = self.data[['ZCTA5', 'GEOID']]


if __name__ == '__main__':

    # define the constant paths
    geo_path = 'datas/00-tractTOzcta/Modified Zip Code Tabulation Areas (MODZCTA).geojson'
    txt_path = 'datas/00-tractTOzcta/zcta_tract_rel_10.txt'

    # read constant data
    print('Reading geojson data...')
    geo_instance = GeoData(geo_path)
    geo_instance.read_file()
    print('Reading txt data...')
    txt_instance = TxtData(txt_path)
    txt_instance.read_file()

    # get datas folder under the current directory
    base_dir = findpath.get_base_dir()
    # find out all the csv files in the data folder
    valid_csv = findpath.find_tract_csv(base_dir)

    # for each csv, work as below
    for index, csv_path in enumerate(valid_csv):
        print('Working on %s' % csv_path)
        # get the out path
        out_path = os.path.join(base_dir, (str(index) + findpath.generate_outpath(csv_path)))

        # read the datas
        print('Reading csv data...')
        csv_instance = CsvData(csv_path)
        csv_instance.read_file()

        # parse geo data into dataframe with zcta5 and modzcta
        print('Converting data from geojson into pandas dataframe...')
        geo_instance.zcta_modzcta()
        # parse txt data into dataframe with zcta5 and geoid
        print('Selecting ZCTA5 and GEOID from text dataframe...')
        txt_instance.select_2_col()
        # drop margin_of_error rows in csv data, and select NY state rows
        print('Dropping useless columns and selecting New York rows from csv dataframe...')
        csv_instance.drop_Margin_of_Error()
        csv_instance.select_NY()

        # join txt and geojson data
        print('Joining text dataframe and geojson dataframe on ZCTA5...')
        txt_geo = DataSet.join_data(txt_instance.data, geo_instance.geoj_df, 'ZCTA5', 'ZCTA5')
        # join txt_geo and csv data
        print('Joining csv dataframe and txt_geo dataframe on GEOID...')
        txt_geo_csv = DataSet.join_data(csv_instance.data, txt_geo, setindex='GEOID', joinindex='Geographic Identifier - FIPS Code', subset=['ZCTA5', 'modzcta'], inplace=False)

        # move the cols of zcta to the front
        print('Moving ZCTA5 and modzcta to the front...')
        txt_geo_csv = DataSet.rearrange_col(txt_geo_csv, ['ZCTA5', 'modzcta'])
        # save the data
        print('Saving data as csv...')
        out_instance = DataSet(out_path)
        out_instance.save_csv_data(txt_geo_csv)