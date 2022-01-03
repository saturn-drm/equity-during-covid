import geopandas
import geopy
import pandas
import time

# initialize the convertor
locator = geopy.Nominatim(user_agent='myGeocoder')

# read data and set the location column
data = pandas.read_csv('medical-facilities.csv')
data['location'] = ''
data.astype({'lat': 'float64', 'lng': 'float64'})

# convert
for index, row in data.iterrows():
    location = locator.geocode(row['ADDRESS'])
    print('converting %s' % row['ADDRESS'])
    if location:
        data.loc[index, 'lat'] = location.latitude
        data.loc[index, 'lng'] = location.longitude
        data.loc[index, 'location'] = str(location.address)
    else:
        data.loc[index, 'lat'] = 0
        data.loc[index, 'lng'] = 0
        data.loc[index, 'location'] = 'None'

    time.sleep(0.5)

data.to_csv('medical-facilities-converted.csv', index=False)