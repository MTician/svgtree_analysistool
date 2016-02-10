from __future__ import division
from math import sqrt
from operator import itemgetter
import numpy as np
gauss = np.random.rand

from stattools import *
from csvio import csv2arr, arr2csv, transpose

########################
# Generate fake test data
########################
def gen_new_fake_data(n_rain=50, n_samples=10,
                      rel_noise=2, mean_slope=5):
    dummy_rain = np.array([[abs(x)] for x in gauss(50)])
    arr2csv(dummy_rain, 'dummy_rainfalldata.csv')

    sample_sizes = np.random.randint(n_rain//4, n_rain*2, n_samples)

    if opt.TEST_FALSE_CASE:
        dummy_samples = [abs(gauss(sz)) * rel_noise for sz in sample_sizes]

    else:
        max_shift = opt.MAX_FAKE_DATA_SHIFT
        shifts = np.random.randint(-max_shift, max_shift, n_samples)
        slopes = np.array([abs(x) for x in gauss(n_samples)]) + mean_slope

        constants = [abs(x) for x in gauss(n_samples)]
        dummy_samples = []
        for idx, shift in enumerate(shifts):
            sample_size = sample_sizes[idx]
            sample = gauss(sample_size) * rel_noise  # add noise
            rainyr_first = shift
            rainyr_last = shift + n_rain - 1
            transformed_rain = slopes[idx] * dummy_rain + constants[idx]
            if shift > 0:
                time_period = range(shift, shift + n_rain)
                for rain_yr, yr in enumerate(time_period):
                    try:
                        # sample[shift] <-- rain[0]
                        sample[yr] += transformed_rain[rain_yr]
                    except IndexError:
                        continue
            else:
                time_period = range(abs(shift), abs(shift) + n_rain)
                for yr, rain_yr in enumerate(time_period):
                    try:
                        # sample[0] <-- rain[shift]
                        sample[yr] += transformed_rain[rain_yr]
                    except IndexError:
                        continue
            dummy_samples.append([abs(x) for x in sample])

        arr2csv([shifts, slopes, constants], 'dummy_params.csv')
    arr2csv(transpose(dummy_samples), 'dummy_sampledata.csv')


def get_fake_data_params():
    shifts, slopes, constants = csv2arr('dummy_params.csv', dtype=float)
    shifts = [int(x) for x in shifts]
    return shifts, slopes, constants


def shiftres(shft, cc):
    for rs in cc:
        if shft == rs[0]:
            return rs
    else:
        return "shift not found"


def test_shift_results(results, expected_shifts):
    shifts = expected_shifts

    # Check results against parameters
    for idx, res in enumerate(results):
        if shifts[idx] == res[0]:
            print ':)', shifts[idx], res[:3]
        else:
            print 'fail', shifts[idx], res[:3]
            # print '....', shiftres(shifts[idx], res[3])
