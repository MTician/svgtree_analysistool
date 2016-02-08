# External Dependencies
from __future__ import division
import numpy as np
from operator import itemgetter

# Internal Dependencies
from scipy.stats import pearsonr
from stattools import shifted_and_patterned, ccorr
import options as opt


# single sample correlations
def align(rain, sampledata, pattern=None):
    results = []
    for sample in sampledata:
        cc = ccorr(rain, sample, opt.MAX_SHIFT, opt.MIN_OVERLAP, pattern)
        if cc:
            shift, r, p = min(cc, key=itemgetter(2))  # find best alignment by P-value
        else:
            shift, r, p = 'NA', 'NA', 'NA'
        results.append((shift, r, p, cc))
    return results


def alignment_pval(pvals):
    q = 1
    for pval in pvals:
        q *= 1 - pval
    return 1 - q


def forest_average(rain, trees, rain_test_patterns, test_tree_indices):

    test_trees = [trees[idx] for idx in test_tree_indices]
    ver_trees = [trees[idx] for idx in range(len(trees)) if
                 idx not in test_tree_indices]

    # Find which rain data test pattern gives best
    # alignment against test trees
    test_results = []
    for pattern in rain_test_patterns:
        # test_rain = [rain[idx] for idx in pattern]
        results = align(rain, test_trees, pattern=pattern)
        shifts = [res[0] for res in results]
        pvals = [res[2] for res in results]
        test_results.append((alignment_pval(pvals), pattern, shifts))

    best_result = min(test_results, key=itemgetter(0))
    best_pattern, best_shifts = best_result[1:3]

    # Align verification trees using best rain data test pattern
    # test_rain = [rain[idx] for idx in best_pattern]
    ver_results = align(rain, ver_trees, pattern=best_pattern)

    # Finally, correlate the above alignment with rain_ver to see how we did
    opp_of_best_pattern = [idx for idx in range(len(rain)) if
                           idx not in best_pattern]
    forest_results = []
    skipped_trees = []  # in case vtree's patterned overlap with rain too small
    for idx, vtree in enumerate(ver_trees):
        shift = ver_results[idx][0]
        crain, ctree = shifted_and_patterned(rain, vtree, shift,
                                             opp_of_best_pattern)
        if len(crain) < 3:
            r, p = 'NA', 'NA'
            skipped_trees.append(list(trees).index(vtree))
        else:
            r, p = pearsonr(crain, ctree)
        forest_results.append((shift, r, p, []))
    return forest_results, skipped_trees, best_pattern


def forest_average_brute(data):
    bla=1 # Brook maybe already wrote this.