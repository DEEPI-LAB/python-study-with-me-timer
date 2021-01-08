# -*- coding: utf-8 -*-

import glob

from PyQt5 import uic

class Utils():

    text = ['current_date',
            'current_time',
            'study_time',
            'break_time',
            'meal_time']

    def uiUpdate():
        path = glob.glob('./resource/*.ui')
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

    def uiSetup():
        FROM_CLASS = uic.loadUiType("./resource/main.ui")[0]
        WIDGET_CLASS = uic.loadUiType("./resource/timer.ui")[0]
        UPDATE_CLASS = uic.loadUiType("./resource/version.ui")[0]
        CLASS = [FROM_CLASS,WIDGET_CLASS,UPDATE_CLASS]
        return CLASS
        
        
        
        