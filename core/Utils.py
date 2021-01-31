# -*- coding: utf-8 -*-

import glob
import os
from PyQt5 import uic

class Utils():
    def __init__(self):
        dirs = os.getcwd()
        self.fonts = ["./resource/font/NanumSquare_acEB.ttf",
                      "./resource/font/NanumSquare_acB.ttf",
                      "./resource/font/LABDISITAL.ttf"]
        self.bells = [dirs+"/resource/sound/bell1.mp3",
                      dirs+"/resource/sound/bell2.mp3",
                      dirs+"/resource/sound/bell3.mp3"]
        self.texts = ['current_date','current_time',
                      'study_time','break_time',
                      'meal_time']
        self.uiUpdate()
        self.uiSetup()

    def uiUpdate(self):
        path = glob.glob('./resource/style/*.ui')
        for ui_path in path:
            ui_ = open(ui_path, 'r', encoding='utf-8')
            lines_ = ui_.readlines()
            ui_.close()
            for ii, i in enumerate(lines_):
                if 'include location' in i:
                    lines_[ii] = i.replace('.qrc', '.py')
                if '<pointsize>-1</pointsize>' in i:
                    lines_[ii] = ''
            ui_ = open(ui_path, 'w', encoding='utf-8')
            [ui_.write(i) for i in lines_]
            ui_.close()

    def uiSetup(self):
        FROM_CLASS = uic.loadUiType("./resource/style/main.ui")[0]
        WIDGET_CLASS = uic.loadUiType("./resource/style/timer.ui")[0]
        UPDATE_CLASS = uic.loadUiType("./resource/style/version.ui")[0]
        RANKING_CLASS = uic.loadUiType("./resource/style/ranking.ui")[0]
        TABLE_CLASS = uic.loadUiType("./resource/style/table.ui")[0]
        self.CLASS = [FROM_CLASS,WIDGET_CLASS,UPDATE_CLASS,RANKING_CLASS,TABLE_CLASS]
