import os
import options as opt
from csvio import transpose, csv2arr, arr2csv

# Note that for each transect average, svgtree outputs 11 rows
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
rows2grab = [2, 3]

# Select which transects to include in the analyis
trans2grab = range(10)

# Directory with summary data (defaults to subfolder 'summaries' of input
# folder specified in options)
summary_dir = os.path.join(os.getcwd(), 'summaries')

# name of output csv file
outf = 'summary_data.csv'

#####################################################


if (not summary_dir
    and os.path.exists()):
    summary_dir = os.path.join(opt.INPUT_DIRECTORY, 'summaries')
else:
    summary_dir = os.path.join(os.getcwd(), 'summaries')

data = []
data_guide = []
for fn in os.listdir(summary_dir):
    path2summary = os.path.join(summary_dir, fn)
    summary = csv2arr(path2summary)[4:] # throw out first 4 rows
    for m in trans2grab:
        for k in rows2grab:
            data.append(summary[11*m + k][3:])
            rownum = 10*m + k + 4  # in original csv (not counting blank rows)
            data_guide.append(fn[:-4] + '_({}-{}-{}))'.format(m, k, rownum))

data = transpose(data)
data.insert(0, data_guide)
arr2csv(data, filename=outf)






