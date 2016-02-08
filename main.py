# External Dependencies
from __future__ import division
from math import sqrt
from operator import itemgetter
from scipy.stats import pearsonr
import numpy as np

# Internal Dependencies
from stattools import ccorr, shifted_and_patterned
from csvio import csv2arr, arr2csv, transpose
import patterns as pat
from alignment import *
import options as opt


############################################################
# Fake Data Setup for Debugging
############################################################
if opt.DEBUG_MODE_ON:
    from testingtools import gen_new_fake_data
    opt.RAINFALLDATA_FN = 'dummy_rainfalldata.csv'
    opt.SAMPLEDATA_FN = 'dummy_sampledata.csv'
    opt.RAIN_DATA_HAS_HEADERS = False
    opt.SAMPLE_DATA_HAS_HEADERS = False

if opt.GENERATE_NEW_FAKE_DATA:
    gen_new_fake_data(opt.N_RAIN, opt.N_SAMPLES, opt.REL_NOISE, opt.MEAN_SLOPE)


############################################################
# Data Pre-Processing
############################################################
assert opt.MAX_SHIFT >= 0
assert 0 <= opt.MIN_OVERLAP <= len(csv2arr(opt.RAINFALLDATA_FN))

# format and normalize rainfall data
rain = csv2arr(opt.RAINFALLDATA_FN, hasheaders=opt.RAIN_DATA_HAS_HEADERS)
rain = list(np.array(rain).T[0])  # convert Nx1 array to list


rain = [float(x) for x in rain]

# read and format sample data and take the transpose
# (so now each sample is a row)
sampledata = csv2arr(opt.SAMPLEDATA_FN, hasheaders=opt.SAMPLE_DATA_HAS_HEADERS)

# take the transpose (so now each sample is a row)
sampledata = transpose(sampledata)

# convert any strings to floats
sampledata = [[float(x) for x in sample if x] for sample in sampledata]


############################################################
# Analysis
############################################################
if not opt.DEBUG_MODE_ON:
    # Test single sample results if using generated fake data
    single_sample_results = align(rain, sampledata)
    print "\nSingle Sample Results:"
    q = 1
    for res in single_sample_results:
        q *= 1 - res[2]
        print "(shift, r, p) =", res[:3]
    print "Product P-value =", 1 - q

    # Test single sample results if using generated fake data
    test_patterns = [f(len(rain)) for f in opt.TEST_PATTERNS]
    test_tree_indices = opt.TEST_TREE_INDICES(len(sampledata))
    args = (rain, sampledata, test_patterns, test_tree_indices)
    forest_results, skipped_trees, best_pattern = forest_average(*args)
    print "\nForest Average Results:"
    print "best pattern =", best_pattern
    print "skipped trees: ", (str(skipped_trees)[1:-1]
                              if skipped_trees else 'None')
    q = 1
    for res in forest_results:
        shift, r, p = res[:3]
        if p != 'NA':
            q *= 1 - p
        print "(shift, r, p) =", res[:3]
    print "Product P-value =", 1 - q


############################################################
# Debug Test
############################################################
if opt.DEBUG_MODE_ON:
    # Test single sample results
    single_sample_results = align(rain, sampledata)
    from testingtools import test_shift_results, get_fake_data_params
    shifts = get_fake_data_params()[0]
    test_shift_results(single_sample_results, shifts)
    print ''

    # Test forest results
    test_patterns = [f(len(rain)) for f in opt.TEST_PATTERNS]
    test_tree_indices = opt.TEST_TREE_INDICES(len(sampledata))
    args = (rain, sampledata, test_patterns, test_tree_indices)
    forest_results, skipped_trees, best_pattern = forest_average(*args)
    from testingtools import test_shift_results, get_fake_data_params
    rshifts = get_fake_data_params()[0]
    rshifts = [k for idx, k in enumerate(rshifts) if
               idx not in test_tree_indices]
    test_shift_results(forest_results, rshifts)
    s = "skipped trees: "
    s += (str(skipped_trees)[1:-1] if skipped_trees else 'None')
    print s
