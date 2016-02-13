# External Dependencies
from __future__ import division
import numpy as np
from operator import itemgetter

# Internal Dependencies
from stattools import shifted_and_patterned, ccorr
from correlation_tests import test_dict
import options as opt
from patterns import pattern_dict

correlation_test = test_dict[opt.CORRELATION_TEST]


def align(rain, sampledata, pattern=None):
    results = []
    probs = []
    for sample in sampledata:
        cc = ccorr(rain, sample, opt.MIN_SHIFT, opt.MAX_SHIFT,
                   opt.MIN_OVERLAP, pattern)
        if cc:
            # find best alignment by P-value
            shift, r, p = min(cc, key=itemgetter(2))

            # find the probability of getting such a good P-value by random
            # chance in len(cc) tests
            num_tests = len([x for x in cc if x[0] != 'NA'])
            prob = 1 - (1 - p)**num_tests

        else:
            shift, r, p, prob = 'NA', 'NA', 'NA', 1
        results.append((shift, r, p, cc))
        probs.append(prob)
    return results, probs


def pattern_score(pvals):
    """This function is meant to score how well a pattern did so it can be
    compared against others."""
    q = 1
    for p in pvals:
        q *= 1-p
    return 1 - q


def forest_average(rain, trees):
    rain_test_patterns = opt.TEST_PATTERNS
    test_tree_indices = pattern_dict[opt.TEST_TREE_PATTERN](len(trees))
    test_trees = [trees[idx] for idx in test_tree_indices]
    ver_trees = [trees[idx] for idx in range(len(trees)) if
                 idx not in test_tree_indices]

    # Find which rain data test pattern gives best
    # alignment against test trees
    test_results = []
    for pattern in rain_test_patterns:
        # test_rain = [rain[idx] for idx in pattern]
        results, probs = align(rain, test_trees, pattern=pattern)
        shifts = [res[0] for res in results]
        pvals = [res[2] for res in results]
        score = pattern_score(pvals)
        test_results.append((score, pattern, shifts))

    best_result = min(test_results, key=itemgetter(0))
    best_pattern, best_shifts = best_result[1:3]

    # Align verification trees using best rain data test pattern
    ver_results, prob = align(rain, ver_trees, pattern=best_pattern)

    # Finally, correlate the above alignment with rain_ver to see how we did
    best_pat_fcn = pattern_dict[best_pattern]
    opp_of_best_pattern = lambda n: list(set(range(n)) - set(best_pat_fcn(n)))
    forest_results = []
    skipped_trees = []  # in case vtree's patterned overlap with rain too small
    for idx, vtree in enumerate(ver_trees):
        shift = ver_results[idx][0]
        if shift != 'NA':
            crain, ctree = shifted_and_patterned(rain, vtree, shift,
                                                 opp_of_best_pattern)
        if shift == 'NA' or len(crain) < 3:
            r, p = 'NA', 'NA'
            skipped_trees.append(list(trees).index(vtree))
        else:
            r, p = correlation_test(crain, ctree)
        forest_results.append((shift, r, p, []))
    return forest_results, skipped_trees, best_pattern


def forest_average_brute(data):
    bla=1 # Brook maybe already wrote this.