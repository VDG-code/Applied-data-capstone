#!/usr/bin/env python
# coding: utf-8

# # Question 1

# ## About

# In this project we are required to explore and cluster the neighborhoods in Toronto. Next we will have different titles for each action which is need for this project.

# ## Preprocessing

# In[3]:


#importing necessary libraries
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import folium
from geopy.geocoders import Nominatim
from pandas.io.json import json_normalize
from sklearn.cluster import KMeans
import matplotlib.cm as cm
import matplotlib.colors as cl
print('Libraries imported!')


# In[7]:


#scrapping data
source = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M").text
soup = BeautifulSoup(source, 'lxml')

table = soup.find("table")
table_rows = table.tbody.find_all("tr")

data = []
for tr in table_rows:
    td = tr.find_all("td")
    row = [tr.text for tr in td]
    
    if row != [] and row[1] != "Not assigned":
        if "Not assigned" in row[2]: 
            row[2] = row[1]
        data.append(row)


df = pd.DataFrame(data, columns = ["PostalCode", "Borough", "Neighborhood"])
df["PostalCode"] = df["PostalCode"].str.replace("\n","")
df["Borough"] = df["Borough"].str.replace("\n","")
df["Neighborhood"] = df["Neighborhood"].str.replace("\n","")
df.head()


# In[19]:


for index, row in df.iterrows():
    if row['Neighborhood'] == 'Not assigned':
        row['Neighborhood'] = row['Borough']
        
df = df[df.Borough != 'Not assigned']
df = df.rename(columns={'Postcode': 'Postalcode'})

df = df.groupby(['PostalCode', 'Borough'])['Neighborhood'].apply(list).apply(lambda x:', '.join(x)).to_frame().reset_index()
df.head()


# In[20]:


df.shape

