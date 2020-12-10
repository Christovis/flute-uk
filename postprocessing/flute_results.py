#!/usr/bin/env python
# coding: utf-8

# In[14]:


import sys
get_ipython().system('{sys.executable} -m pip install numpy')
get_ipython().system('{sys.executable} -m pip install pandas')
get_ipython().system('{sys.executable} -m pip install geopandas')
get_ipython().system('{sys.executable} -m pip install matplotlib')
get_ipython().system('{sys.executable} -m pip install descartes')


# In[15]:


import locale
import numpy as np
import pandas as pd
import geopandas as gpd

from pylab import cm                                                             
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.pyplot import figure

#import figure_size
plt.style.use("mplstyle")


# In[16]:


flute_dir = "/Users/dph0rgb/Box Sync/Research/Flute/FluTE_UK/"

flute_id = pd.read_csv(
    flute_dir + "northeast_tracts",
    delimiter=',',
    delim_whitespace=False,
)

log = pd.read_csv(
    flute_dir + "northeast_log",
    delimiter=',',
    delim_whitespace=False,
    #dtype={'':int,'':str,'':int,'':int,'':int,'':int,'':int,'':int,'':int,'':int,'':int,'':int},
)
#log = log.astype({'TractID': 'str'})
#log = log.groupby(["time"]).sum(axis=1)  # sum all areas to complete region (North East)


# In[17]:


# dictionaries from FluTe to NOMIS
RGN17CD_df = pd.read_csv(
    flute_dir + "input_ew/RGN17CD_dict.csv",
    delimiter=',',
    delim_whitespace=False,
)
RGN17CD_df = RGN17CD_df.rename(columns={"Unnamed: 0": "nomis id"})
LAD11CD_df = pd.read_csv(
    flute_dir + "input_ew/LAD11CD_dict.csv",
    delimiter=',',
    delim_whitespace=False,
)
LAD11CD_df = LAD11CD_df.rename(columns={"Unnamed: 0": "nomis id"})
MSOA11CD_df = pd.read_csv(
    flute_dir + "input_ew/MSOA11CD_dict.csv",
    delimiter=',',
    delim_whitespace=False,
)
MSOA11CD_df = MSOA11CD_df.rename(columns={"Unnamed: 0": "nomis id"})


# In[18]:


for flute_key in flute_id["TractID"].values:
    trans_key = flute_id[flute_id["TractID"] == flute_key]["FIPStract"].values[0]
    nomis_key = MSOA11CD_df[MSOA11CD_df["flute id"] == trans_key]["nomis id"].values[0]
    log["TractID"] = log["TractID"].replace(flute_key, nomis_key)


# In[26]:


log

# To convert into percentage read whole population
pop = pd.read_csv(
    flute_dir + "input_ew/population_in_msoa_sape21dt3a_2018.csv",
    skiprows=4,
    delimiter=',',
    delim_whitespace=False,
)

# Group ages in same bins as FluTE
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
for col in pop.columns[4:]:
    pop[col] = pop[col].apply(lambda x: locale.atoi(x))

list_0_4 = ['0','1','2','3','4']
list_5_18 = ['5','6','7','8','9','10','11','12','13','14','15','16','17','18']
list_19_29 = ['19','20','21','22','23','24','25','26','27','28','29']
list_30_64 = ['30','31','32','33','34','35','36','37','38','39','40','41',
              '42','43','44','45','46','47','48','49','50','51','52','53',
              '54','55','56','57','58','59','60','61','62','63','64']
list_65_inf = ['65','66','67','68','69','70','71','72','73','74','75','76',
               '77','78','79','80','81','82','83','84','85','86','87','88','89','90+']
pop["0-4"] = pop[list_0_4].sum(axis=1)
pop = pop.drop(list_0_4, axis=1)
pop["5-18"] = pop[list_5_18].sum(axis=1)
pop = pop.drop(list_5_18, axis=1)
pop["19-29"] = pop[list_19_29].sum(axis=1)
pop = pop.drop(list_19_29, axis=1)
pop["30-64"] = pop[list_30_64].sum(axis=1)
pop = pop.drop(list_30_64, axis=1)
pop["65-inf"] = pop[list_65_inf].sum(axis=1)
pop = pop.drop(list_65_inf, axis=1)
pop
# In[27]:


fig, ax = plt.subplots(
    1, 1, figsize=(14, 12),
    facecolor="w", edgecolor="k",
)

plt.plot(
    log.index.values,
    log["cumsym0-4"].values,
    label="0-4",
)
plt.plot(
    log.index.values,
    log["cumsym5-18"].values,
    label="5-18",
)
plt.plot(
    log.index.values,
    log["cumsym19-29"].values,
    label="19-29",
)
plt.plot(
    log.index.values,
    log["cumsym30-64"].values,
    label="30-64",
)
plt.plot(
    log.index.values,
    log["cumsym65+"].values,
    label="65+",
)

plt.xlim([0, 180])
plt.xlabel(r'time  [days]', fontsize=16)
plt.ylabel(r'cumsym', fontsize=16)
plt.title(r"North East")
plt.legend(loc='best')
plt.grid()


# In[28]:


fig, ax = plt.subplots(
    1, 1, figsize=(14, 12),
    facecolor="w", edgecolor="k",
)

plt.plot(
    log.index.values,
    log["cumsym5-18"].values / \
    log[["cumsym19-29", "cumsym30-64", "cumsym65+"]].sum(axis=1).values,
)

plt.xlim([0, 180])
plt.xlabel(r'time  [days]', fontsize=16)
plt.ylabel(r'child attack rate / adult attack rate', fontsize=16)
plt.title(r"North East")
plt.grid()


# In[29]:


dirs = "./Middle_Layer_Super_Output_Areas_December_2011_Full_Clipped_Boundaries_in_England_and_Wales/"
ew_shape = gpd.read_file(
    dirs+'Middle_Layer_Super_Output_Areas_December_2011_Full_Clipped_Boundaries_in_England_and_Wales.shp'
)
ew_shape = ew_shape.set_index('msoa11cd')


# In[30]:


log = log[log["time"] == 181].set_index('TractID')
log["cumsym0-inf"] = log[["cumsym0-4","cumsym5-18","cumsym19-29","cumsym30-64","cumsym65+"]].sum(axis=1)

region_shape = ew_shape.merge(
    log[["time", "cumsym0-inf"]],
    left_index=True,
    right_index=True
)


# In[24]:


# Convert to Lon. & Lat.
# https://gis.stackexchange.com/questions/302699/extracting-longitude-and-latitude-from-shapefile
test = region_shape.to_crs(epsg=4326)  # EPSG 4326 = WGS84 = https://epsg.io/4326
durham = [54.7753, 1.5849]
newcastle_ut = [54.9783, 1.6178]


# In[25]:


fig, ax = plt.subplots(
    figsize=(12, 6),
)

norm = colors.Normalize(vmin=log["cumsym0-inf"].values.min(), vmax=log["cumsym0-inf"].values.max())
cbar = plt.cm.ScalarMappable(norm=norm, cmap='Blues')

test.plot(
    column="cumsym0-inf",
    ax=ax,
    legend=True,
    cmap=cm.Blues,
    alpha=0.9,
    categorical=False,
)
plt.scatter(
    -1.5849, 54.7753,
    marker=7, #'+',
    s=300,
    c='red',
    label="Durham"
)
plt.scatter(
    -1.6178, 54.9783,
    marker=7,#'+',
    s=300,
    c='orange',
    label="Newcastle upon Tyne"
)

ax_cbar = fig.colorbar(cbar, ax=ax)
ax_cbar.set_label('I am a label')
plt.legend(loc='best')
plt.xlim([-2.0, -1.25])
plt.ylim([54.6, 55.2])

"""
# Convert axis ticks units from m to km
labels = [item.get_text() for item in ax.get_xticklabels()]
labels = [float(item)/1e3 for item in labels]
ax.set_xticklabels(labels)
labels = [item.get_text() for item in ax.get_yticklabels()]
labels = [float(item)/1e3 for item in labels]
ax.set_yticklabels(labels)
plt.xlabel("x  [km]")
plt.xlabel("y  [km]")
"""
#cbar = fig.colorbar(choropleth, format='%.2f')
#cbar.set_label('# of symptomatic cases',size=14)


# In[ ]:




