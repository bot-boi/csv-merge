# bunch of functions used for merging csv files

import csv
import logging # you should actually use this this time
import numpy as np


class CSVInfo:
    def __init__(self, path):
        self.path = path
        self.handle = open(path)

        sample = self.handle.read(2048)
        self.handle.seek(0)
        sniffer = csv.Sniffer()
        self.dialect = sniffer.sniff(sample)
        self.has_header = sniffer.has_header(sample)
        if self.has_header: # store column index -> name map
            self.header = get_text(self)[0]

def get_reader(info):
    return csv.reader(info.handle, info.dialect)

def get_writer(info, f): # file
    return csv.writer(f, dialect=info.dialect, escapechar='\\')

# returns a numpy array of the csv file
def get_text(info):
    result = np.array([row for row in get_reader(info)])
    info.handle.seek(0) # reset index for later reads
    return result

# save a csv file to disk
def save(info, arr, fpath):
    f = open(fpath, "w", newline="")
    w = get_writer(info, f)
    w.writerows(arr)
    f.close()

# operations on the raw numpy data

# accepts 1 or more columns
def get_columns(arr, colindices):
    return arr[...,colindices]

# acceppts 1 or more rows
def get_rows(arr, rowindices):
    return arr[rowindices]

# get column titles
# NOTE: some csv files don't have a header (?)
def get_header(arr):
    return arr[0]

# convert column name to index
def get_header_index(arr, name):
    header = get_header(arr)
    if name in header:
        return np.where(header == name)[0][0]
    else:
        raise Exception('{} is not a valid column title'.format(name))

# convert column index to name
def get_header_name(arr, index):
    return get_header(arr)[index]

# return indices of rows where ismatch is tru
def lookup(arr, ismatch):
    matches = []
    # ismatch is a fn that accepts a row
    for i,row in enumerate(arr):
        if ismatch(row):
            matches.append(i)
    return matches

# check for duplicates of a single row
# isdupe returns a boolean
def find_duplicates(arr, rowindex, isdupe):
    dupes = []
    row = arr[rowindex]
    for i,other in enumerate(arr):
        if rowindex != i:
            if isdupe(row, other):
                dupes.append(i)
    return dupes

# find duplicates for all rows in arr
# returns 2d array of indices
# each subarray is the indices of related duplicates
def find_all_duplicates(arr, isdupe):
    dupes = []
    for i,row in enumerate(arr):
        d = find_duplicates(arr, i, isdupe)
        if len(d) > 0:
            result = [i] + d
            result.sort()
            if result not in dupes:
                dupes.append(result)
    return dupes

# returns a dict (header names -> indices)
def get_header_map(arr):
    mmap = {}
    for i,coltitle in enumerate(get_header(arr)):
        mmap.update({coltitle: i})
    return mmap

# naive implementation of a merge
# generates a csv file from two csv files
# arr & other are csv files in numpy form
# isdupe is the row comparison fn -- isdupe(row, other)
# merge_op is what runs when fields of two duplicate rows are merged
# merge_op(source, dest)
def merge(arr, other, isdupe, merge_op):
    out = list(arr) + list(other[1:]) # ignore header row in other
    dupes = find_all_duplicates(out, isdupe)
    for group in dupes:
        outrow = [''] * len(get_header(arr)) # TODO: undo temp fix
        for dupeid in group:
            dupe = out[dupeid]
            for i,field in enumerate(dupe):
                # print(i, len(dupe))
                if i < len(outrow):
                    outrow[i] = merge_op(field, outrow[i])
                else:
                    print(dupeid)
        out.append(outrow)

    logging.debug("Duplicates from merging databases, size {} & {} respectively\n {}".format(len(arr), len(other), dupes))
    for group in dupes:
        for dupeid in group:
            out[dupeid] = [''] * len(get_header(out))

    out1 = [row for row in out if not np.all(row == ['']*len(get_header(out)))]

    return out1

def merge_all(arrs, isdupe, merge_op):
    out = []
    for arr in arrs:
        out = merge(arr, out, isdupe, merge_op)
    return out
