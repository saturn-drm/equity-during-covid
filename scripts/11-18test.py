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
# %%
geomodzcta = []
for geo in geojdata['features']:
    geomodzcta.append(geo['properties']['modzcta'])
geomodzcta
# %%
convertortouse = convertorSelected[convertorSelected['ZCTA5'].isin(geomodzcta)]
convertortouse
# %%
len(geomodzcta)
# %%
print(convertortouse['GEOID'][0])
# %%
incomeColDropped.head()
# %%
incomeNY = incomeColDropped[incomeColDropped['State'] == 'New York']
incomeNY.head()
# %%
geoidlist = convertortouse['GEOID'].to_list()
incomeNYC = incomeNY[incomeNY['Geographic Identifier - FIPS Code'].isin(geoidlist)]
incomeNYC.shape
# %%
for index, row in incomeNYC.iterrows():
    print(convertortouse.loc[convertortouse['GEOID'] == row['Geographic Identifier - FIPS Code'], 'ZCTA5'].iloc[0])
# %%
convertortouse[convertortouse['GEOID'] == '36005000100']['ZCTA5'].iloc[0]
# %%
for index, row in incomeNYC.iterrows():
    tmpconverter = int(convertortouse[convertortouse['GEOID'] == str(row['Geographic Identifier - FIPS Code'])]['ZCTA5'].iloc[0])
    incomeNYC['ZCTA5'][index] = tmpconverter
incomeNYC.head()
# %%
incomeNY.head()
# %%
incomeNYC.reset_index(drop=True, inplace=True)
incomeNYC.head()
# %%
colToMove = incomeNYC.pop('ZCTA5')
incomeNYC.insert(1, 'ZCTA5', colToMove)
incomeNYC.head()
# %%
incomeNYC.to_csv('../datas/01income-cleaned.csv', index=False)
# %%
