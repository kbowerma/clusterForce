
# coding: utf-8

# ## The purpose of this notebook is to take random contacts and assign them to cities according to the population of those cities.

# In[1]:


import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from random import choices

#read the data file for cites
path = '/Users/kylebowerman/Documents/mydev/clusterForce/data/uscitiesv1.4.csv'
citiesDF = pd.read_csv(path)
#print("df shape:", df.shape)

#read the data file for contacts
path = '/Users/kylebowerman/Documents/mydev/clusterForce/data/contacts1.csv'
contactsDF = pd.read_csv(path)
print("\nThis cell loads the contacts in contactsDF and cities in citiesDF")
print("citiesDF shape:", citiesDF.shape, "\tcontactsDF shape: ", contactsDF.shape)
contactsDF


# In[2]:


df2 =  citiesDF.loc[citiesDF['population'] > 100].sort_values(by=['population'],ascending=False)
cityIndex = df2.index.values
population = df2['population'].values
print("This cell creates two arrays: one for the cityIndex and one for the population")
print("They will be used to select a weighted random city for each of the contacts")


# In[3]:



#choices(cityIndex,population)  will pick from the cityIndex array based on the weight of population

# create an array of cities, one for each contact 
arr = []
for x in range (0,len(contactsDF)):
    arr.append(choices(cityIndex,population))
# convert array to data frame    
randomCityDf = pd.DataFrame(arr, columns=['cityId'])

#make common keys
randomCityDf['key'] = randomCityDf.index
contactsDF['key'] = contactsDF.index

#merge the contact data fram with the randomCity Dataframe based on the index of the contacts
#mdf1 = pd.merge(contactsDF,randomCityDf,how='left',on='contactsDF.index')
# need a common column name not needed in juputer
mdf1 = pd.merge(contactsDF,randomCityDf,how='left',on='key')

df4 = df2[['city','state_id','county_name','lat','lng','population','density']]
df4.insert(0,'cityId',df4.index)


# In[4]:

output = pd.merge(mdf1,df4)
csvOutput = output.sort_values('LastName').to_csv(index=False)

contactsFile = open("contacts.csv","w")
contactsFile.write(csvOutput)

# In[5]:

summary = output.groupby(by="city").size().reset_index(name='counts')
print(summary.sort_values('counts',ascending=False))


