'''
This script is created on 2020 Nov. 18th
It's meant for cleaning the first-hand csv datas downloaded from ArcGIS webserver
'''

class DataCleaning():

    def __init__(self, filepath):
        self.filepath = filepath

if __name__ == '__main__':
    pass

# TODO: read csv files

# TODO: drop the columns not need

# TODO: read geojson file

# TODO: add the used zcta codes to each district correspondingly

# TODO: select the rows for NYC (with zcta codes)

# TODO: export data as '*-cleaned.csv'