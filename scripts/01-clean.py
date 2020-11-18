'''
This script is created on 2020 Nov. 18th
It's meant for cleaning the first-hand csv datas downloaded from ArcGIS webserver
'''

import pandas
import json

# define parent class for all data
class DataSet():

    # file path
    def __init__(self, filepath):
        self.filepath = filepath

# define child class for csv data
class CsvData(DataSet):

    # read file
    def read_file(self):
        self.data_raw = pandas.read_csv(self.filepath)
    
    # drop the columns of Margin of Error
    def drop_Margin_of_Error(self):
        col_to_drop = []
        for column in self.data_raw.columns:
            if 'Margin of Error' in column:
                col_to_drop.append(column)
        self.data_without_margin = self.data_raw.drop(columns=col_to_drop, inplace=False)
    
    # select the rows for NY
    def select_NY(self, colname='State', colcontent='New York'):
        self.data_NY = self.data_without_margin[self.data_without_margin[colname] == colcontent]

# define child class for geojson data
class GeoData(DataSet):

    # read file
    def read_file(self):
        with open(self.filepath) as f:
            self.data_raw = json.load(f)
        
    # store all the ZCTA used in geodata

# define child class for txt data
class TxtData(DataSet):

    # read file
    def read_file(self):
        self.data_raw = pandas.read_csv(self.filepath, converters={'ZCTA5': lambda x: str(x), 'GEOID': lambda x: str(x)})

    # select the 2 columns
    def select_2_col(self):
        self.data_select = self.data_raw[['ZCTA5', 'GEOID']]

if __name__ == '__main__':
    pass




# TODO: add the used zcta codes to each district correspondingly


# TODO: export data as '*-cleaned.csv'