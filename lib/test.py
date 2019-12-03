from lib import *

info = CSVInfo("../data.csv")
arr = get_text(info)
hmap = get_header_map(arr)

def dupefn(row, other):
    # contact index
    ci = 28
    return row[ci] == other[ci]

def mergefn(src, dest):
    if src in dest:
        return dest
    elif dest in src:
        return src
    else:
        return src + dest
