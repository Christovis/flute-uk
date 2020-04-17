"""make some quick plots analysising the result of flute run"""

import locale
import numpy as N
import pylab as P
import pandas as PD
import geopandas as GPD

#flute_dir= "./northeast-close-schools/"
flute_dir= "./"
home_dir="./"

# total population ... need to find a neat way to read this from the summary file. Hardwire for NothEast for now.
total_pop = N.array([158627,521126,343960,1279055,355487])


log = PD.read_csv(
    flute_dir + "northeast_log",
    delimiter=',',
    delim_whitespace=False,
    #dtype={'':int,'':str,'':int,'':int,'':int,'':int,'':int,'':int,'':int,'':int,'':int,'':int},
)
log["sym0-inf"] = log[["sym0-4","sym5-18","sym19-29","sym30-64","sym65+"]].sum(axis=1)


print(log)

flute_id = PD.read_csv(
    flute_dir + "northeast_tracts",
    delimiter=',',
    delim_whitespace=False,
)

# convert dictionaries from FluTe to NOMIS
RGN17CD_df = PD.read_csv(
    home_dir + "input_ew/RGN17CD_dict.csv",
    delimiter=',',
    delim_whitespace=False,
)
RGN17CD_df = RGN17CD_df.rename(columns={"Unnamed: 0": "nomis id"})
LAD11CD_df = PD.read_csv(
    home_dir + "input_ew/LAD11CD_dict.csv",
    delimiter=',',
    delim_whitespace=False,
)
LAD11CD_df = LAD11CD_df.rename(columns={"Unnamed: 0": "nomis id"})
MSOA11CD_df = PD.read_csv(
    home_dir + "input_ew/MSOA11CD_dict.csv",
    delimiter=',',
    delim_whitespace=False,
)
MSOA11CD_df = MSOA11CD_df.rename(columns={"Unnamed: 0": "nomis id"})

for flute_key in flute_id["TractID"].values:
    trans_key = flute_id[flute_id["TractID"] == flute_key]["FIPStract"].values[0]
    nomis_key = MSOA11CD_df[MSOA11CD_df["flute id"] == trans_key]["nomis id"].values[0]
    log["TractID"] = log["TractID"].replace(flute_key, nomis_key)

print( log["cumsym0-4"].values )
print( log.index.values )
print( log["TractID"] )
print( log["time"] )

print( "-------------------------" )

def plot_by_age_and_tract():
    """plot number of symptomatic cases by tract and age"""
    tract_list = N.unique(log["TractID"])

    for tract in tract_list :
        ok = (log["TractID"] == tract)
        P.plot(
            log["time"].values[ok],
            log["sym0-4"].values[ok],
        )
        P.plot(
            log["time"].values[ok],
            log["sym5-18"].values[ok],
        )
        P.plot(
            log["time"].values[ok],
            log["sym19-29"].values[ok],
        )
        P.plot(
            log["time"].values[ok],
            log["sym30-64"].values[ok],
        )
        P.plot(
            log["time"].values[ok],
            log["sym65+"].values[ok],
        )
        P.xlim([0, 180])
    P.xlabel(r'time  [days]', fontsize=16)
    P.ylabel(r'sym', fontsize=16)
    P.title(r"North East")
    #P.legend(loc='best')

def plot_by_tract():
    """plot number of symptomatic cases by tract"""

    tract_list = N.unique(log["TractID"])

    for tract in tract_list :
        ok = (log["TractID"] == tract)
        P.plot(
            log["time"].values[ok],
            log["sym0-inf"].values[ok],
            label=tract
        )
    P.xlim([0, 180])
    P.xlabel(r'time  [days]', fontsize=16)
    P.ylabel(r'sym', fontsize=16)
    P.title(r"North East")
    P.legend(loc='best')

def plot_by_age():
    """plot number of symptomatic cases by tract and age"""

    time_list= N.unique(log["time"].values)
    totals = log.groupby(["time"]).sum()

    P.plot(
            time_list,
            totals["sym0-4"].values,
            label="0-4"
        )    
    P.plot(
            time_list,
            totals["sym5-18"].values,
            label="5-18"
        )    
    P.plot(
            time_list,
            totals["sym19-29"].values,
            label="19-29"
        )    
    P.plot(
            time_list,
            totals["sym30-64"].values,
            label="30-64"
        )    
    P.plot(
            time_list,
            totals["sym65+"].values,
            label="65+"
        )    

    P.xlim([0, 180])
    P.xlabel(r'time  [days]', fontsize=16)
    P.ylabel(r'sym', fontsize=16)
    P.title(r"North East")
    P.legend(loc='best')


def plot_withdrawn_by_age():
    """plot number of withdrawn individuals by tract and age"""

    time_list= N.unique(log["time"].values)
    totals = log.groupby(["time"]).sum()

    P.plot(
            time_list,
            totals["Withd0-4"].values/total_pop[0],
            label="0-4"
        )    
    P.plot(
            time_list,
            totals["Withd5-18"].values/total_pop[1],
            label="5-18"
        )    
    P.plot(
            time_list,
            totals["Withd19-29"].values/total_pop[2],
            label="19-29"
        )    
    P.plot(
            time_list,
            totals["Withd30-64"].values/total_pop[3],
            label="30-64"
        )    
    P.plot(
            time_list,
            totals["Withd65+"].values/total_pop[4],
            label="65+"
        )    

    P.xlim([0, 180])
    P.xlabel(r'time  [days]', fontsize=16)
    P.ylabel(r'fraction withdrawn individuals', fontsize=16)
    P.title(r"North East")
    P.legend(loc='best')



P.figure()
plot_by_age()
P.savefig( flute_dir+"plot_by_age.png" )

P.figure()
plot_withdrawn_by_age()
P.savefig( flute_dir+"plot_withdrawn_by_age.png" )
P.show()
