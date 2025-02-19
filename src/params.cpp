/*
 * params.cpp
 * constants for FluTE
 *
 * Shufu Xu
 * 11.01.2006
 * Modified and recalibrated by Dennis Chao (April 2010)
 * Modified and recalibrated for UK by Christoph Becker (April 2020)
 */

#include <climits>
#include "params.h"

const double fAG0InfantFraction=0.09923; // fraction of those in age group 0 who are <6 months

// contact probabilities
const double cpw= 0.05; // workplace
const double cps[10] = {0.0, 0.0252, 0.03, 0.0348, 0.0348, 0.12, 0.12, 0.12, 0.12, 0.28}; // school, 10 values for:
//      none, high school, middle school, elementary (2), day care (4), play group
const double cpcm[TAG] = {0.0000109, 0.0000326, 0.000087, 0.000087, 0.000174}; // community
const double cpnh[TAG] = {0.0000435, 0.0001305, 0.000348, 0.000348, 0.000696}; // neighborhood
const double cpfc[TAG] = {0.8, 0.8, 0.37, 0.37, 0.37};         // family from children
const double cpfa[TAG] = {0.25, 0.25, 0.37, 0.37, 0.37};       // family from adults
const double cphcc[TAG] = {0.08, 0.08, 0.037, 0.037, 0.037};   // household cluster from children
const double cphca[TAG] = {0.025, 0.025, 0.037, 0.037, 0.037}; // household cluster from adults

// withdraw probabilities
const double withdrawprob[3][WITHDRAWDAYS] = {
  {0.304, 0.575, 0.324},  // preschool children
  {0.203, 0.498, 0.375},  // school children
  {0.100, 0.333, 0.167}	  // adults
};

// self isolation probabilities by age
const double isolationprob[TAG] = {0.8,0.75,0.5,0.5,0.5};

const int nQuarantineLength = 14; // length of quarantine in days
const int nAntiviralCourseSize = 10; // number of pills in one antiviral course (1 tablet/day for prophylaxis and 2 tablets/day for treatment)
const double fStopAntiviralTwoPills = 0.05; // probability that individuals taking antivirals stop after exactly two pills

// cdf of duration for incubation period in days
const double incubationcdf[3] = {0.01, 0.05, 0.18, 0.38, 0.54, 0.7, 0.87, 0.9, 0.92, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0};

// viral load trajectories
// source: https://doi.org/10.1038/s41591-020-0869-5
const double basevload[VLOADNSUB][VLOADNDAY] = {
	{9.0, 8.5, 8.0, 7.5, 7.0, 6.5, 6.0, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5}
};

// travel data
double const travel_pr[TAG] = {
    .0023,
    .0023,
    .0050,
    .0053,
    .0028
}; // age-specific travel probability per day
double const travel_length_cdf[12] = {
    0.239,
    0.406,
    0.574,
    0.741,
	0.787,
    0.834,
    0.880,
    0.926,
	0.945,
    0.963,
    0.982,
    1.0
}; // cdf of length of trip in days (nights away from home)

// Source: "CAA Airport Data 2018". caa.co.uk. UK Civil Aviation Authority. 13 March 2019. Retrieved 13 March 2019.
// Biggest airports of the England and Wales
// last three digits = LAD11CD id
// first digits = RGN17CD id
const unsigned int FIPS_hubs[] = {
    8039, //LHR
    8248, //LGW
    2260, //MAN
    6130, //STN
    6032, //LTN
    5282, //BHX
    9023, //BRS
    1278, //NCL
    2269, //LPL
    4015, //EMA
    7294, //LCY
    3292, //LBA
};
// Total number of passengers trafficed in 2018.
// Source : "CAA Airport Data 2018". caa.co.uk. UK Civil Aviation Authority.
// 13 March 2019. Retrieved 13 March 2019.
const unsigned int Size_hubs[] = {
    80124537,
    46086089,
    28292797,
    27996116,
    16769634,
    12457051,
    8699529,
    5334095,
    5046995,
    4873831,
    4820292,
    4038889,
}; 
