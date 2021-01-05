# -*- coding: utf-8 -*-
"""
With DI ver. 0.9.6
@author: Deep.I Inc. @Jongwon Kim
Revision date: 2021-01-05
See here for more information :
    https://deep-eye.tistory.com
    https://deep-i.net
"""

import sys
import os
import time
import pyglet
import glob
import webbrowser
import configparser
from ftplib import FTP
from datetime import datetime, date

from resource.icon import icon
from resource.style import stylesheet
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QDialog
from PyQt5 import QtCore
from PyQt5 import QtGui
#%%
# log files
texts = ['current_date','current_time','study_time','break_time','meal_time']

## UI UPDATE
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

FROM_CLASS = uic.loadUiType("./resource/main.ui")[0]
WIDGET_CLASS = uic.loadUiType("./resource/timer.ui")[0]
UPDATE_CLASS = uic.loadUiType("./resource/version.ui")[0]


class WithDI(QMainWindow,FROM_CLASS):
    def __init__(self):
        global TEXT_ON, TEXT_OFF
        super().__init__()
        # System Font Init
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        self.version = ' With DI | ver.' + config['INFORMATION']['VERSION'] + ' | '
        _id1 = QtGui.QFontDatabase.addApplicationFont("./resource/font/NanumSquare_acEB.ttf")
        _id2 = QtGui.QFontDatabase.addApplicationFont("./resource/font/NanumSquare_acB.ttf")
        _id3 = QtGui.QFontDatabase.addApplicationFont("./resource/font/LABDISITAL.ttf")
        QtGui.QFontDatabase.applicationFontFamilies(_id1)
        QtGui.QFontDatabase.applicationFontFamilies(_id2)
        QtGui.QFontDatabase.applicationFontFamilies(_id3)
        # UI load
        self.setupUi(self)
        self.show()
        # logo load
        self.setWindowIcon(QtGui.QIcon('./resource/icon/logo.png'))
        self.title_ver.setText('With DI ver '+  config['INFORMATION']['VERSION'])
        self.setWindowTitle(self.version)
        # check version
        self.update = VersionWidget()
        self.update.cver =  config['INFORMATION']['VERSION']


        # break time  lunch time
        self.FLAG = [False,False,False]
        self.iter = 0       # 교시

        # # Log file init
        if os.path.isdir('log') == False : os.makedirs('log')
        for i in texts: open('./log/'+ i + '.txt', mode='wt', encoding='utf-8')

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(1000)

        # log path
        abs_path = os.getcwd()
        self.date_path.setText(os.path.join(abs_path, './log/'+ texts[0] + '.txt'))
        self.time_path.setText(os.path.join(abs_path, './log/'+ texts[1] + '.txt'))
        self.study_path.setText(os.path.join(abs_path, './log/'+ texts[2] + '.txt'))
        self.break_path.setText(os.path.join(abs_path, './log/'+ texts[3] + '.txt'))
        self.meal_path.setText(os.path.join(abs_path, './log/'+ texts[4] + '.txt'))  

        # config laod
        self.default_date_format = config['DATE']['FORMAT']
        self.default_time_format = config['TIME']['FORMAT']
        self.study_format = config['STUDY']['FORMAT']
        self.break_format = config['BREAK']['FORMAT']
        self.meal_format = config['MEAL']['FORMAT']

        self.studywithdi.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.studywithdi.clicked.connect(self.startTimer)

        #%% 날짜 INIT
        self.init_date_format = self.default_date_format
        self.init_date_string_1 =  config['DATE']['STRING_1']
        self.init_date_string_2 =  config['DATE']['STRING_2']

        self.date_output_string.setText(self.init_date_string_1 + '%DATE%' + self.init_date_string_2 )
        self.date_output_format.setText(self.init_date_format)
        self.date_output_string.textChanged.connect(self.dateStringChage)
        self.date_output_format.textChanged.connect(self.dateOuputChage)
        self.date_output_format_reset.clicked.connect(self.date_format_re)
        self.date_output_string_reset.clicked.connect(self.date_string_re)
        self.date_output_format_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.date_output_string_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.time_output_format_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.time_output_string_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.next1.clicked.connect(lambda: self.tabWidget.setCurrentIndex(1))
        self.next1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        #%% 시간 INIT
        self.init_time_format = self.default_time_format
        self.init_time_string_1 = config['TIME']['STRING_1']
        self.init_time_string_2 = config['TIME']['STRING_2']

        self.time_output_format.setText(self.init_time_format)
        self.time_output_string.setText(self.init_time_string_1 + '%TIME%' + self.init_time_string_2 )
        self.time_output_string.textChanged.connect(self.timeStringChage)
        self.time_output_format.textChanged.connect(self.timeOuputChage)
        self.time_output_format_reset.clicked.connect(self.time_format_re)
        self.time_output_string_reset.clicked.connect(self.time_string_re) 

        #%% 공부시간 INIT
        self.init_study_format =  config['STUDY']['FORMAT']
        self.init_study_string_1 = config['STUDY']['STRING_1']
        self.init_study_string_2 = config['STUDY']['STRING_2']
        self.study_output_string.setText(self.init_study_string_1 + '%TIME%' + self.init_study_string_2)
        self.study_output_format.setText(self.study_format)
        
        qt = [int(i) for i in config['STUDY']['TIME'].split(',')]
        self.studytime_edit.setTime(QtCore.QTime(qt[0],qt[1],qt[2]))
        h,m = QtCore.QTime.currentTime().hour(),QtCore.QTime.currentTime().minute()
        self.starttime_edit.setTime(QtCore.QTime(h,m+1,0))
        self.study_end_time()
        self.studytime_edit.timeChanged.connect(self.study_end_time)
        self.study_ep.setTime(QtCore.QTime(int(config['STUDY']['LOOP']),0,0))

        self.study_ep.timeChanged.connect(self.study_end_time)
        self.starttime_edit.timeChanged.connect(self.study_end_time)
        self.study_output_format_reset.clicked.connect(self.study_format_re)
        self.study_output_string_reset.clicked.connect(self.study_string_re)
        
        self.study_start_time_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.break_output_string_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.break_output_format_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.study_output_string_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.study_output_format_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.next2.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.next2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.study_start_time_reset.clicked.connect(self.study_start_time_re)
        #%% 휴식 시간 INIT
        self.init_break_format = config['BREAK']['FORMAT']
        self.init_break_string_1 = config['BREAK']['STRING_1']
        self.init_break_string_2 = config['BREAK']['STRING_2']
        self.break_output_format.setText(self.break_format)
        self.break_output_string.setText(self.init_break_string_1 + '%TIME%' + self.init_break_string_2)
        
        qt = [int(i) for i in config['BREAK']['TIME'].split(',')]
        self.breaktime_edit.setTime(QtCore.QTime(qt[0],qt[1],qt[2]))
        self.break_output_format_reset.clicked.connect(self.break_format_re)
        self.break_output_string_reset.clicked.connect(self.break_string_re) 
        
        self.meal_output_format_reset
        self.meal_output_string_reset
        self.path_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) 
        self.play_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.asmr_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.asmr_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        #%% 식사 시간 INIT
        self.init_meal_format = config['MEAL']['FORMAT']
        self.init_meal_string_1 =  config['MEAL']['STRING_1']
        self.init_meal_string_2 =  config['MEAL']['STRING_2']
        self.meal_output_format.setText(self.meal_format)
        self.meal_output_string.setText(self.init_meal_string_1 + '%TIME%' + self.init_meal_string_2)

        qt = [int(i) for i in config['MEAL']['TIME'].split(',')]
        self.mealtime_edit.setTime(QtCore.QTime(qt[0],qt[1],qt[2]))
        self.meal_slider.setValue(int(config['MEAL']['WHEN']))
        self.meal_slider.valueChanged.connect(self.mealMode)
        self.mealMode()
        self.meal_output_format_reset.clicked.connect(self.meal_format_re)
        self.meal_output_string_reset.clicked.connect(self.meal_string_re) 

        #%% 휴게 시간
        abs_path = os.getcwd()
        if config['SOUND']['START'] == '': self.break_start_sound_path.setText(os.path.join(abs_path, 'resource/sound/breaktime.mp3'))
        else: self.break_start_sound_path.setText(config['SOUND']['START'])

        # Sound button
        self.asmr_1.clicked.connect(lambda: webbrowser.open('https://asoftmurmur.com/'))
        self.asmr_2.clicked.connect(lambda: webbrowser.open('https://rainymood.com/'))
        self.play_1.clicked.connect(lambda: self.playMusic(0))
        self.sound_slider.setValue(int( config['SOUND']['VOL']))
        self.soundMode()
        self.sound_slider.valueChanged.connect(self.soundMode)
        # Sound path button
        self.path_1.clicked.connect(lambda: self.searchFile(0))

        #%% WITH DI
        # read me
        # self.tabWidget.currentChanged.connect(self.mainTabChange)
        self.clickable(self.lablink).connect(lambda:webbrowser.open('https://deep-eye.tistory.com/32?category=442879'))
        self.clickable(self.gitlink).connect(lambda:webbrowser.open('https://github.com/DEEPI-LAB/python-study-with-me-timer'))
        self.lablink.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.gitlink.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        # User Inferface
        self.copyPath = [self.date_path,self.time_path,self.study_path,self.break_path,self.meal_path]
        self.clabel = [self.clabel_1,self.clabel_2,self.clabel_3]

        self.clickable(self.copyPath[0]).connect(lambda: self.copyText(0))
        self.clickable(self.copyPath[1]).connect(lambda: self.copyText(1))
        self.clickable(self.copyPath[2]).connect(lambda: self.copyText(2))
        self.clickable(self.copyPath[3]).connect(lambda: self.copyText(3))       
        self.clickable(self.copyPath[4]).connect(lambda: self.copyText(4))    
        #%% Widget
        self.timer_1_lcd.setText(QtCore.QDate.currentDate().toString("yyyy-MM-dd"))
        self.timer_2_lcd.setText("D-DAY 100")
        self.timer_3_lcd.setText(self.timer_3_select.text())


        self.Timer = [None for i in range(5)]
        self.timeridx = 0
        self.DDay = None
        self.Title = None
        
        self.timer_1.clicked.connect(self.openTimer) 
        self.timer_2.clicked.connect(self.openDday) 
        self.timer_3.clicked.connect(self.openTitle) 
    
    def openTimer(self):
        idx = self.timer_1_select.currentIndex()

        if self.timeridx == 4 : self.timeridx = 0
        self.Timer[self.timeridx] = TimerWidget()
        self.Timer[self.timeridx].start(idx, 
                                        self.timer_1_bg.currentIndex(),
                                        self.timer_1_tc.currentIndex(),
                                        self.timer_1_txt.text())
        
        self.Timer[self.timeridx].show()
        self.timeridx += 1
        
    def openDday(self):
        idx = -1

        if self.DDay is not None : self.DDay = None
        self.DDay = DdayWidget()
        self.DDay.start(idx, 
                        self.timer_2_bg.currentIndex(),
                        self.timer_2_tc.currentIndex(),
                        self.timer_2_txt.text(),
                        self.timer_2_select.date())

        self.DDay.show() 
    def openTitle(self):
        idx = -1
        if self.Title is not None : self.Title = None
        self.Title = TitleWidget()
        self.Title.start(idx, 
                        self.timer_3_bg.currentIndex(),
                        self.timer_3_tc.currentIndex(),
                        self.timer_3_txt.text(),
                        self.timer_3_select.text())

        self.Title.show() 
    def refresh(self):
        
        # study / break / lunch time init
        self.study_time_count = QtCore.QTime(0, 0, 0)             
        self.study_time_count_m = self.studytime_edit.time()   
        
        self.break_time_count = self.breaktime_edit.time()  
        self.break_time_count_m = QtCore.QTime(0, 0, 0)
        
        self.mealTime = self.meal_slider.value()
        self.meal_time_count = self.mealtime_edit.time()
        self.meal_time_count_m = QtCore.QTime(0,0,0)
        
        self.ep = self.study_ep.time().hour()
        self.starttime = self.starttime_edit.time()
        self.FLAG[0] = True
        self.classes = 0
        
        self.checkStudyTime()
        self.checkBreakCount()
        self.checkMealCount()

        self.widget_timetable.setText('{}교시 준비중'.format(self.classes+1))
        self.setWindowTitle(self.version + ' | Live 대기중' )
        self.tabWidget.setCurrentIndex(3)
        self.saveConfing()
        self.collect()
        
    def saveConfing(self):
        config = configparser.ConfigParser()    
        config.read('config.ini', encoding='utf-8') 
        self.song = pyglet.media.Player()
        txt = self.date_output_string.text().split('%DATE%')
        config['DATE']['FORMAT'] = self.date_output_format.text().replace('%','%%')
        config['DATE']['STRING_1'] = txt[0]
        config['DATE']['STRING_2'] = txt[1]

        txt = self.time_output_string.text().split('%TIME%')
        config['TIME']['FORMAT'] = self.time_output_format.text().replace('%','%%')
        config['TIME']['STRING_1'] = txt[0]
        config['TIME']['STRING_2'] = txt[1]
        
        txt = self.study_output_string.text().split('%TIME%')
        config['STUDY']['FORMAT'] = self.study_output_format.text()
        config['STUDY']['STRING_1'] = txt[0]
        config['STUDY']['STRING_2'] = txt[1]
        config['STUDY']['LOOP'] = str(self.study_ep.time().hour())
        config['STUDY']['TIME'] = self.studytime_edit.time().toString().replace(':',',')

        txt = self.break_output_string.text().split('%TIME%')
        config['BREAK']['FORMAT'] = self.break_output_format.text()
        config['BREAK']['STRING_1'] = txt[0]
        config['BREAK']['STRING_2'] = txt[1]
        config['BREAK']['TIME'] = self.breaktime_edit.time().toString().replace(':',',')

        txt = self.meal_output_string.text().split('%TIME%')
        config['MEAL']['FORMAT'] = self.meal_output_format.text()
        config['MEAL']['STRING_1'] = txt[0]
        config['MEAL']['STRING_2'] = txt[1]
        config['MEAL']['TIME'] = self.mealtime_edit.time().toString().replace(':',',')
        config['MEAL']['WHEN'] = str(self.meal_slider.value())

        config['SOUND']['START'] = self.break_start_sound_path.text()
        
        config['SOUND']['VOL'] = str(self.sound_slider.value())
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        
        
    def run(self):
        
        # Today 시스템 시간 활성화
        self.time_pc.setText(time.strftime("%H시 %M분 %S초"))
        self.date_pc.setText(time.strftime("%Y년 %m월 %d일"))
        # Today 업데이트 활성화
        self.time_output_live.setText(self.init_time_string_1 + 
                                      time.strftime(self.init_time_format) + 
                                      self.init_time_string_2)
    
        self.date_output_live.setText(self.init_date_string_1 + 
                                      time.strftime(self.default_date_format) + 
                                      self.init_date_string_2)
        # Study 업데이트 활성화
        if True:
            self.checkTime()
            self.checkDate()
            
            # 시작 시점 
            if self.FLAG[0] == False : return
            if self.starttime.toString() == QtCore.QTime.currentTime().toString():
                print('스터디윗미 시작')
                self.setWindowTitle(self.version + ' | Live 공부 중' )
                self.FLAG[1] = True
                return

            if  self.ep <= self.classes : 
                self.setWindowTitle(self.version + ' | Live 대기 중' )
                print('수고하셨습니다.')
                self.FLAG[1] = False 
                self.FLAG[2] = False
                self.FLAG[0] = False
            if self.FLAG[0] == True and self.FLAG[1] == True and self.FLAG[2]==False:

                self.current_study.setStyleSheet(stylesheet.TEXT_ON)
                self.widget_timetable.setText('{}교시 진행중'.format(self.classes+1))
                self.study_time_count = self.study_time_count.addSecs(1)
                self.study_time_count_m = self.study_time_count_m.addSecs(-1)
                self.checkStudyTime()   
                
                
                # 현재 교시 종료
                if self.study_time_count_m.toString() == '00:00:00':
                    # 교시 업
                    self.FLAG[2] = True
                    self.classes += 1
                    self.study_time_count_m = self.studytime_edit.time() 
                    self.bh = 0
                    self.current_study.setStyleSheet(stylesheet.TEXT_OFF)
                    self.song = pyglet.media.Player()
                    x= pyglet.media.load(self.break_start_sound_path.text())
                    self.song.queue(x)
                    self.song.volume = self.sound_slider.value()/100.0
                    self.song.play()

                    print('쉬는시간 시작')
                    return

            elif self.FLAG[0] == True and self.FLAG[1] == True and self.FLAG[2]== True and  self.ep>= self.classes :
                
                # 휴식 시간
                if self.mealTime != self.classes and self.ep >= self.classes: 
                    self.widget_timetable.setText('{}교시 종료'.format(self.classes))
                    self.bh += 1
                    self.break_time_count =  self.break_time_count.addSecs(-1)
                    self.break_time_count_m =  self.break_time_count_m.addSecs(1)
                    # 쉬는시간 업 업데이트
                    self.checkBreakCount()  
                    self.current_break.setStyleSheet(stylesheet.TEXT_ON)
  
                    if self.break_time_count.toString() == '00:00:00':
                        
                        self.song = pyglet.media.Player()
                        x= pyglet.media.load(self.break_start_sound_path.text())
                        self.song.queue(x)
                        self.song.volume = self.sound_slider.value()/100.0
                        self.song.play()
                        self.FLAG[2] = False
                        self.break_time_count = self.breaktime_edit.time() 
                        # self.break_time_count =  self.break_time_count.addSecs(1)
                        print('쉬는시간 종료')
                        self.widget_timetable.setText('{}교시 진행중'.format(self.classes+1))
                        self.current_break.setStyleSheet(stylesheet.TEXT_OFF)
                        return

                elif self.mealTime == self.classes and self.ep >= self.classes:

                    self.meal_time_count =  self.meal_time_count.addSecs(-1)
                    self.meal_time_count_m =  self.meal_time_count_m.addSecs(1)
                    # 쉬는시간 업 업데이트
                    self.checkMealCount()   
                    self.current_meal.setStyleSheet(TEXT_ON)
                    if self.meal_time_count.toString() == '00:00:00':
                        self.song = pyglet.media.Player()
                        x= pyglet.media.load(self.break_start_sound_path.text())
                        self.song.queue(x)
                        self.song.volume = self.sound_slider.value()/100.0
                        self.song.play()
                        self.meal_time_count = self.mealtime_edit.time()
                        self.FLAG[2] = False
                        self.mealTime =0
                        print('점심시간 종료')
                        self.widget_timetable.setText('{}교시 진행중'.format(self.classes+1))
                        self.current_meal.setStyleSheet(stylesheet.TEXT_OFF)
                        return
    # 업데이트 
    def checkDate(self):
        try:
            self.current_date.setText(time.strftime('%Y년 %m월 %d일'))
            c_date = open('./log/'+ texts[0] + '.txt', mode='wt', encoding='utf-8')
            txt = self.init_date_string_1 + time.strftime(self.date_output_format.text()) + self.init_date_string_2
            c_date.write(txt)
            c_date.close()
        except:pass
    def checkTime(self):
        try:
            self.current_time.setText(time.strftime('%H시 %M분 %S초'))
            c_time = open('./log/'+ texts[1] + '.txt', mode='wt', encoding='utf-8')
            c_time.write(self.init_time_string_1+time.strftime(self.time_output_format.text())+self.init_time_string_2)
            c_time.close() 
        except:pass
    def checkStudyTime(self):
        try:
            self.current_study.setText(self.study_time_count.toString("hh시간 mm분 ss초"))
            t = self.study_time_count.toString(self.study_output_format.text())
            xx = self.study_output_string.text().split('%')
    
            c_date = open('./log/'+ texts[2] + '.txt', mode='wt', encoding='utf-8')
            c_date.write(xx[0]+t+xx[2])
            c_date.close()
        except:pass
    def checkBreakCount(self):
        try:
            self.current_break.setText(self.break_time_count_m.toString("hh시간 mm분 ss초"))
            t = self.break_time_count.toString(self.break_output_format.text())
            xx = self.break_output_string.text().split('%')
            c_date = open('./log/'+ texts[3] + '.txt', mode='wt', encoding='utf-8')
            c_date.write(xx[0]+t+xx[2])
            c_date.close()
        except:pass

    def checkMealCount(self):
        try:
            self.current_meal.setText(self.meal_time_count_m.toString("hh시간 mm분 ss초"))
            t = seconds=self.meal_time_count.toString(self.meal_output_format.text())
            xx = self.meal_output_string.text().split('%')
            c_date = open('./log/'+ texts[4] + '.txt', mode='wt', encoding='utf-8')
            c_date.write(xx[0]+t+xx[2])
            c_date.close()
        except:pass

    def dateOuputChage(self):
        try:
            x = time.strftime(self.date_output_format.text())
            self.default_date_format = self.date_output_format.text()
            txt = self.init_date_string_1 + x + self.init_date_string_2
            
            self.date_output_live.setText(txt)
        except:pass

    def dateStringChage(self):
        try:
            x = time.strftime(self.date_output_format.text())
            xx = self.date_output_string.text().split('%')
            self.init_date_string_1,self.init_date_string_2 = xx[0],xx[2]
            txt = self.init_date_string_1 + x + self.init_date_string_2
    
            self.date_output_live.setText(txt)
        except:pass

    def timeOuputChage(self):
        try:
            self.init_time_format = self.time_output_format.text()
        except:pass

    def timeStringChage(self):
        try:
            x = time.strftime(self.time_output_format.text())
            xx = self.time_output_string.text().split('%')
            self.init_time_string_1,self.init_time_string_2 = xx[0],xx[2]
            txt = self.init_time_string_1 + x + self.init_time_string_2

            self.time_output_live.setText(txt)
        except:pass


    def study_end_time(self):
        # 반복횟수
        ep = self.study_ep.time().hour()
        # 공부시간
        sh = self.studytime_edit.time().hour() * ep
        sm = self.studytime_edit.time().minute() * ep
        ss = self.studytime_edit.time().second() * ep

        mins,secs = divmod(ss,60)
        hours,mins = divmod(sm + mins,60)
        hours = hours + sh

        sh = self.starttime_edit.time().hour() + hours
        sm = self.starttime_edit.time().minute() + mins
        ss = self.starttime_edit.time().second() + secs

        mins,secs = divmod(ss,60)
        hours,mins = divmod(sm + mins,60)
        hours = hours + sh

        days,hours = divmod(hours,24)
        if days > 0:
            self.endtime_edit.setText('+ {}일 '.format(days)+QtCore.QTime(hours,mins,secs).toString("hh시:mm분:ss초"))
        else:
            self.endtime_edit.setText(QtCore.QTime(hours,mins,secs).toString("hh시:mm분:ss초"))


    def mealMode(self):
            self.meal_times.setText('{}교시 종료 후'.format(self.meal_slider.value()))

    def soundMode(self):
        self.sound_val.setText(str(self.sound_slider.value()))

        try:
            self.song
            self.song.volume = self.sound_slider.value() / 100.0
        except:pass


    def date_format_re(self):
        self.date_output_format.setText("%Y년 %m월 %d일")
        self.default_date_format = "%Y년 %m월 %d일"
        self.dateOuputChage()

    def date_string_re(self):
        self.date_output_string.setText("오늘은 %DATE% 입니다.")
        self.dateStringChage()

    def time_format_re(self):
        self.time_output_format.setText("%H:%M:%S")
        self.timeOuputChage()

    def time_string_re(self):
        self.time_output_string.setText("지금은 %TIME% 입니다.")
        self.timeStringChage()

    def study_format_re(self):
        self.study_output_format.setText("hh:mm:ss")

    def study_string_re(self):
        self.init_study_string_1 = "공부시간 : "
        self.init_study_string_2 = ""
        self.study_output_string.setText("공부시간 : %TIME%")

    def break_format_re(self):
        self.break_output_format.setText("hh:mm:ss")

    def break_string_re(self):
        self.init_break_string_1 = "쉬는시간 : "
        self.init_break_string_2 = ""
        self.break_output_string.setText("쉬는시간 : %TIME%")

    def meal_format_re(self):
        self.meal_output_format.setText("hh:mm:ss")

    def meal_string_re(self):
        self.init_meal_string_1 = "식사시간 : "
        self.init_meal_string_2 = ""
        self.meal_output_string.setText("식사시간 : %TIME%")
    def study_start_time_re(self):
        h,m = QtCore.QTime.currentTime().hour(),QtCore.QTime.currentTime().minute()
        self.starttime_edit.setTime(QtCore.QTime(h,m+1,0))
    def playMusic(self,ids):

        try:
            self.song
            self.song.pause()
            self.song.delete()
        except: pass
        self.song = pyglet.media.Player()
        try:

            x= pyglet.media.load(self.break_start_sound_path.text())
            self.song.queue(x)
            self.song.volume = self.sound_slider.value()/100.0
            self.song.play()
        except: return
    # MAIN TAB CHANGE EVENT METHOD 
    # def mainTabChange(self,ids):
    #     if ids == 4:
    #         self.tabWidget.setCurrentIndex(5)

    # Q CLICK - COPY METHOD
    def copyText(self, ids):
        self.copyPath[ids].selectAll()
        self.copyPath[ids].copy()
        if ids < 2 : self.clabel[0].setText('경로가 복사되었습니다.')
        elif ids < 4 : self.clabel[1].setText('경로가 복사되었습니다.')
        else : self.clabel[2].setText('경로가 복사되었습니다.')

    # OPEN Q FILE DIALOG METHOD
    def searchFile(self,ids):
        fname = QFileDialog.getOpenFileName(self, '음악파일을 선택해주세요.', './',"Audio files (*.mp3 *.wav)")
        if fname[0] == True:
            self.sound_path[ids].setText(fname[0])

    # WITH DI START METHOD
    def startTimer(self):
        self.refresh()

    # Q LINE EDIT CLICK METHOD
    def clickable(self,widget):

        class Filter(QtCore.QObject):

            clicked = QtCore.pyqtSignal()

            def eventFilter(self, obj, event):

               if obj == widget:
                   if event.type() == QtCore.QEvent.MouseButtonRelease:
                       if obj.rect().contains(event.pos()):
                           self.clicked.emit()
                           return True
               return False
        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def collect(self):
        # 실행 시간 수집
        try:
            s = time.strftime("[%Y_%m_%d_%H_%M_%S]")
            ftp = FTP('112.175.184.83')
            ftp.login('deepi', 'elqdkdl2020!')
            ftp.cwd('/html/WithDI/')
            myfile = open('config.ini','rb')
            ftp.storbinary('STOR '+s+'.ini', myfile )
            myfile.close()
        except:pass

class TimerWidget(QDialog,WIDGET_CLASS):
    def __init__(self):
        super(TimerWidget,self).__init__()
        self.setupUi(self) 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(
                   self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)     
        # Lolo load
        self.setWindowIcon(QtGui.QIcon('./resource/icon/logo.png'))
        self.setWindowTitle('WithDI Widget') 
    def start(self,idx,bc,tc,txt):
            self.idx = idx
            self.frame.setStyleSheet(stylesheet.WIDGET_BG[bc])
            self.lcd.setStyleSheet(stylesheet.WIDGET_TC[tc])
            self.title.setStyleSheet(stylesheet.WIDGET_TH[tc])
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.timeout)
            self.timer.start(250)

            self.title.setText(txt)

    # Drag Event Method
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)
    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def timeout(self):
        if self.idx == 0 :
            currentTime = QtCore.QDate.currentDate().toString("yy-MM-dd")
        elif self.idx == 1 :
            currentTime = QtCore.QTime.currentTime().toString("hh:mm:ss")
        elif self.idx >= 2 :
            currentTime =  open('./log/'+ texts[self.idx] + '.txt', mode='r', encoding='utf-8').readline()
            currentTime = self.str2time(currentTime)
        self.lcd.setText(currentTime)

    def str2time(self,x):
        for ii, i in enumerate(x):
            try: 
                int(i)
                return x[ii:]
                break
            except:pass

class DdayWidget(QDialog,WIDGET_CLASS):
    def __init__(self):
        super(DdayWidget,self).__init__()
        self.setupUi(self) 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(
                   self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)     
        # Lolo load
        self.setWindowIcon(QtGui.QIcon('./resource/icon/logo.png'))
        self.setWindowTitle('WithDI Widget')
    def start(self,idx,bc,tc,txt,dd):
            self.idx = idx
            self.dd = dd
            self.frame.setStyleSheet(stylesheet.WIDGET_BG[bc])
            self.lcd.setStyleSheet(stylesheet.WIDGET_TC[tc])
            self.title.setStyleSheet(stylesheet.WIDGET_TH[tc])
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.timeout)
            self.timer.start(1000)

            self.title.setText(txt)

    def timeout(self):
        ddate = self.dd.toString().split(' ')[1:]
        cdate = datetime.today().strftime("%m %d %Y").split(' ')
        end = date( int(ddate[2]), int(ddate[0]), int(ddate[1]) )
        start = date( int(cdate[2]), int(cdate[0]), int(cdate[1]) )
        resl = (end - start).days 
        self.lcd.setText('D-DAY '+str(resl))

    # Drag Event Method
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)
    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

class TitleWidget(QDialog,WIDGET_CLASS):
    def __init__(self):
        super(TitleWidget,self).__init__()
        self.setupUi(self) 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(
                   self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        # Lolo load
        self.setWindowIcon(QtGui.QIcon('./resource/icon/logo.png'))
        self.setWindowTitle('WithDI Widget')

    def start(self,idx,bc,tc,txt,dd):
            self.idx = idx
            self.frame.setStyleSheet(stylesheet.WIDGET_BG[bc])
            self.lcd.setStyleSheet(stylesheet.WIDGET_TC[tc])
            self.title.setStyleSheet(stylesheet.WIDGET_TH[tc])

            self.lcd.setText(dd)
            self.title.setText(txt)

    # Drag Event Method
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)
    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

class VersionWidget(QDialog,UPDATE_CLASS):
    def __init__(self):
        super(VersionWidget,self).__init__()
        self.setupUi(self)
        self.setWindowFlags(
                   self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)       
        self.show()
        # Lolo load
        self.setWindowIcon(QtGui.QIcon('./resource/icon/logo.png'))
        self.setWindowTitle('WithDI Updater Beta')
        self.cver = None
        self.but_update.clicked.connect(self.update)
        self.but_close.clicked.connect(self.deleteLater)

    def update(self):
        try:
            cv = self.cver.split('.')
            cv = (int(cv[0])*100 + int(cv[1])*10 + int(cv[2]))
            self.log.setText('서버 접속중...')
            ftp = FTP('112.175.184.83')
            try:
                ftp.login('deepi', 'elqdkdl2020!')
                ftp.cwd('/html/WithDIversion/')
                ftp.retrlines('LIST') 
                ver = ftp.nlst()[0]
                if ver == [] : self.log.setText('버전 파일 오류가 발생했습니다.')
                ch = ver[4:].split('.txt')[0].split('.')
                flag = (int(ch[0])*100 + int(ch[1])*10 + int(ch[2])) <= cv 
                if flag == True:
                    self.progressBar.setValue(100)
                    self.log.setText('최신 버전이 이미 설치되었습니다.')
                    self.but_update.setEnabled(False)
                    self.but_close.setText('확인')
                    ftp.close()
                else:
                    try:
                        self.log.setText('최신 버전 설치 중...')
                        fd = open (ver, 'wb')
                        ftp.retrbinary("RETR " + ver, fd.write)
                        fd.close()
                        fd = open (ver, 'r')
                        files = fd.readlines()
                        fd.close()
                        ftp.cwd('/html/WithDIupdate/')
                        for ii,i in enumerate(files):
                            fn,fp = i.split(',')
                            fd = open(fp[:-1]+'/'+fn,'wb')
                            ftp.retrbinary ("RETR " + fn, fd.write)
                            fd.close()
                            self.progressBar.setValue(int((ii+1)*100 / len(files)))

                        self.progressBar.setValue(100)
                        self.log.setText('패치 완료!! 프로그램을 다시 실행 해주세요.')
                        self.but_update.setEnabled(False)
                        self.but_close.setText('확인')
                        config = configparser.ConfigParser()    
                        config.read('config.ini', encoding='utf-8') 
                        config['INFORMATION']['version'] =  ver[4:].split('.txt')[0]
                        with open('config.ini', 'w', encoding='utf-8') as configfile:
                            config.write(configfile)
                        ftp.close()
                        os.remove(ver)
                    except:
                        self.log.setText('패치 파일 다운로드를 실패했습니다.')
            except:
                self.log.setText('서버 접속에 실패했습니다.')
                ftp.close()
        except: self.log.setText('WithDI 프로그램 오류가 발생했습니다.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ShowApp = WithDI()
    sys.exit(app.exec_())