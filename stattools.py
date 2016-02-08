from __future__ import division
from math import sqrt
from scipy.stats import pearsonr
import numpy as np


# import warnings
# def pearsonr(x, y):
#     with warnings.catch_warnings():
#         warnings.filterwarnings('error')
#         try:
#             return pear(x, y)
#         except Warning:
#             print Warning
#             res = pear(x, y)
#             raise Exception()


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
        xp = [val for i, val in enumerate(xp) if i in pattern]
        yp = [val for i, val in enumerate(yp) if i in pattern]
    if crop:
        win_size = min(len(xp), len(yp))
        xp = xp[:win_size]
        yp = yp[:win_size]
    return xp, yp


def shifted(x, y, k, pattern=None):
    """Returns cropped subsequences of maximal length that
    align x[0] with y[k]"""
    # if k > 0:  # x[0] aligns with y[k]
    #     win_size = min(len(x), len(y[k:]))
    #     x_win = x[0:win_size]
    #     y_win = y[k:k + win_size]
    # else:  # x[k] aligns with y[0]
    #     win_size = min(len(x[abs(k):]), len(y))
    #     x_win = x[abs(k):abs(k) + win_size]
    #     y_win = y[0:win_size]
    return shifted_and_patterned(x, y, k)


def ccorr(x, y, max_shift, min_overlap, pattern=None):
    """returns the cross-correlations as a list of triples (k, r, p) where
    r and p are the peasrson correlation coefficient and associated P-value
    for when aligning x[0] with y[k]."""
    res = []
    for shft in xrange(0 - max_shift, max_shift + 1):
        x_win, y_win = shifted(x, y, shft, pattern=pattern)
        if len(x_win) < min_overlap:
            continue
        r, p = pearsonr(x_win, y_win)
        res.append((shft, r, p))
    return res

