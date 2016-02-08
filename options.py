from __future__ import division
import patterns as pat


############################################################
# Parameters
############################################################

# rainfall data in chronological order (oldest to newest)
# note: this should be one column with no labels
RAINFALLDATA_FN = 'rain.csv'
RAIN_DATA_HAS_HEADERS = False  # first row is label

# sample data where each column is the averaged transect
# data to use from a different sample
SAMPLEDATA_FN = 'summary_data.csv'
# SAMPLEDATA_FN = 'samples.csv'
SAMPLE_DATA_HAS_HEADERS = True  # first row is labels

# maximum offset and in time between rain and sample data
# time series to test for
MAX_SHIFT = 1000
MIN_OVERLAP = 5  # minimum time overlap to consider

# Forest Average test patterns
# Note: any desired pattern that can be described as a
# function of n, the length of the rain data, can be used.
# Note: If you only want to use one test pattern, add a column
# to your data (on the far right) with dummy numbers and
# set TEST_TREE_INDICES = pat.onlylast

# TEST_PATTERNS = (pat.most,)
# TEST_PATTERNS = (pat.odds,
#                  pat.evens,
#                  pat.first_half,
#                  pat.second_half,
#                  pat.first_and_last_quarter)
# TEST_PATTERNS = (pat.most,)
# TEST_PATTERNS = (pat.firstseventy,)
TEST_PATTERNS = (pat.odds,)
TEST_TREE_INDICES = pat.onlylast

# Debugging options
DEBUG_MODE_ON = False
GENERATE_NEW_FAKE_DATA = False
N_RAIN = 50
N_SAMPLES = 10
REL_NOISE = .01  # This can be low, but should not be zero
MEAN_SLOPE = 1
