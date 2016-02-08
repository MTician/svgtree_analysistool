"""Given a directory containing transect summaries output by svgtree,
this script will create a single csv file appropriate for use with
svgtree_analysistool.
Note: The csv file output will have headers, '<svg_filename>_(m-k-x)' where
m - is the transect number,
k - specifies which of the 11 rows explained below this particlar column comes
    from and,
x - is the relevant row number from the original transect summary csv file
    as it will appear if opened in excel (excel ignores blank rows).

Use:
Put a bunch of transect summary csv files in a folder named summaries, put
that folder in the folder containing this script.  Then run this script
(i.e. open a terminal in the folder containing this script and enter
'python summaryparser.py').

With the default settings this will take the 'raw w/o zeros' and
'raw with zeros' data from the first 10 transects of each input csv.
To change these settings, see the "parameters" section below.
"""
import os
import options as opt
from csvio import transpose, csv2arr, arr2csv

# Note that for each transect average, svgtree outputs 11 rows, and the first
# 4 rows of each summary are just boiler plate (including the third row, which
# is blank)
# 0)  arrow guide
# 1)  closure
# 2)  raw w/o zeros
# 3)  raw with zeros
# 4)  normalized w/o zeros
# 5)  normalized with zeros
# 6)  renormalized raw w/o zeros
# 7)  renormalized raw with zeros
# 8)  renormalized normalized w/o zeros
# 9)  renormalized normalized with zeros
# 10) blank row

# Parameters #######################################

# Select which of the 11 rows to include in the analysis (use 0 for first row)
# if None, defaults to [2, 3] (i.e. 'raw w/o zeros' and 'raw with zeros')
rows2grab = None

# Select which transects to include in the analyis
# if None, defaults to [0, 1, ..., 9] (i.e. first 10 transects - meaning rows
# 7, 18, 29, etc. from each csv file)
trans2grab = None

# Directory with summary data
# if None, defaults to the 'summaries' subdirectory of the folder containing
# this script.
summary_dir = None

# name of output csv file
# if None, defaults to 'summary_data.csv' (in the folder containing this
# script)
outf = None

#####################################################
# set defaults
if not rows2grab:
    rows2grab = [2, 3]
if not trans2grab:
    trans2grab = range(10)
if not summary_dir:
    summary_dir = os.path.join(os.getcwd(), 'summaries')
if not outf:
    outf = 'summary_data.csv'

# do stuff
data = []
data_guide = []
for fn in os.listdir(summary_dir):
    path2summary = os.path.join(summary_dir, fn)
    summary = csv2arr(path2summary)[4:] # throw out first 4 rows
    for m in trans2grab:
        for k in rows2grab:
            data.append(summary[11*m + k][3:])
            x = 10*m + k + 4  # in original csv (not counting blank rows)
            data_guide.append(fn[:-4] + '_({}-{}-{}))'.format(m, k, x))

data = transpose(data)
data.insert(0, data_guide)
arr2csv(data, filename=outf)
