import sys
sys.path.insert(0,'..')


import pygame
from pygame.locals import *
from pgu import gui
import main
import difficulty
import error


def open_file_browser(arg):
    #open a file dialog, allow user choose their own file
    dialog=gui.FileDialog()
    dialog.connect(gui.CHANGE,handle_file_browser_closed,dialog)
    dialog.open()


def handle_file_browser_closed(dlg):
    #convert path into a readable string
    w_pos=-3 #*.wav, so pos of w is -3
    if dlg.value: INPUT_FILE.value=dlg.value
    if INPUT_FILE.value[w_pos:len(INPUT_FILE.value)]=='wav':
        return INPUT_FILE.value
    else: return False #error: not wav file

def run_game(event):
    file=handle_file_browser_closed(INPUT_FILE)
    items=['Easy','Medium','Hard','Main Menu']
    if file==False: error.Error(SCREEN).run()
    else: difficulty.GameMenu(SCREEN,items,file).run()


#gui.theme.load('../data/themes/default')
APP=gui.Desktop()
APP.connect(gui.QUIT,APP.quit,None)

MAIN_WINDOW=gui.Container(width=500,height=400)#,background=(220,220,220))

TD_POS=10
TD_STYLE={'padding_right':TD_POS} #style of the window in PGU
TABLE=gui.Table() #file path table
TABLE.tr()
TABLE.td(gui.Label('File Name:'),style=TD_STYLE)
INPUT_FILE=gui.Input()
TABLE.td(INPUT_FILE,style=TD_STYLE)
BUTTON1=gui.Button("Browse...") #browse button
TABLE.td(BUTTON1,style=TD_STYLE)
BUTTON1.connect(gui.CLICK,open_file_browser,None)
BUTTON2=gui.Button("Continue") #start game button
TABLE.td(BUTTON2,style=TD_STYLE)
BUTTON2.connect(gui.CLICK,run_game,None)

MAIN_WINDOW_POS1, MAIN_WINDOW_POS2=20,100
MAIN_WINDOW.add(TABLE,MAIN_WINDOW_POS1,MAIN_WINDOW_POS2)

class Choose_File(object):
    def __init__(self,screen):
        global SCREEN
        SCREEN=screen

    def go(self):
        APP.run(MAIN_WINDOW)
