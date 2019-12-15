import PySimpleGUI as sg
import time
from lib.lib import *

def dupeop_default(row, other):
    # contact index
    comp = 27  # company index
    cont = 28  # contact name index
    title = 81 # job title index
    return (row[comp] == other[comp] and
            row[cont] == other[cont] and
            row[title] == other[title])

def mergeop_default(src, dest):
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

def merge_event(values):
    paths = values['-files-'].split(';')
    infos = [CSVInfo(path) for path in paths]
    rawtexts = [get_text(info) for info in infos]
    out = merge_all(rawtexts, dupeop_default, mergeop_default)
    save(infos[0], out, values['-output-'])

sg.change_look_and_feel('DarkAmber')
layout = [[sg.Text('Select the .csv files you want to merge.')],
          [sg.Text('Files', size=(15, 1)), sg.InputText(key='-files-'), sg.FilesBrowse()],
          [sg.Text('Output File', size=(15, 1)), sg.InputText(key='-output-'), sg.FileSaveAs(target='-output-')],
          [sg.Button('Merge'), sg.Cancel()]]

window = sg.Window('File Compare', layout)
while True:
    event, values = window.read()
    if event == None or event == 'Cancel':
        break
    elif event == 'Merge':
        merge_event(values)
    else:
        print(event)

event, values = window.read()
window.close()
