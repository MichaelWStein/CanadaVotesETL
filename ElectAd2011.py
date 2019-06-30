import pandas as pd
import numpy as np

#Read the csv file with the election results
election_results_2011 = pd.read_csv('resultsbyelectoralDistrict2011.csv')

#Create a dictionary - key is the electoral district number (which can be linked to the geo-code in the df for the election results),
#and value is the election result. 
results = {}

counter = election_results_2011.shape[0]
i = 0
while i < counter:
    sample = election_results_2011.iloc[i]
    if "NDP" in sample[12]:
        results[sample[2]] = "NDP"
    elif "Liberal" in sample[12]:
        results[sample[2]] = "Liberal"
    elif "Conservative" in sample[12]: 
        results[sample[2]] = "Conservative"
    elif "Bloc" in sample[12]:
        results[sample[2]] = "Bloc"
    elif "Green" in sample[12]:
        results[sample[2]] = "Green"
    else: print(sample, "not tracked")
    i += 1

print(results)

#Unpickle the dataframe and add column with default value
census_df = pd.read_pickle("Census2016ElecDistrwResults.pkl")
census_df['2011 Results'] = 'unknown'

#Loop through the dataframe
# still need to work on this loup - some of the electoral districts didn't exist in the 2011 election (only 308 seats)
counter = census_df.shape[0]
i = 0
while i < counter:
    distr = census_df.iloc[i][2]
    party = results[int(distr)]
    census_df.at[i, '2011 Results'] = party
    i += 1
    
print(census_df.head())
print(census_df.tail())

#Save the dataframe with the results
census_df.to_pickle("Census2016ElecDistrw2011_15Results.pkl")


