# External Dependencies
from __future__ import division
from math import sqrt, ceil, log10
from operator import itemgetter
from scipy.stats import pearsonr
import numpy as np

# Internal Dependencies
from stattools import ccorr, shifted_and_patterned
from csvio import csv2arr, arr2csv, transpose
import patterns as pat
from alignment import *
import options as opt
from patterns import pattern_dict


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
        args = (opt.N_RAIN, opt.N_SAMPLES, opt.REL_NOISE, opt.MEAN_SLOPE)
        gen_new_fake_data(*args)


############################################################
# Data Pre-Processing
############################################################
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
if not opt.DEBUG_MODE_ON or opt.TEST_DUMMY_RESULTS_LIKE_THEY_ARE_REAL:
    # Test single sample results if using generated fake data
    single_sample_results, probs = align(rain, sampledata)
    print "\nSingle Sample Results:"
    q = 1
    print "# : (p < {}, p, r, shift)".format(opt.ALPHA)
    digs = int(ceil(log10(len(single_sample_results))))
    for idx, res in enumerate(single_sample_results):
        id = str(idx).zfill(digs)
        if res[0]!='NA':
            args = (probs[idx] < opt.ALPHA, probs[idx], res[1], res[0])
            print "{} : ({}, {:.3f}, {:+.3f}, {})".format(id, *args)
        else:
            print "{} : skipped".format(id)

    # Forest Average results
    test_pat_funcs = [pattern_dict[test] for test in opt.TEST_PATTERNS]
    test_patterns = [f(len(rain)) for f in test_pat_funcs]
    test_tree_indices = pattern_dict[opt.TEST_TREE_PATTERN](len(sampledata))
    args = rain, sampledata
    forest_results, skipped_trees, best_pattern = forest_average(*args)
    print "\nForest Average Results:"
    print "best pattern =", best_pattern
    print "skipped trees: ", (str(skipped_trees)[1:-1]
                              if skipped_trees else 'None')
    print "# : (p < {}, p, r, shift)".format(opt.ALPHA)
    digs = int(ceil(log10(len(forest_results))))
    for idx, res in enumerate(forest_results):
        id = str(idx).zfill(digs)
        if res[2]!='NA':
            args = (res[2] < opt.ALPHA, res[2], res[1], res[0])
            print "{} : ({}, {:.3f}, {:+.3f}, {})".format(id, *args)
        else:
            print "{} : skipped".format(id)


############################################################
# Debug Test
############################################################
if opt.DEBUG_MODE_ON and not opt.TEST_DUMMY_RESULTS_LIKE_THEY_ARE_REAL:
    # Test single sample results
    single_sample_results, probs = align(rain, sampledata)
    from testingtools import test_shift_results, get_fake_data_params
    shifts = get_fake_data_params()[0]

    print "\nSingle Sample Results:"
    if opt.TEST_FALSE_CASE:
        print "(p < 0.01, p, r, shift)"
        for idx, res in enumerate(single_sample_results):
            args = (probs[idx] < 0.01, probs[idx], res[1], res[0])
            print "({}, {:.3f}, {:+.3f}, {})".format(*args)
    else:
        test_shift_results(single_sample_results, shifts)
    print ''

    # Test forest results
    test_tree_indices = pattern_dict[opt.TEST_TREE_PATTERN](len(sampledata))
    args = rain, sampledata
    forest_results, skipped_trees, best_pattern = forest_average(*args)
    from testingtools import test_shift_results, get_fake_data_params
    rshifts = get_fake_data_params()[0]
    rshifts = [k for idx, k in enumerate(rshifts) if
               idx not in test_tree_indices]

    print "\nForest Average Results:"
    print "best pattern =", best_pattern
    print "skipped trees: ", (str(skipped_trees)[1:-1]
                              if skipped_trees else 'None')
    if opt.TEST_FALSE_CASE:
        print "(p < 0.01, p, r, shift)"
        for idx, res in enumerate(forest_results):
                if res[0]!='NA':
                    args = (res[2] < 0.01, res[2], res[1], res[0])
                    print "({}, {:.3f}, {:+.3f}, {})".format(*args)
                else:
                    print "skipped"
    else:
        test_shift_results(forest_results, rshifts)
    s = "skipped trees: "
    s += (str(skipped_trees)[1:-1] if skipped_trees else 'None')
    print s
