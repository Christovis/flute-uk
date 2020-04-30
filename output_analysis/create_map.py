import sys, argparse, locale
import numpy as np
import pandas as pd
import geopandas as gpd

from pylab import cm                                                             
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.pyplot import figure
#plt.style.use("publication.mplstyle")

region = "output_analysis/EnglandWales"
run_dir = "ew-noaction/test_r0_2p0/"

# load encoder to get from FluTE internal to naming convection of input data
flute_trans = pd.read_csv(
    run_dir +"/ew_tracts",
    delimiter=',',
    delim_whitespace=False,
)
flutelog_df = pd.read_csv(
    run_dir + "ew_log",
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
    trans_key = flute_trans[flute_trans["TractID"] == flute_key]["FIPStract"].values[0] - 1  # counting issue : this needs -1 
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
ew_shape = gpd.read_file("output_analysis/"+'%s/%s.shp' % (shape_file, shape_file))
ew_shape = ew_shape.set_index('msoa11cd')


# crea maps for each day in simulation
for day in np.unique(flutelog_df["time"].values):
    flute_day = flutelog_df[flutelog_df["time"] == day].set_index('TractID')

   # Plot
    fig, ax_map = plt.subplots(
        1, 1, sharex=False, sharey=False,
        figsize=(7.5, 7.5),
        facecolor="w", edgecolor="k",
    )

    ew_day = ew_shape.merge(
        flute_day[["time", "cumsym0-inf"]],
        left_index=True,
        right_index=True
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
#    ew_shape.plot(
#        ax=ax_map,
#        facecolor="none",
#        edgecolor='black',
#        linewidth=0.5,
#        categorical=False,
#        )
    ax_map.axis('off')
    plt.savefig(run_dir + "ew_day%d_map.png"%day, dpi=150)
    print( "finished plot for day ", day )
    plt.close()


    
