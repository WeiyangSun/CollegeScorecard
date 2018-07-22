
# coding: utf-8

# #### Data is taken from : https://collegescorecard.ed.gov/data/

# ##### Using 'Most Recent Data' - 141 MB CSV

# In[1]:


import pandas as pd
import numpy as np
import os

import folium


# In[2]:


path = '/Users/Weiyang/Downloads'


# In[3]:


os.chdir(path)


# In[4]:


dataset = pd.DataFrame.from_csv('dataset.csv')


# ### Problem: Are students who pursue Computer Science better off than Engineering students after graduation?

# #### Selecting columns based on Data Dictionary

# In[5]:


target = ['INSTNM', 'LATITUDE', 'LONGITUDE', 'ADM_RATE', 'CONTROL', 'LOCALE', 'SAT_AVG', 'PCIP11', 'PCIP14', 'TUITIONFEE_IN', 'TUITIONFEE_OUT', 'MEDIAN_HH_INC', 'UNEMP_RATE', 'GRAD_DEBT_MDN', 'COMPL_RPY_1YR_RT', 'COMPL_RPY_3YR_RT']


# In[6]:


focus = dataset[target]


# In[7]:


focus.shape


# In[8]:


focus.head()


# #### Getting rid of rows with 'Privacy Suppressed'

# In[9]:


new_target = ['MEDIAN_HH_INC', 'UNEMP_RATE', 'GRAD_DEBT_MDN', 'COMPL_RPY_1YR_RT', 'COMPL_RPY_3YR_RT']


# In[10]:


for i in new_target:
    
    focus = focus[focus[i] != 'PrivacySuppressed']


# In[11]:


focus.shape


# #### Casting rows as numeric

# In[12]:


for i in new_target:
    
    focus[i] = pd.to_numeric(focus[i])


# In[13]:


focus.describe()


# #### Mapping

# In[14]:


focus.isnull().sum()


# In[15]:


first_map = focus[np.isfinite(focus['LONGITUDE'])]


# #### Note: Map is centered on Dallas, Texas

# In[30]:


folium_map = folium.Map(location=(32.804407, -96.629080),
                     zoom_start = 8,
                     tiles='OpenStreetMap')

for idx, row in first_map.iterrows():
    green = '#228B22'
    orange = '#FFA500'
    blue = '#0000FF'
    red = '#ff4545'
    
    ### Applying manual scaling by 30
    radius = row['PCIP11']*30
    threshold = row['GRAD_DEBT_MDN']
    
    if threshold > first_map['GRAD_DEBT_MDN'].quantile(0.25) and threshold <= first_map['GRAD_DEBT_MDN'].quantile(0.5):
        color = green
    elif threshold > first_map['GRAD_DEBT_MDN'].quantile(0.5) and threshold <= first_map['GRAD_DEBT_MDN'].quantile(0.75):
        color = orange
    elif threshold > first_map['GRAD_DEBT_MDN'].quantile(0.75):
        color = red
    else:
        color = blue
        
    folium.CircleMarker(location = (row['LATITUDE'], row['LONGITUDE']),
                        radius = radius,
                        color = color,
                        fill=True).add_to(folium_map)


# In[31]:


folium_map.save('CS_Map.html')


# In[32]:


from IPython.core.display import display, HTML
display(HTML('CS_Map copy.html'))


# In[26]:


folium_map2 = folium.Map(location=(32.804407, -96.629080),
                     zoom_start = 8,
                     tiles='OpenStreetMap')

for idx, row in first_map.iterrows():
    green = '#228B22'
    orange = '#FFA500'
    blue = '#0000FF'
    red = '#ff4545'
    
    ### Applying manual scaling by 30
    radius = row['PCIP14']*30
    threshold = row['GRAD_DEBT_MDN']
    
    if threshold > first_map['GRAD_DEBT_MDN'].quantile(0.25) and threshold <= first_map['GRAD_DEBT_MDN'].quantile(0.5):
        color = green
    elif threshold > first_map['GRAD_DEBT_MDN'].quantile(0.5) and threshold <= first_map['GRAD_DEBT_MDN'].quantile(0.75):
        color = orange
    elif threshold > first_map['GRAD_DEBT_MDN'].quantile(0.75):
        color = red
    else:
        color = blue
        
    folium.CircleMarker(location = (row['LATITUDE'], row['LONGITUDE']),
                        radius = radius,
                        color = color,
                        fill=True).add_to(folium_map2)


# In[27]:


folium_map2.save('Eng_Map.html')


# In[28]:


from IPython.core.display import display, HTML
display(HTML('Eng_Map copy.html'))

