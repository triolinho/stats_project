import requests
import config
from bs4 import BeautifulSoup as BS
import mysql.connector
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sb

#!/usr/bin/env python
# make sure to install these packages before running:
# pip install pandas
#pip install sodapy

import pandas as pd
from sodapy import Socrata
import config_nyc_od

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
#client = Socrata("data.cityofnewyork.us", None)

client = Socrata('data.cityofnewyork.us',
                 config_nyc_od.app_tok,
                 username=config_nyc_od.app_username,
                 password=config_nyc_od.app_pw)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
#results = client.get("tg4x-b46p", limit=2000)

#dF for seven major felonies
felony_df = pd.read_excel(r'felony_clean.xls')
felony_df['PCT'].fillna( method ='ffill', inplace = True)
felony_df = felony_df[felony_df['CRIME']=='TOTAL SEVEN MAJOR FELONY OFFENSES']

#non-major felonies dF
other_felony_df = pd.read_excel(r'other_felony.xls')
other_felony_df['PCT'].fillna( method ='ffill', inplace = True)
other_felony_df.head(20)

#misdemeanor dF
misdemeanor_df = pd.read_excel(r'misdemeanor_pct.xls')
misdemeanor_df['PCT'].fillna( method = 'ffill', inplace = True)
misdemeanor_df = misdemeanor_df[misdemeanor_df['CRIME']=='TOTAL MISDEMEANOR OFFENSES']

#violation dF
violation_df = pd.read_excel(r'violation_pct.xls')
violation_df['PCT'].fillna( method = 'ffill', inplace = True)
violation_df = violation_df[violation_df['CRIME']=='TOTAL VIOLATION OFFENSES']

#set index to precinct column for each dataframe
# felony_df = felony_df.set_index('PCT')
# other_felony_df = other_felony_df.set_index('PCT')
# misdemeanor_df = misdemeanor_df.set_index('PCT')
# violation_df = violation_df.set_index('PCT')

#add df for median rent
rent_df = pd.read_csv("median_rent.csv")
rent_df.head()
rent_df = rent_df.dropna() #drop null values

#create new dataframe for average median rent for the year
mean_rent_df = rent_df.filter(['areaName', 'Borough', 'areaType'])

df2010 = rent_df.filter(['2010-01', '2010-02', '2010-03',
                        '2010-04', '2010-05', '2010-06', '2010-07', '2010-08', '2010-09', '2010-10',
                         '2010-11', '2010-12'])

series2010 = df2010.mean(axis = 1, skipna = True)

### repeat this step for each year ###

mean_rent_df['Year 2010'] = series2010
mean_rent_df['Year 2011'] = series2011
mean_rent_df['Year 2012'] = series2012
mean_rent_df['Year 2013'] = series2013
mean_rent_df['Year 2014'] = series2014
mean_rent_df['Year 2015'] = series2015
mean_rent_df['Year 2016'] = series2016
mean_rent_df['Year 2017'] = series2017
mean_rent_df['Year 2018'] = series2018

#getting zip codes for neighborhoods

page = requests.get("https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm")
page

table = html.find("table")
rows = table.findAll('tr')
zipdata = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]

for item in zipdata:
    if len(item) == 2:
        item.insert(0, None)
zipdata

zipdf = pd.DataFrame(zipdata)
zipdf[0].fillna( method ='ffill', inplace = True)

zipdf.columns = ['Borough', 'Neighborhood', 'Zip Code(s)']

## creating zip code dataframe

zipdf = zipdf.dropna()
zipdf['Borough'] = zipdf['Borough'].str[0]
zipdf['Neighborhood'] = zipdf['Neighborhood'].str[0]
zipdf['Zip Code(s)'] = zipdf['Zip Code(s)'].str[0]
zipdf

## getting rid of everything outside of manhattan
zipdf = zipdf[zipdf['Borough'] == 'Manhattan']
zipdf

#narrowing down rent values to neighborhoods only
manhattan_df = manhattandf[manhattandf['areaType'] == 'neighborhood']

## change column names for crime dataframes
violation_df.columns = ('PCT', 'CRIME', 'y2000', 'y2001', 'y2002', 'y2003', 'y2004',
                        'y2005', 'y2006', 'y2007', 'y2008', 'y2009', 'y2010', 'y2011',
                         'y2012', 'y2013', 'y2014', 'y2015', 'y2016', 'y2017', 'y2018')

### do this for each dataframe

## drop duplicate from rent df
manhattan_df = manhattan_df.drop([131, 120])

## create column for zip codes in rent values DataFrame

rent_zip_codes = ['10280', '10026', '10019', '10001', '10038', '10029', '10003', '10005', '10010', '10016',
                 '10014', '10031', '10034', '10013', '10002', '10017', '10022', '10018', '10025', '10044',
                 '10012', '10007', '10128', '10023', '10032', '10011']
manhattan_df.insert(2, 'Zip_Code', rent_zip_codes)

### add brittany's data to notebook

film_permits_df = pd.read_csv(r'manhattan_film_permit_results_df')
value_zip_code_df = pd.read_csv(r'mean_value_by_zipcode')
permits_by_zip_df = pd.read_csv(r'permits_per_zip_df')
### isolate film permits to shooting permits only
film_permits_df = film_permits_df[film_permits_df['eventtype'] == 'Shooting Permit']


##merge dataframes

new_felony_df_stats_only= felony_df_stats_only.drop('CRIME', axis=1)
new_felony_df_stats_only.head()

new_new = new_felony_df_stats_only.filter(['y2016', 'y2017', 'y2018'])
new_new.head()

new_new['sum'] = new_new.sum(axis=1)
new_new.head()

## get total permits for each precinct

new_fp['total_permits'] = new_fp.groupby('policeprecinct_s')['policeprecinct_s'].transform('count')
new_fp.head(50)

new_fp = new_fp.filter(['policeprecinct_s', 'total_permits'])

## drop duplicates

new_new_fp =new_fp.drop_duplicates('policeprecinct_s')
new_new_fp.head(20)

## finally merge dataframes

felony_film_df = pd.merge(new_new_new, new_new_fp, left_on='PCT', right_on='policeprecinct_s')

### repeat for each crime DataFrame

## find pearson correlation for each crime stat and amount of film permits
felony_film_df.corr(method='pearson')
other_felony_film_df.corr(method='pearson')
misdemeanor_film_df.corr(method='pearson')
violation_film_df.corr(method='pearson')

##create lists for ttest
felony_list = felony_df.values.tolist()
top_felony_list1 = felony_list[0]
top_felony_list2 = felony_list[9]

print(top_felony_list1.pop(0))
top_felony1 = list(map(int, top_felony_list1))

## do same for other list

from scipy.stats import ttest_ind
import numpy as np
ttest_ind(top_felony1, top_felony2)
##Ttest_indResult(statistic=-4.1841688359582925, pvalue=0.00017552099421652955)
​
###repeat for each crime DataFrame

### scatter plot for crimes/film permits
fig, ax = plt.subplots(figsize=(10,5))
sns.scatterplot(felony_film_df['sum'], felony_film_df['total_permits'], s=200)
plt.xlabel('Total Felonies from 2016-2018')
plt.ylabel('Total Film Permits')
plt.show()

##repeat for each crime 
