# Upload required libraries

import pandas as pd
import json
import urllib.request
import numpy as np

# Create a list of urls to call (electoral districts only)

def getdata(url):

    data = urllib.request.urlopen(url).read()
    data1 = data[2:]
    output = json.loads(data1)

    return output

url = "https://www12.statcan.gc.ca/rest/census-recensement/CR2016Geo.json?lang=E&geos=FED&cpt=00"
distlist = []

for data in getdata(url)['DATA']:
    distlist.append(data[0])

print("Districts:", len(distlist))

# Function for transforming the data

def dist_data(url):
    data = urllib.request.urlopen(url).read()

    #Statscan data has a 'head' that needs to be removed, then the json can be read properly.
    data1 = data[2:]
    output = json.loads(data1)

    #Creating the dataframe for simplification of the data
    info_surv = output.get("DATA")
    column_names = output.get("COLUMNS")

    info_surv2 = np.transpose(info_surv)

    data_dict = {}

    for i in range (0, len(column_names)):
        data_dict[column_names[i]] = info_surv2[i]
 
    surv_df = pd.DataFrame.from_dict(data_dict)

    surv_df.rename(columns={'PROV_TERR_NAME_NOM':'PROV_NAME', 'GEO_NAME_NOM':'NAME', 'TEXT_NAME_NOM':'TEXT','T_DATA_DONNEE':'DATA'}, inplace=True)

    #Simplifying Dataframe - Really unnecessary, but makes work easier
    surv2_df = surv_df[['PROV_NAME', 'GEO_UID', 'GEO_ID', 'NAME', 'TEXT', 'DATA']]

    #Array with required information from the dataframe
    column_names = ['PROVINCE', 'GEO_UID', 'GEO_ID', 'NAME']
    distr_data = [surv2_df.iloc[0, 0], surv2_df.iloc[0, 1], surv2_df.iloc[0, 2], surv2_df.iloc[0, 3, ]]

    req_info = [0, 5, 38, 57, 114, 115, 116, 673, 859]
    for req in req_info:
        c_name = surv2_df.iloc[req, 4]
        d_data = surv2_df.iloc[req, 5]
        column_names.append(c_name)
        distr_data.append(d_data)
    
    return(column_names, distr_data)


#Looping through all federal election districts (this takes a while)
i = 0
columns = []
district_data = []

for district in distlist:

    # Create the call
    data = district
    url_sel = f'https://www12.statcan.gc.ca/rest/census-recensement/CPR2016.json?lang=E&dguid={data}&topic=0&notes=0'
    rec = dist_data(url_sel)

    print(i)

    # Create list of column names (first call only)
    if i == 0:
        columns = rec[0]

    #store the district data
    district_data.append(rec[1])
    i = i+1

# Create the datafiles 
print('finished, read', i, 'files')
print(columns)
print("Sample=", district_data[312])

# Use list of column names and datafiles to create the new dataframe
el_dist_df = pd.DataFrame(columns=columns)
for i in range(len(district_data)):
    el_dist_df.loc[i] = district_data[i]

print(el_dist_df.head(20))

# Pickel the dataframe (for use in other programs)
# File can be easily re-converted into a df with pd.read_pickle("nameoffiletounpickel")

el_dist_df.to_pickle("Census2016ElectoralDistrictsInfo.pkl")

print("Data stored")

