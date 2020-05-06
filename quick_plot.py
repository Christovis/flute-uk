"""make some quick plots analysising the result of flute run"""

import locale
import numpy as N
import pylab as P
import pandas as PD
import geopandas as GPD
import numpy.random as R
import plot_hospital_data as PHD

# if flute_dir is a list, make 4 plots from each of the directories on one page.
#flute_dir="./"

region = "northeast"
#region="ew"
if region == "northeast":
    #flute_dir= ["northeast-noaction/test_r0_1p0/","northeast-noaction/test_r0_1p5/","northeast-noaction/test_r0_2p0/","northeast-noaction/test_r0_3p0/"]
    flute_dir= "northeast-noaction/test_r0_3p0/"
    #flute_dir= "northeast-noaction/"
    tract_file = flute_dir + "northeast_tracts"
    log_file = "northeast_log"
    nomis_dir = "output_analysis/NorthEast/"
    old_file_type=True
    plot_title = "NorthEast"
    # total population ... need to find a neat way to read this from the summary file. Hardwire for NothEast for now.
    total_pop = N.array([158627,521126,343960,1279055,355487])
    offset = 0
else :
    flute_dir= "ew-lockdown-seedLondon/test_r0_3p0/"
    tract_file = flute_dir + "ew_tracts"
    log_file = "ew_log"
    nomis_dir = "output_analysis/EnglandWales/"
    old_file_type=False
    plot_title = "Englad and Wales"
    total_pop = N.array([3530963,11618091,7642752,28445028,7886388])
    offset = 1   # corrects for counting error in the translation tables

    
home_dir="./"



# fraction of people that show symptoms. Needs to be read from input file!
# symptomatic_fraction = 0.58
n_infected_days = 14  # the number of days in the Vload array. Used to calculate R0



flute_id = PD.read_csv(
    tract_file,
    delimiter=',',
    delim_whitespace=False,
)

# convert dictionaries from FluTe to NOMIS
RGN17CD_df = PD.read_csv(
    nomis_dir + "RGN17CD_dict.csv",
    delimiter=',',
    delim_whitespace=False,
)
RGN17CD_df = RGN17CD_df.rename(columns={"Unnamed: 0": "nomis id"})
LAD11CD_df = PD.read_csv(
    nomis_dir + "LAD11CD_dict.csv",
    delimiter=',',
    delim_whitespace=False,
)
LAD11CD_df = LAD11CD_df.rename(columns={"Unnamed: 0": "nomis id"})
MSOA11CD_df = PD.read_csv(
    nomis_dir + "MSOA11CD_dict.csv",
    delimiter=',',
    delim_whitespace=False,
)
MSOA11CD_df = MSOA11CD_df.rename(columns={"Unnamed: 0": "nomis id"})


print( "-------------------------" )


def read_flute_data(flute_dir):
    """read in the flute log file and return it"""
    log = PD.read_csv(
        flute_dir + log_file,
        delimiter=',',
        delim_whitespace=False,
        #dtype={'':int,'':str,'':int,'':int,'':int,'':int,'':int,'':int,'':int,'':int,'':int,'':int},
    )
    log["sym0-Inf"] = log[["sym0-4","sym5-18","sym19-29","sym30-64","sym65+"]].sum(axis=1)
    log["cumsym0-Inf"] = log[["cumsym0-4","cumsym5-18","cumsym19-29","cumsym30-64","cumsym65+"]].sum(axis=1)
    if not old_file_type :
        log["ninf0-Inf"] = log[["ninf0-4","ninf5-18","ninf19-29","ninf30-64","ninf65+"]].sum(axis=1)
        log["nsus0-Inf"] = log[["nsus0-4","nsus5-18","nsus19-29","nsus30-64","nsus65+"]].sum(axis=1)

    for flute_key in flute_id["TractID"].values:
        trans_key = flute_id[flute_id["TractID"] == flute_key]["FIPStract"].values[0] - offset  # counting issue : this needs -1 
        ok = (MSOA11CD_df["flute id"] == trans_key )   
        if not N.any(ok) : 
            print( "no key match ", flute_key)
        nomis_key = MSOA11CD_df[ok]["nomis id"].values[0]
        log["TractID"] = log["TractID"].replace(flute_key, nomis_key)

    # these are used to caculate the effective beta for the model. This can be use to compare to SIR model.
    log["betasum0-4"] = log["beta0-4"]*log["betacount0-4"]
    log["betasum5-18"] = log["beta5-18"]*log["betacount5-18"]
    log["betasum19-29"] = log["beta19-29"]*log["betacount19-29"]
    log["betasum30-64"] = log["beta30-64"]*log["betacount30-64"]
    log["betasum65+"] = log["beta65+"]*log["betacount65+"]
    log["betasum0-Inf"] = log[["betasum0-4","betasum5-18","betasum19-29","betasum30-64","betasum65+"]].sum(axis=1)
    log["betacount0-Inf"] = log[["betacount0-4","betacount5-18","betacount19-29","betacount30-64","betacount65+"]].sum(axis=1)
   
    time_list= N.unique(log["time"].values)
    totals = log.groupby(["time"]).sum()
    if not old_file_type :
        effective_beta = N.sum(totals["betasum0-Inf"].values)/N.sum((totals["ninf0-Inf"].values*totals["nsus0-Inf"].values))
        print( flute_dir, " ...effective beta of overall model: ", effective_beta )  # weighted sum of values each day+night
               
    print( "finished reading log file")
    return log


def plot_by_age_and_tract(log, npick=10):
    """plot number of symptomatic cases by tract and age"""
    tract_list = N.unique(log["TractID"])
    if npick!=0 :
        tract_list= tract_list[R.randint(0,len(tract_list),size=npick)]

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
    ax = P.axes()
    ax.ticklabel_format(style='sci')
    P.xlabel(r'time  [days]', fontsize=16)
    P.ylabel(r'sym', fontsize=16)
    P.title(plot_title)
    #P.legend(loc='best')

    
def plot_by_tract(log, npick=10):
    """plot number of symptomatic cases by tract"""

    tract_list = N.unique(log["TractID"])
    if npick!=0 :
        tract_list= tract_list[R.randint(0,len(tract_list),size=npick)]

    for tract in tract_list :
        ok = (log["TractID"] == tract)
        P.plot(
            log["time"].values[ok],
            log["sym0-Inf"].values[ok],
            label=tract
        )
    ax = P.axes()
    ax.ticklabel_format(style='sci', scilimits=(0,0))
    P.xlim([0, 180])
    P.xlabel(r'time  [days]', fontsize=16)
    P.ylabel(r'sym', fontsize=16)
    P.title(plot_title)
    P.legend(loc='best')

    
def plot_cumulative_by_age(log, logplot=False):
    """plot cumulative number of symptomatic cases by age"""

    time_list= N.unique(log["time"].values)
    totals = log.groupby(["time"]).sum()

    P.plot(
            time_list,
            totals["cumsym0-4"].values/total_pop[0],
            label="0-4"
        )    
    P.plot(
            time_list,
            totals["cumsym5-18"].values/total_pop[1],
            label="5-18"
        )    
    P.plot(
            time_list,
            totals["cumsym19-29"].values/total_pop[2],
            label="19-29"
        )    
    P.plot(
            time_list,
            totals["cumsym30-64"].values/total_pop[3],
            label="30-64"
        )    
    P.plot(
            time_list,
            totals["cumsym65+"].values/total_pop[4],
            label="65+"
        )    

    P.xlim([0, 180])
    if logplot:
        P.yscale('log')
        P.ylim(bottom=10./N.sum(total_pop), top =1.2)
        day = N.arange( 60 )
        P.plot( day,  2**(day/2.) / N.sum(total_pop), 'k:' )     # add a line showing 2 day doublinmg time for guidance.
        PHD.plot_hosital_data()
    P.xlabel(r'time  [days]', fontsize=16)
    P.ylabel(r'cumulative symptomatic fraction', fontsize=16)
    P.title(plot_title)
    P.legend(loc='best')

    
def plot_beta_by_age(log):
    """plot beta by tract and age. NB although number is given as beta, it really should be multiplied by total population."""

    time_list= N.unique(log["time"].values)
    totals = log.groupby(["time"]).sum()

    ax = P.axes()
    ax.ticklabel_format(style='sci', scilimits=(0,0))
    ax.plot(
        time_list,
        totals["betasum0-4"].values/(totals["ninf0-Inf"].values*totals["nsus0-4"].values),
        label="0-4"
        )    
    ax.plot(
        time_list,
        totals["betasum5-18"].values/(totals["ninf0-Inf"].values*totals["nsus5-18"].values),
        label="5-18"
        )    
    ax.plot(
        time_list,
        totals["betasum19-29"].values/(totals["ninf0-Inf"].values*totals["nsus19-29"].values),
        label="19-29"
        )    
    ax.plot(
        time_list,
        totals["betasum30-64"].values/(totals["ninf0-Inf"].values*totals["nsus30-64"].values),
        label="30-64"
        )    
    ax.plot(
        time_list,
        totals["betasum65+"].values/(totals["ninf0-Inf"].values*totals["nsus65+"].values),
        label="65+"
        )   
    ax.plot(
        time_list,
        totals["betasum0-Inf"].values/(totals["ninf0-Inf"].values*totals["nsus0-Inf"].values),
        label="all"
        )   
    
    P.xlim([0, 180])
    P.xlabel(r'time  [days]', fontsize=16)
    P.ylabel(r'beta', fontsize=16)
    P.ylim(bottom=0.)
    P.title(plot_title)
    P.legend(loc='best')

def plot_Rt_by_age(log):
    """plot beta by tract and age. NB although number is given as beta, it really should be multiplied by total population."""

    time_list= N.unique(log["time"].values)
    totals = log.groupby(["time"]).sum()

    ax = P.axes()
    ax.ticklabel_format(style='sci', scilimits=(0,0))
    ax.plot(
        time_list,
        n_infected_days * totals["betasum0-4"].values/(totals["ninf0-Inf"].values),
        label="0-4"
        )    
    ax.plot(
        time_list,
        n_infected_days * totals["betasum5-18"].values/(totals["ninf0-Inf"].values),
        label="5-18"
        )    
    ax.plot(
        time_list,
        n_infected_days * totals["betasum19-29"].values/(totals["ninf0-Inf"].values),
        label="19-29"
        )    
    ax.plot(
        time_list,
        n_infected_days * totals["betasum30-64"].values/(totals["ninf0-Inf"].values),
        label="30-64"
        )    
    ax.plot(
        time_list,
        n_infected_days * totals["betasum65+"].values/(totals["ninf0-Inf"].values),
        label="65+"
        )   
    ax.plot(
        time_list,
        n_infected_days * totals["betasum0-Inf"].values/(totals["ninf0-Inf"].values),
        label="all"
        )   
    
    P.xlim([0, 180])
    P.xlabel(r'time  [days]', fontsize=16)
    P.ylabel(r'Rt', fontsize=16)
    P.ylim(bottom=0.)
    P.title(plot_title)
    P.legend(loc='best')

def plot_withdrawn_by_age(log):
    """plot number of withdrawn individuals by tract and age"""
    
    time_list= N.unique(log["time"].values)
    totals = log.groupby(["time"]).sum()

    ax = P.axes()
    ax.ticklabel_format(style='sci', scilimits=(0,0))
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
    P.title(plot_title)
    P.legend(loc='best')

def plot_by_age(log):
    """plot number of symptomatic people as function of age"""

    time_list= N.unique(log["time"].values)
    totals = log.groupby(["time"]).sum()

    ax = P.axes()
    ax.ticklabel_format(style='sci', scilimits=(0,0))
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
    P.ylabel(r'number symptomatic individuals', fontsize=16)
    P.title(plot_title)
    P.legend(loc='best')

    
def plot_susceptible_by_age(log):
    """plot probability of infetion factor beta as a function of age"""

    time_list= N.unique(log["time"].values)
    totals = log.groupby(["time"]).sum()

    ax = P.axes()
    ax.ticklabel_format(style='sci', scilimits=(0,0))
    P.plot(
            time_list,
            totals["nsus0-4"].values,
            label="0-4"
        )    
    P.plot(
            time_list,
            totals["nsus5-18"].values,
            label="5-18"
        )    
    P.plot(
            time_list,
            totals["nsus19-29"].values,
            label="19-29"
        )    
    P.plot(
            time_list,
            totals["nsus30-64"].values,
            label="30-64"
        )    
    P.plot(
            time_list,
            totals["nsus65+"].values,
            label="65+"
        )    

    P.xlim([0, 180])
    P.xlabel(r'time  [days]', fontsize=16)
    P.ylabel(r'susceptible people', fontsize=16)
    P.title(plot_title)
    P.legend(loc='best')

    
def plot_infected_by_age(log):
    """plot probability of infetion factor beta as a function of age"""

    time_list= N.unique(log["time"].values)
    totals = log.groupby(["time"]).sum()

    ax = P.axes()
    ax.ticklabel_format(style='sci', scilimits=(0,0))
    ax.plot(
            time_list,
            totals["ninf0-4"].values,
            label="0-4"
        )    
    ax.plot(
            time_list,
            totals["ninf5-18"].values,
            label="5-18"
        )    
    ax.plot(
            time_list,
            totals["ninf19-29"].values,
            label="19-29"
        )    
    ax.plot(
            time_list,
            totals["ninf30-64"].values,
            label="30-64"
        )    
    ax.plot(
            time_list,
            totals["ninf65+"].values,
            label="65+"
        )    
    P.xlabel(r'time  [days]', fontsize=16)
    P.ylabel(r'infected people', fontsize=16)

    
def make_plots(fdir):
    """for single directory, just make the plots"""
    log = read_flute_data(fdir)
    P.figure()
    plot_by_age(log)
    P.savefig( flute_dir+"plot_by_age.png" )

    P.figure()
    plot_cumulative_by_age(log)
    P.savefig( flute_dir+"plot_cumulative_by_age.png" )

    P.figure()
    plot_cumulative_by_age(log, logplot=True)
    P.savefig( flute_dir+"plot_logcumulative_by_age.png" )

    P.figure()
    plot_withdrawn_by_age(log)
    P.savefig( flute_dir+"plot_withdrawn_by_age.png" )

    if not old_file_type :
        P.figure()
        plot_beta_by_age(log)
        P.savefig( flute_dir+"plot_beta_by_age.png" )

        P.figure()
        plot_Rt_by_age(log)
        P.savefig( flute_dir+"plot_Rt_by_age.png" )

        P.figure()
        plot_susceptible_by_age(log)
        P.savefig( flute_dir+"plot_susceptible_by_age.png" )

        P.figure()
        plot_infected_by_age(log)
        P.savefig( flute_dir+"plot_infected_by_age.png" )

    

def make_multi_plots(fdir_list):
    """loop over list of directories making the plots"""
    if (type(fdir_list) is list):
        P.figure(figsize=(10,10))
        for i, fdir in enumerate(fdir_list):
            log = read_flute_data(fdir)
            P.subplot(2,2,i+1)
            plot_by_age(log)
            P.title(fdir)
        P.savefig( "plot_by_age.png" )

        P.figure(figsize=(10,10))
        for i, fdir in enumerate(fdir_list):
            log = read_flute_data(fdir)
            P.subplot(2,2,i+1)
            plot_cumulative_by_age(log)
            P.title(fdir)
        P.savefig( "plot_cumulative_by_age.png" )

        P.figure(figsize=(10,10))
        for i, fdir in enumerate(fdir_list):
            log = read_flute_data(fdir)
            P.subplot(2,2,i+1)
            plot_withdrawn_by_age(log)
            P.title(fdir)
        P.savefig( "plot_withdrawn_by_age.png" )

        P.figure(figsize=(10,10))
        for i, fdir in enumerate(fdir_list):
            log = read_flute_data(fdir)
            P.subplot(2,2,i+1)
            plot_beta_by_age(log)
            P.title(fdir)
        P.savefig( "plot_beta_by_age.png" )

    else:
        print("only one directory, making simple plots")
        make_plots(fdir_list)



make_multi_plots(flute_dir)
P.show()
