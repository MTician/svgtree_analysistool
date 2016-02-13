from __future__ import division


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

# min/max offset and in time between rain and sample data
# time series to test for
# Note: min should be negative if trees are older than first
# year of rain data
MIN_SHIFT = -50
MAX_SHIFT = 50
MIN_OVERLAP = 10  # minimum time overlap to consider

# Forest Average test patterns (see patterns.py for options)
# Note: If you only want to use one test pattern, add a column
# to your data (on the far right) with dummy numbers and
TEST_PATTERNS = ['first_seventy']
TEST_TREE_PATTERN = 'only_last'

# See correlation_tests.py for choices.
CORRELATION_TEST = 'pearson'
# CORRELATION_TEST = 'spearman'
# CORRELATION_TEST = 'kendall'

# Debugging options
DEBUG_MODE_ON = False
TEST_FALSE_CASE = False  # If true, all tests are expected to fail
GENERATE_NEW_FAKE_DATA = True
TEST_DUMMY_RESULTS_LIKE_THEY_ARE_REAL = True
N_RAIN = 500
N_SAMPLES = 10
REL_NOISE = .01  # This can be low, but should not be zero
MEAN_SLOPE = 1
MAX_FAKE_DATA_SHIFT = MAX_SHIFT
