import sys, argparse, locale
import numpy as np
import pandas as pd
import geopandas as gpd

from pylab import cm                                                             
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.pyplot import figure
plt.style.use("mplstyle")

region = "EnglandWales/with_airports"

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

# sum all areas to complete region (North East)
flutelog_tl_df = flutelog_df.groupby(["time"]).sum(axis=1)
flutelog_tl_df = flutelog_tl_df.drop(columns=["TractID"])

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
for day in np.unique(flutelog_df["time"].values)[10:]:
    print("Day", day)
    flute_day = flutelog_df[flutelog_df["time"] == day].set_index('TractID')

    # filter data by day
    ew_day = ew_shape.merge(
        flute_day[["time", "cumsym0-inf"]],
        left_index=True,
        right_index=True
    )
    
    # Plot
    fig, (ax_map, ax_tl) = plt.subplots(
        1, 2, sharex=False, sharey=False,
        figsize=(16, 7.5),
        facecolor="w", edgecolor="k",
    )

    # Map
    ew_day.plot(
        column="cumsym0-inf",
        ax=ax_map,
        cmap=cm.Blues,
        vmin=0,
        vmax=ew_day["cumsym0-inf"].values.max(),
        categorical=False,
    )
    uk_shape.plot(
        ax=ax_map,
        facecolor="none",
        edgecolor='black',
        linewidth=0.5,
        categorical=False,
    )
    ax_map.axis('off')
    
    # Time-line
    ax_tl.plot(
        flutelog_tl_df.loc[:day].index.values,
        flutelog_tl_df.loc[:day]["cumsym0-4"].values,
        label="0-4",
    )
    ax_tl.plot(
        flutelog_tl_df.loc[:day].index.values,
        flutelog_tl_df.loc[:day]["cumsym5-18"].values,
        label="5-18",
    )
    ax_tl.plot(
        flutelog_tl_df.loc[:day].index.values,
        flutelog_tl_df.loc[:day]["cumsym19-29"].values,
        label="19-29",
    )
    ax_tl.plot(
        flutelog_tl_df.loc[:day].index.values,
        flutelog_tl_df.loc[:day]["cumsym30-64"].values,
        label="30-64",
    )
    ax_tl.plot(
        flutelog_tl_df.loc[:day].index.values,
        flutelog_tl_df.loc[:day]["cumsym65+"].values,
        label="65+",
    )
    ax_tl.set_xlim([0, 180])
    ax_tl.set_xlabel(r'time  [days]', fontsize=16)
    ax_tl.set_yscale('log')
    ax_tl.legend(loc='best')
    ax_tl.grid()
    
    fig.suptitle(r'Cumulative number of infections', fontsize=16)
    plt.savefig(
        "./EnglandWales/with_airports/gif/ew_day%d_log_gif.png"%day,
        dpi=150,
        bbox_inches='tight'
    )
    plt.clf()
    plt.close('all')
