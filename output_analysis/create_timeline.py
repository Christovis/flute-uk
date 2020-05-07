import sys, argparse, locale
import numpy as np
import pandas as pd
import geopandas as gpd

from pylab import cm                                                             
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.pyplot import figure
plt.style.use("publication.mplstyle")

region = "EnglandWales"

# load encoder to get from FluTE internal to naming convection of input data
flute_trans = pd.read_csv(
    "./%s/ew_tracts" % region,
    delimiter=',',
    delim_whitespace=False,
)
flutelog_df = pd.read_csv(
    "./%s/ew_log" % region,
    delimiter=',',
    delim_whitespace=False,
)
# sum all areas to complete region (North East)
flutelog_df = flutelog_df.groupby(["time"]).sum(axis=1)

# load encoder to get from FluTE input data to NOMIS/MSOA naming convection
RGN17CD_df = pd.read_csv(
    "./%s/RGN17CD_dict.csv" % region,
    delimiter=',',
    delim_whitespace=False,
)
RGN17CD_df = RGN17CD_df.rename(columns={"Unnamed: 0": "nomis id"})
LAD11CD_df = pd.read_csv(
    "./%s/LAD11CD_dict.csv" % region,
    delimiter=',',
    delim_whitespace=False,
)
LAD11CD_df = LAD11CD_df.rename(columns={"Unnamed: 0": "nomis id"})
MSOA11CD_df = pd.read_csv(
    "./%s/MSOA11CD_dict.csv" % region,
    delimiter=',',
    delim_whitespace=False,
)
MSOA11CD_df = MSOA11CD_df.rename(columns={"Unnamed: 0": "nomis id"})


# Rename FluTE area codes to NOMIS/MSOA area codes
for flute_key in flute_trans["TractID"].values:
    trans_key = flute_trans[flute_trans["TractID"] == flute_key]["FIPStract"].values[0]
    nomis_key = MSOA11CD_df[MSOA11CD_df["flute id"] == trans_key]["nomis id"].values[0]
    flutelog_df["TractID"] = flutelog_df["TractID"].replace(flute_key, nomis_key)

fig, ax = plt.subplots(
    1, 1, figsize=(14, 12),
    facecolor="w", edgecolor="k",
)

plt.plot(
    flutelog_df.index.values,
    flutelog_df["cumsym0-4"].values,
    label="0-4 yr",
)
plt.plot(
    flutelog_df.index.values,
    flutelog_df["cumsym5-18"].values,
    label="5-18 yr",
)
plt.plot(
    flutelog_df.index.values,
    flutelog_df["cumsym19-29"].values,
    label="19-29 yr",
)

plt.plot(
    flutelog_df.index.values,
    flutelog_df["cumsym30-64"].values,
    label="30-64 yr",
)

plt.plot(
    flutelog_df.index.values,
    flutelog_df["cumsym65+"].values,
    label="65+ yr",
)


plt.xlim([0, 180])
plt.xlabel(r'time  [days]', fontsize=16)
plt.ylabel(r'cumsym', fontsize=16)
plt.title(r"North East")
plt.legend(loc='best')
plt.grid()
plt.savefig("ew_total_infection_timeline.png", dpi=150)
plt.clf()
