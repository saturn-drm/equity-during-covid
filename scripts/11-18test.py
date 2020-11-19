#%%
import pandas
# %%
incomeraw = pandas.read_csv('../datas/01-medianIncome/ACS_Median_Household_Income_Variables_-_Boundaries/Tract_2.csv')
incomeraw.head()
# %%
import json
# %%
with open('../datas/00-tractTOzcta/Modified Zip Code Tabulation Areas (MODZCTA).geojson') as f:
    geojdata = json.load(f)
geojdata['features'][0]
# %%
incomeraw.columns
# %%
incomeraw.columns[8]
# %%
print('Margin of Error' in incomeraw.columns[8])
# %%
colTOdrop = []
for column in incomeraw.columns:
    if 'Margin of Error' in column:
        colTOdrop.append(column)
colTOdrop
# %%
incomeColDropped = incomeraw.drop(columns=colTOdrop, inplace=False)
incomeColDropped.head()
# %%
import numpy
# %%
print(incomeColDropped[incomeColDropped['State'] == 'New York'].shape)
# %%
convertor = pandas.read_csv('../datas/00-tractTOzcta/zcta_tract_rel_10.txt', converters={'ZCTA5': lambda x: str(x), 'GEOID': lambda x: str(x)})
convertor.head()
# %%
convertor.dtypes
# %%
incomeColDropped.dtypes
# %%
convertorSelected = convertor[['ZCTA5', 'GEOID']]
convertorSelected.head()
#%%
geodic = {}
for geo in geojdata['features']:
    zctalist = geo['properties']['zcta'].split(', ')
    modzcta = geo['properties']['modzcta']
    if modzcta != '99999':
        for zcta in zctalist:
            geodic[zcta] = modzcta
len(geodic)
#%%
list(geodic.keys())
# %%
convertortouse = convertorSelected[convertorSelected['ZCTA5'].isin(list(geodic.keys()))]
len(convertortouse)
#%%
convertortouse[convertortouse['ZCTA5'] == '10119']
#%%
geodic['10119']
# %%
incomeColDropped.head()
# %%
incomeNY = incomeColDropped[incomeColDropped['State'] == 'New York']
incomeNY.shape
#%%
convertortouse['GEOID'] = convertortouse.astype(str)
# %%
geoidlist = convertortouse['GEOID'].to_list()
type(geoidlist[0])
#%%
incomeNYC = incomeNY[incomeNY['Geographic Identifier - FIPS Code'].isin(geoidlist)]
incomeNYC.shape
#%%
for index, row in incomeNY.iterrows():
    if not row['Geographic Identifier - FIPS Code'] in geoidlist:
        print(row['Geographic Identifier - FIPS Code'])
#%%
36023970600 in geoidlist
#%%
len(incomeNY['Geographic Identifier - FIPS Code'].to_list())
#%%
len(geoidlist)
# %%
incomeNYC['ZCTA5'] = ''
incomeNYC['modzcta'] = ''
for index, row in incomeNYC.iterrows():
    tmpconverter = convertortouse[convertortouse['GEOID'] == str(row['Geographic Identifier - FIPS Code'])]['ZCTA5'].iloc[0]
    incomeNYC['ZCTA5'][index] = int(tmpconverter)
    incomeNYC['modzcta'][index] = int(geodic[tmpconverter])
incomeNYC.shape
#%%
incomeNYC.head()
# %%
incomeNYC.reset_index(drop=True, inplace=True)
incomeNYC.head()
# %%
colToMove1 = incomeNYC.pop('ZCTA5')
colToMove2 = incomeNYC.pop('modzcta')
incomeNYC.insert(1, 'ZCTA5', colToMove1)
incomeNYC.insert(2, 'modzcta', colToMove2)
incomeNYC.head()
# %%
incomeNYC.to_csv('../datas/01income-cleaned.csv', index=False)
# %%
len(incomeNYC['ZCTA5'].unique())
# %%
for index, row in incomeNYC.iterrows():
    if row['ZCTA5'] != row['modzcta']:
        print(str(row['ZCTA5']) + ': ' + str(row['modzcta']))
# %%
10119 in incomeNYC['ZCTA5'].to_list()




# %%
import pandas
import json
incomeraw = pandas.read_csv('../datas/01-medianIncome/ACS_Median_Household_Income_Variables_-_Boundaries/Tract_2.csv')
with open('../datas/00-tractTOzcta/Modified Zip Code Tabulation Areas (MODZCTA).geojson') as f:
    geojdata = json.load(f)
convertor = pandas.read_csv('../datas/00-tractTOzcta/zcta_tract_rel_10.txt', converters={'ZCTA5': lambda x: str(x), 'GEOID': lambda x: str(x)})
# %%
incomeraw.dtypes
# %%
type(geojdata['features'][0]['properties']['modzcta'])
# %%
colTOdrop = []
for column in incomeraw.columns:
    if 'Margin of Error' in column:
        colTOdrop.append(column)
incomeColDropped = incomeraw.drop(columns=colTOdrop, inplace=False)
# %%



class Test():

    def __init__(self, a, b):
        self.x = a
        self.y = b
    
    def plus(self, a, b):
        return a + b
    
test1 = Test(1,2)
test1.plus(1, 2)
# %%
import os
parentdir = os.path.dirname((os.getcwd()))
os.path.join(parentdir, 'datas/01-medianIncome/ACS_Median_Household_Income_Variables_-_Boundaries/Tract_2.csv')
# %%
