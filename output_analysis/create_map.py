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

# sum of all age groups
flutelog_df["cumsym0-inf"] = flutelog_df[
    ["cumsym0-4","cumsym5-18","cumsym19-29","cumsym30-64","cumsym65+"]
].sum(axis=1)
flutelog_df = flutelog_df.drop(
    columns=["cumsym0-4","cumsym5-18","cumsym19-29","cumsym30-64","cumsym65+"]
)

# load shape file of England and Wales
shape_file = 'Middle_Layer_Super_Output_Areas_December_2011_Full_Clipped_Boundaries_in_England_and_Wales'
ew_shape = gpd.read_file('%s/%s.shp' % (shape_file, shape_file))
ew_shape = ew_shape.set_index('msoa11cd')

shape_file = 'Countries_December_2019_GB_BFC'
uk_shape = gpd.read_file('%s/%s.shp' % (shape_file, shape_file))

# crea maps for each day in simulation
for day in np.unique(flutelog_df["time"].values)[50:]:
    print("Day", day)
    flute_day = flutelog_df[flutelog_df["time"] == day].set_index('TractID')

    ew_day = ew_shape.merge(
        flute_day[["time", "cumsym0-inf"]],
        left_index=True,
        right_index=True
    )

    fig, ax = plt.subplots(figsize=(12, 6),)

    norm = colors.Normalize(
        vmin=ew_day["cumsym0-inf"].values.min(),
        vmax=ew_day["cumsym0-inf"].values.max(),
    )
    cbar = plt.cm.ScalarMappable(norm=norm, cmap='Blues')

    ew_day.plot(
        column="cumsym0-inf",
        ax=ax,
        cmap=cm.Blues,
        categorical=False,
    )
    uk_shape.plot(
        color=None,
        ax=ax,
        facecolor="none",
        alpha=1.0,
        edgecolor='black',
        linewidth=0.5,
        categorical=False,
    )
    ax.axis('off')
    plt.savefig("ew_day%d_map.png"%day, dpi=150)
    plt.clf()
    plt.close('all')
