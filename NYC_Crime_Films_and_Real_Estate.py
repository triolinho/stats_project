#Property Data: pull, clean
pip install sodapy

import pandas as pd
from sodapy import Socrata
import config #contains username, password, app token
import numpy as np

#pull from NYC Open data
client = Socrata("data.cityofnewyork.us", '7YJroGSBVCt6gzuLz6whih0yc')

# Example authenticated client (needed for non-public datasets):
client = Socrata('data.cityofnewyork.us',
                  config.app_token,
                  username=config.app_user,
                  password=config.app_pw)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
property_values_results = client.get("8vgb-zm6e", limit=50000)

# Convert to pandas DataFrame
property_values_results_df = pd.DataFrame.from_records(property_values_results)

#remove non_NYC properties ('borough data empty')
#replace '' with nan
property_values_results_df['borough'] = property_values_results_df['borough'].replace('',np.nan)

#drop nans
property_values_results_df = property_values_results_df.dropna(axis=0, subset=['borough'])

#confirm rows were deleted
property_values_results_df.shape

#reindex DataFrame
property_values_results_df = property_values_results_df.reset_index(drop=True)

#confirm reset_index
property_values_results_df

#save datafram to .csv
property_values_results_df.to_csv('property_values.csv')

#Film permit data pull
client = Socrata('data.cityofnewyork.us',
                  config.app_token,
                  username=config.app_user,
                  password=config.app_pw)
permit_results = client.get("tg4x-b46p", limit=50000)
permit_results_df = pd.DataFrame.from_records(permit_results)

#save to to_csv
results_df.to_csv('film_permits.csv')
