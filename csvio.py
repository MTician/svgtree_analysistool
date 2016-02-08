from copy import copy
# def transpose_old(rows):
#     num_cols = max(len(row) for row in rows)
#     cols = []
#     for j in range(num_cols):
#         cols.append([row[j] for row in rows if len(row) > j])
#     return cols
def transpose(arr, empty_cell=''):
    num_rows = max(len(row) for row in arr)
    num_cols = len(arr)
    new_arr = [['']*num_cols for dummy in range(num_rows)]
    for i in range(num_rows):
        for j in range(num_cols):
            try:
                new_arr[i][j] = arr[j][i]
            except IndexError:
                pass

    # get rid of commas at end of rows
    for i, row in enumerate(new_arr):
        for j in range(len(row)):
            if row[len(row) - j - 1] != '':
                new_arr[i] = row[:len(row) - j]
                break
    return new_arr



def csv2arr(csvfile, delimiter=',', dtype=None, hasheaders=False,
            return_headers=False):
    """Converts a csv file to a numpy matrix, data, where data[i][j] is the
    data from the ith row jth column.  Note: Assumes comma-delimited by
    default.
    If you want to make sure the data is returned as a certain type, use
    set the dtype (e.g. dtype=float, dtype=int, or dtype=str)."""
    data = []
    headers = []
    with open(csvfile) as f:
        for line_num, line in enumerate(f):
            # get rid of any line end characters and split (using delimiter)
            # into list
            rowvec = line.replace('\r', '').replace('\n', '').split(delimiter)
            if hasheaders and not line_num:
                headers = rowvec
                continue
            if dtype:
                rowvec = [dtype(x) for x in rowvec]
            data.append(rowvec)
    if return_headers:
        return data, headers
    else:
        return data


def arr2csv(arr, filename, mode='w', delimiter=','):
    """Writes an array to a csv file.
    Note: use mode='w' to overwrite file or mode='a' to append to file)."""
    # Convert array to string
    s = ''
    for row in arr:
        s += delimiter.join(str(x) for x in row) + '\n'
    s = s[:-1]  # Remove last line end

    # Write string to csv.
    with open(filename, mode) as f:
        f.write(s)
