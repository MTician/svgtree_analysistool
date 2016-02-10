from __future__ import division
from math import sqrt
from correlation_tests import test_dict
import numpy as np
import options as opt
import patterns as pat

correlation_test = test_dict[opt.CORRELATION_TEST]


def shifted_and_patterned(x, y, k, pattern=None, crop=True):
    """Returns cropped subsequences of maximal length that
    align x[0] with y[k]."""
    if k > 0:  # x[0] aligns with y[k]
        xp = x[0:]
        yp = y[k:]
    else:  # x[k] aligns with y[0]
        xp = x[abs(k):]
        yp = y[0:]
    if pattern:
        if isinstance(pattern, str):
            pat_range = pat.pattern_dict[pattern](len(xp))
        else:
            pat_range = pattern(len(xp))
        xp = [val for i, val in enumerate(xp) if i in pat_range]
        yp = [val for i, val in enumerate(yp) if i in pat_range]
    if crop:
        win_size = min(len(xp), len(yp))
        xp = xp[:win_size]
        yp = yp[:win_size]
    return xp, yp


def shifted(x, y, k, pattern=None):
    """Returns cropped subsequences of maximal length that
    align x[0] with y[k]"""
    return shifted_and_patterned(x, y, k, pattern=pattern)


def ccorr(x, y, max_shift, min_overlap, pattern=None):
    """returns the cross-correlations as a list of triples (k, r, p) where
    r and p are the peasrson correlation coefficient and associated P-value
    for when aligning x[0] with y[k]."""
    res = []
    for shft in xrange(0 - max_shift, max_shift + 1):
        x_win, y_win = shifted(x, y, shft, pattern=pattern)
        if len(x_win) < min_overlap:
            continue
        r, p = correlation_test(x_win, y_win)
        res.append((shft, r, p))
    return res

