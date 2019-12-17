from lib.lib import *

info = CSVInfo("mine.csv")
info30 = CSVInfo("alan30.csv")
info1200 = CSVInfo("alan1200.csv")
arr30 = get_text(info30)
arr1200 = get_text(info1200)
arr = get_text(info)
hmap = get_header_map(arr)

def dupefn(row, other):
    # contact index
    comp = 27  # company index
    cont = 28  # contact name index
    title = 81 # job title index
    return (row[comp] == other[comp] and
            row[cont] == other[cont] and
            row[title] == other[title])

def mergefn(src, dest):
    if src == "" and dest != "": # handle "" comparison case
        return dest
    elif dest == "" and src != "":
        return src
    elif src in dest:
        return dest
    elif dest in src:
        return src
    else:
        return src + dest
