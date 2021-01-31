# -*- coding: utf-8 -*-
"""
With DI ver. 1.0.1
@author: Deep.I Inc. @Jongwon Kim
Revision date: 2021-01-26
See here for more information :
    https://deep-eye.tistory.com
    https://deep-i.net
"""

import sys
import os
import time
import pyglet
import webbrowser
import configparser
import shutil
from ftplib import FTP
from datetime import datetime, date
from core import withDI
from core.Utils import Utils
from resource.icon import icon
from resource.style import stylesheet
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QTableWidgetItem
from PyQt5 import QtCore,QtWidgets
from PyQt5 import QtGui

# sys init
utils = Utils()

class WithDI(QMainWindow,utils.CLASS[0]):
    def __init__(self):
        global TEXT_ON, TEXT_OFF
        super().__init__()
        
        # CONFIG 파일 불러오기
        if os.path.exists('config.ini') == False: self.configRefresh()
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        self.version = ' With DI | ver.' + config['INFORMATION']['VERSION'] + ' | '
        # 폰트 불러오기
        _ids = [QtGui.QFontDatabase.addApplicationFont(utils.fonts[i]) for i in range(3)]
        [QtGui.QFontDatabase.applicationFontFamilies(_ids[i]) for i in range(3)]
        # UI 불러오기
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./resource/icon/logo.png'))
        self.title_ver.setText('With DI ver '+  config['INFORMATION']['VERSION'])
        self.setWindowTitle(self.version)
        # Update 확인 위젯 불러오기
        if config['USER']['VERCHECK'] =='1':
            self.updates = VersionWidget(self)
            self.updates.cver =  config['INFORMATION']['VERSION']
        self.vercheck = False
        self.nickname = config['USER']['NICKNAME']
        self.totaltime = config['USER']['TOTAL']
        self.addtime = '00:00:00'
        # break time  lunch time
        self.FLAG = [False,False,False]
        self.TRIGER = False
        self.addFLAG = False
        self.iter = 0
        # Log init
        if os.path.isdir('log') == False : os.makedirs('log')
        for i in utils.texts: open('./log/'+ i + '.txt', mode='wt', encoding='utf-8')
        try: os.remove('path.exe')
        except:pass

        # log path
        apath = os.getcwd()
        self.date_path.setText(os.path.join(apath, './log/'+ utils.texts[0] + '.txt'))
        self.time_path.setText(os.path.join(apath, './log/'+ utils.texts[1] + '.txt'))
        self.study_path.setText(os.path.join(apath, './log/'+ utils.texts[2] + '.txt'))
        self.break_path.setText(os.path.join(apath, './log/'+ utils.texts[3] + '.txt'))
        self.meal_path.setText(os.path.join(apath, './log/'+ utils.texts[4] + '.txt'))  

        # config laod
        self.default_date_format = config['DATE']['FORMAT']
        self.default_time_format = config['TIME']['FORMAT']
        self.study_format = config['STUDY']['FORMAT']
        self.break_format = config['BREAK']['FORMAT']
        self.meal_format = config['MEAL']['FORMAT']

        self.studywithdi.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.studyfinish.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
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

        self.time_pc.setText(time.strftime("%H시 %M분 %S초"))
        self.date_pc.setText(time.strftime("%Y년 %m월 %d일"))
        self.time_output_live.setText(self.init_time_string_1 + 
                                      time.strftime(self.init_time_format) + 
                                      self.init_time_string_2)

        self.date_output_live.setText(self.init_date_string_1 + 
                                      time.strftime(self.default_date_format) + 
                                      self.init_date_string_2)
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
        self.study_output_format_reset.clicked.connect(lambda: self.msFormatReset(0))
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
        self.play.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.asmr_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.asmr_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #%% 식사 시간 INIT
        self.init_meal_format = config['MEAL']['FORMAT']
        self.init_meal_string_1 =  config['MEAL']['STRING_1']
        self.init_meal_string_2 =  config['MEAL']['STRING_2']
        self.meal_output_format.setText(self.meal_format)
        self.meal_output_string.setText(self.init_meal_string_1 + '%TIME%' + self.init_meal_string_2)

        qt = [int(i) for i in config['MEAL']['TIME'].split(',')]
        self.meal_count = [self.m_1,self.m_2,self.m_3,self.m_4,
                           self.m_5,self.m_6,self.m_7,self.m_8,
                           self.m_9]
        self.meal_but = [0 for i in range(9)]
        self.meal_count[0].clicked.connect(lambda: self.mealCount(0))
        self.meal_count[1].clicked.connect(lambda: self.mealCount(1))
        self.meal_count[2].clicked.connect(lambda: self.mealCount(2))
        self.meal_count[3].clicked.connect(lambda: self.mealCount(3))
        self.meal_count[4].clicked.connect(lambda: self.mealCount(4))
        self.meal_count[5].clicked.connect(lambda: self.mealCount(5))
        self.meal_count[6].clicked.connect(lambda: self.mealCount(6))
        self.meal_count[7].clicked.connect(lambda: self.mealCount(7))
        self.meal_count[8].clicked.connect(lambda: self.mealCount(8))
        self.meal_count_reset.clicked.connect(self.mealReset)
        self.mealtime_edit.setTime(QtCore.QTime(qt[0],qt[1],qt[2]))

        self.meal_output_format_reset.clicked.connect(lambda: self.msFormatReset(0))
        self.meal_output_string_reset.clicked.connect(self.mstringReset) 
        self.meal_output_format_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.meal_output_string_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.meal_count_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        #%% 휴게 시간
        # Sound button
        self.asmr_1.clicked.connect(lambda: webbrowser.open('https://asoftmurmur.com/'))
        self.asmr_2.clicked.connect(lambda: webbrowser.open('https://rainymood.com/'))
        self.play.clicked.connect(self.playMusic)
        self.sound_slider.setValue(int(config['SOUND']['VOL']))
        self.soundMode()
        self.sound_slider.valueChanged.connect(self.soundMode)
        try:
            x= pyglet.media.load(utils.bells[self.bgm_box.currentIndex()])
            self.song.queue(x)
            self.song.volume = 0
            self.song.play()
        except:pass
        # Sound path button
        self.play.clicked.connect(self.playMusic)
        self.studyfinish.clicked.connect(self.stopStudy)
        #%% WITH DI
        self.clickable(self.lablink).connect(lambda:webbrowser.open('https://deep-eye.tistory.com/32?category=442879'))
        self.clickable(self.gitlink).connect(lambda:webbrowser.open('https://github.com/DEEPI-LAB/python-study-with-me-timer'))
        self.clickable(self.youlink).connect(lambda:webbrowser.open('https://www.youtube.com/channel/UCi18EeOdU26XvfKzcOMW3XA'))
        self.lablink.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.gitlink.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.youlink.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # User Inferface
        self.copyPath = [self.date_path,self.time_path,self.study_path,self.break_path,self.meal_path]
        self.clabel = [self.clabel_1,self.clabel_2,self.clabel_3]

        self.clickable(self.copyPath[0]).connect(lambda: self.copyText(0))
        self.clickable(self.copyPath[1]).connect(lambda: self.copyText(1))
        self.clickable(self.copyPath[2]).connect(lambda: self.copyText(2))
        self.clickable(self.copyPath[3]).connect(lambda: self.copyText(3))       
        self.clickable(self.copyPath[4]).connect(lambda: self.copyText(4)) 
        self.configrefresh.clicked.connect(self.configRefresh)
        #%% Widget
        self.timer_1_lcd.setText(QtCore.QDate.currentDate().toString("yyyy-MM-dd"))
        self.timer_2_lcd.setText("D-DAY 100")
        self.timer_3_lcd.setText(self.timer_3_select.text())

        self.Timer = [None for i in range(5)]
        self.timeridx = 0
        self.DDay = None
        self.Title = None
        self.Table = None

        self.timer_1.clicked.connect(self.openTimer) 
        self.timer_2.clicked.connect(self.openDday) 
        self.timer_3.clicked.connect(self.openTitle)
        self.timer_4.clicked.connect(self.openTable)
        
        # 반응형 위젯 #1
        self.timer_1_select.currentIndexChanged.connect(self.timer_1_changed)
        self.timer_1_bg.currentIndexChanged.connect(self.timer_1_changed)
        self.timer_1_tc.currentIndexChanged.connect(self.timer_1_changed)
        self.timer_1_txt.textChanged.connect(self.timer_1_changed)

        # 반응형 위젯 #2
        self.timer_2_bg.currentIndexChanged.connect(self.timer_2_changed)
        self.timer_2_tc.currentIndexChanged.connect(self.timer_2_changed)
        self.timer_2_txt.textChanged.connect(self.timer_2_changed)

        # 반응형 위젯 #1
        self.timer_3_select.textChanged.connect(self.timer_3_changed)
        self.timer_3_bg.currentIndexChanged.connect(self.timer_3_changed)
        self.timer_3_tc.currentIndexChanged.connect(self.timer_3_changed)
        self.timer_3_txt.textChanged.connect(self.timer_3_changed)        

        # 반응형 위젯 #1
        self.timer_4_select.textChanged.connect(self.timer_4_changed)
        self.timer_4_bg.currentIndexChanged.connect(self.timer_4_changed)
        self.timer_4_tc.currentIndexChanged.connect(self.timer_4_changed)

    #%% MEAL DEF
    def mealCount(self,idx):
        if sum(self.meal_but) >= 2: return
        if self.meal_but[idx] == 0:
            self.meal_count[idx].setStyleSheet(stylesheet.MEAL_BUT_ON)
            self.meal_but[idx] = 1
        else:
            self.meal_count[idx].setStyleSheet(stylesheet.MEAL_BUT_OFF)
            self.meal_but[idx] = 0
    def mealReset(self):
        for i in range(9):
            self.meal_count[i].setStyleSheet(stylesheet.MEAL_BUT_OFF)
            self.meal_but[i] = 0
    def mstringReset(self):
        self.init_meal_string_1 = "식사시간 : "
        self.init_meal_string_2 = ""
        self.meal_output_string.setText("식사시간 : %TIME%")
    def msFormatReset(self,idx):
        if idx == 1: self.meal_output_format.setText("hh:mm:ss")
        elif idx == 0: self.study_output_format.setText("hh:mm:ss")

    #%% BGM DEF
    def soundMode(self):
        self.sound_val.setText(str(self.sound_slider.value()))
        try:
            self.song
            self.song.volume = self.sound_slider.value() / 100.0
        except:pass
    def playMusic(self):
        try:
            self.song
            self.song.pause()
            self.song.delete()
        except:pass
        self.song = pyglet.media.Player()
        try:
                x= pyglet.media.load(utils.bells[self.bgm_box.currentIndex()])
                self.song.queue(x)
                self.song.volume = self.sound_slider.value() / 100.0
                self.song.play()
        except: pass

    #%% ABOUT
    def configRefresh(self):
        try:
            # os.remove('config.ini')
            shutil.copy('./resource/config.ini','config.ini')
            self.deleteLater()
            app.quit()
        except:pass
    # WITH DI START METHOD
    def startTimer(self):
        if self.FLAG[0] == True or self.TRIGER == True:
            reply = QMessageBox.question(self, 'WithDI', '타이머가 실행중입니다. 다시 시작하겠습니까?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.setWindowTitle(self.version + ' | Live 대기중' )
                self.state.setText('Live 대기중')  
                self.FLAG[1] = False
                self.FLAG[2] = False
                self.FLAG[0] = False
                self.current_study.setStyleSheet(stylesheet.TEXT_OFF)
                self.current_break.setStyleSheet(stylesheet.TEXT_OFF)
                self.current_meal.setStyleSheet(stylesheet.TEXT_OFF)
                if self.nickname =='' :
                    self.ranking = RankingWidget(self)
                else : 
                    self.refresh()
                    self.update()
            else: return
        else:
            if self.nickname =='' :
                self.ranking = RankingWidget(self)
            else : 
                self.refresh()
                self.update()

            

    def update(self):
        # try:
        s = time.strftime("[%Y_%m_%d_%H_%M_%S]")
        ftp = FTP(withDI.server_ip)
        ftp.login(withDI.user_id, withDI.user_pw)
        ftp.cwd('/html/WithDI/')
        myfile = open('config.ini','rb')
        ftp.storbinary('STOR '+s+'.ini', myfile )
        myfile.close()
        ftp.cwd('/html/RANKING/')
        fd = open('rank.ini','wb')
        ftp.retrbinary("RETR " + 'rank.ini', fd.write)
        fd.close()
        fd = open('rank.ini','r')
        rank = fd.readlines()
        fd.close()
        top = []
        for i in range(2):
            top.append('  - '.join(rank[-(i+1)].split(',')[1:]))
        for i in range(len(rank)):
            if rank[-i].split(',')[1] == self.nickname:
                ids = rank[-i].split(',')
                self.dirank.setText("{} 위  - {}".format(ids[0],ids[2]))
                break
            else: self.dirank.setText("{} 위".format(i))
        os.remove('rank.ini')
        self.top_1.setText(top[0])
        self.top_2.setText(top[1])

        # except:pass
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'WithDI', '프로그램을 종료하시겠습니까?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try : 
                self.updates.deleteLater()
            except:pass
            self.deleteLater()
            app.quit()
        else: event.ignore()

    def path(self):
        import subprocess
        self.deleteLater()
        subprocess.Popen("path.exe")
        app.quit()

    def stopStudy(self):
        
        if self.FLAG[1] == True and self.FLAG[0] == True:
            reply = QMessageBox.question(self, 'WithDI', '타이머를 일시정지하시겠습니까?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.setWindowTitle(self.version + ' | Live 일시정지' )
                self.state.setText('Live 일시정지')  
                self.FLAG[1] = False 
                self.FLAG[2] = False
                self.FLAG[0] = False
                self.TRIGER = True
                self.studyfinish.setText('타이머 다시 시작')
            else: return
        elif self.TRIGER == True:
            reply = QMessageBox.question(self, 'WithDI', '타이머를 다시 시작하겠습니까?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.setWindowTitle(self.version + ' | Live 공부중' )
                self.state.setText('Live 공부중')  
                self.FLAG[0] = True
                self.FLAG[1] = True
                self.FLAG[2] = False
                self.TRIGER = False
                self.studyfinish.setText('타이머 일시정지')
                # self.run()
        

    #%% Widget DEF
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
    def openTable(self):
        rowcount = self.study_ep.time().hour() 
        if self.Table is not None : self.Table = None
        self.Table = TableWidget()
        self.Table.initTable(rowcount,
                             self.starttime_edit.time(),
                             self.breaktime_edit.time(),
                             self.studytime_edit.time(),
                             self.mealtime_edit.time(),
                             self.meal_but)
        self.Table.cdate = int(self.date_pc.text().split('월')[1][:-1])
        self.Table.start(self.timer_4_bg.currentIndex(),
                self.timer_4_tc.currentIndex(),
                self.timer_4_select.text())

        self.Table.show()
        
    
    def timer_1_changed(self):
        
        self.timer_1_title.setText(self.timer_1_txt.text())
        self.timer_1_frame.setStyleSheet(stylesheet.WIDGET_BG_T[self.timer_1_bg.currentIndex()])
        self.timer_1_lcd.setStyleSheet(stylesheet.WIDGET_TC_T[self.timer_1_tc.currentIndex()])
        self.timer_1_title.setStyleSheet(stylesheet.WIDGET_TH_T[self.timer_1_tc.currentIndex()])
        
        idx = self.timer_1_select.currentIndex()
        if idx == 0: 
            self.timer_1_lcd.setText(time.strftime('%Y-%m-%d'))
        else : 
            self.timer_1_lcd.setText(time.strftime('%H:%M:%S'))
            
    def timer_2_changed(self):
        
        self.timer_2_title.setText(self.timer_2_txt.text())
        self.timer_2_frame.setStyleSheet(stylesheet.WIDGET_BG_T[self.timer_2_bg.currentIndex()])
        self.timer_2_lcd.setStyleSheet(stylesheet.WIDGET_TC_T[self.timer_2_tc.currentIndex()])
        self.timer_2_title.setStyleSheet(stylesheet.WIDGET_TH_T[self.timer_2_tc.currentIndex()])
    
    def timer_3_changed(self):
        
        self.timer_3_title.setText(self.timer_3_txt.text())
        self.timer_3_lcd.setText(self.timer_3_select.text())
        self.timer_3_frame.setStyleSheet(stylesheet.WIDGET_BG_T[self.timer_3_bg.currentIndex()])
        self.timer_3_lcd.setStyleSheet(stylesheet.WIDGET_TC_T[self.timer_3_tc.currentIndex()])
        self.timer_3_title.setStyleSheet(stylesheet.WIDGET_TH_T[self.timer_3_tc.currentIndex()])        
    
    def timer_4_changed(self):
        
        self.timer_4_title.setText(self.timer_4_select.text())
        self.timer_4_title.setStyleSheet(stylesheet.TABLE_TH_T[self.timer_4_tc.currentIndex()])
        self.timer_4_frame.setStyleSheet(stylesheet.WIDGET_BG_T[self.timer_4_bg.currentIndex()])
        self.timer_4_table.setStyleSheet(stylesheet.TABLE_TH_T[self.timer_4_tc.currentIndex()])     
    #%% WITH DI STARTING SETUP

    def refresh(self):
        # study / break / lunch time init
        self.study_time_count = QtCore.QTime(0, 0, 0)             
        self.study_time_count_m = self.studytime_edit.time()   
        self.addtimes = self.study_time_count_m.toString()
        self.break_time_count = self.breaktime_edit.time()  
        self.break_time_count_m = QtCore.QTime(0, 0, 0)
        self.mtimes = []
        for ii,i in enumerate(self.meal_but):
            if i == 1:self.mtimes.append(ii+1)
        self.meal_time_count = self.mealtime_edit.time()
        self.meal_time_count_m = QtCore.QTime(0,0,0)
        
        self.ep = self.study_ep.time().hour()
        self.starttime = self.starttime_edit.time()
        self.FLAG[0] = True
        self.classes = 0

        self.checkStudyTime()
        self.checkBreakCount()
        self.checkMealCount()

        self.state.setText('{}교시 준비중'.format(self.classes+1))
        self.studyfinish.setText('타이머 일시정지')
        self.setWindowTitle(self.version + ' | Live 대기중' )
        self.tabWidget.setCurrentIndex(3)
        self.saveConfing()
        self.nick.setText(self.nickname)
        self.addtime = "00:00:00"

        st = self.totaltime.split(':')
        self.totalt.setText(st[0]+"시간 " + st[1] + "분 " + st[2] + "초")

        self.ptime = time.time()
        self.ctime = self.ptime
        try:self.timer
        except:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.run)
            self.timer.start(1000)
        
    def saveConfing(self):
        config = configparser.ConfigParser()    
        config.read('config.ini', encoding='utf-8') 
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

        if self.vercheck == True : config['USER']['VERCHECK'] = '0'
        config['USER']['NICKNAME'] = self.nickname
        config['USER']['TOTAL'] = self.totaltime
        if self.FLAG[0] == True and self.FLAG[1] == True and self.addFLAG == True:
            config['USER']['CURRENT'] = self.addtimes
        else: config['USER']['CURRENT'] = "00:00:00"
        config['SOUND']['VOL'] = str(self.sound_slider.value())
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)

    def run(self):

        # Today 시스템 시간 활성화
        self.ptime = time.time()
        self.gt = round(self.ptime - self.ctime)
        self.ctime = self.ptime
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
                self.setWindowTitle(self.version + ' | Live 공부 중' )
                self.FLAG[1] = True
                return

            if  self.ep <= self.classes : 
                self.setWindowTitle(self.version + ' | Live 대기 중' )
                self.state.setText('스터디 종료! 수고하셨습니다.')
                self.FLAG[1] = False 
                self.FLAG[2] = False
                self.FLAG[0] = False

            if self.FLAG[0] == True and self.FLAG[1] == True and self.FLAG[2]==False:

                self.current_study.setStyleSheet(stylesheet.TEXT_ON)
                self.state.setText('{}교시 진행중'.format(self.classes+1))
                self.study_time_count = self.study_time_count.addSecs(self.gt)
                self.study_time_count_m = self.study_time_count_m.addSecs(-self.gt)
                self.checkStudyTime()

                # 현재 교시 종료
                if self.study_time_count_m.toString() == '00:00:00':
                    # 교시 업
                    self.FLAG[2] = True
                    self.classes += 1
                    self.study_time_count_m = self.studytime_edit.time() 
                    self.bh = 0
                    self.current_study.setStyleSheet(stylesheet.TEXT_OFF)
                    try:
                        self.song = pyglet.media.Player()
                        x= pyglet.media.load(utils.bells[self.bgm_box.currentIndex()])
                        self.song.queue(x)
                        self.song.volume = self.sound_slider.value()/100.0
                        self.song.play()
                    except:pass
                    self.addTotalTime()
                    k = self.totaltime.split(':')
                    s = k[0]+'시간'+k[1]+'분'+k[2]+'초'
                    self.totalt.setText(s)
                    return

            elif self.FLAG[0] == True and self.FLAG[1] == True and self.FLAG[2]== True and  self.ep>= self.classes :
                
                # 휴식 시간
                try:
                    self.mt = self.mtimes[0]
                except:self.mt = 0
                if self.mt != self.classes and self.ep >= self.classes: 
                    self.state.setText('{}교시 종료'.format(self.classes))
                    self.bh += 1
                    self.break_time_count =  self.break_time_count.addSecs(-self.gt)
                    self.break_time_count_m =  self.break_time_count_m.addSecs(self.gt)

                    # 쉬는시간 업데이트
                    self.checkBreakCount()  
                    self.current_break.setStyleSheet(stylesheet.TEXT_ON)

                    if self.break_time_count.toString() == '00:00:00':

                        try:
                            self.song = pyglet.media.Player()
                            x= pyglet.media.load(utils.bells[self.bgm_box.currentIndex()])
                            self.song.queue(x)
                            self.song.volume = self.sound_slider.value()/100.0
                            self.song.play()
                        except:pass
                        self.FLAG[2] = False
                        self.break_time_count = self.breaktime_edit.time() 
                        # self.break_time_count =  self.break_time_count.addSecs(1)
                        self.state.setText('{}교시 진행중'.format(self.classes+1))
                        self.current_break.setStyleSheet(stylesheet.TEXT_OFF)
                        return

                elif self.mt == self.classes and self.ep >= self.classes:
                    self.state.setText('{}교시 종료'.format(self.classes))
                    self.meal_time_count =  self.meal_time_count.addSecs(-self.gt)
                    self.meal_time_count_m =  self.meal_time_count_m.addSecs(self.gt)

                    # 식사시간 업데이트
                    self.checkMealCount()   
                    self.current_meal.setStyleSheet(stylesheet.TEXT_ON)
                    if self.meal_time_count.toString() == '00:00:00':
                        try:
                            self.song = pyglet.media.Player()
                            x= pyglet.media.load(utils.bells[self.bgm_box.currentIndex()])
                            self.song.queue(x)
                            self.song.volume = self.sound_slider.value()/100.0
                            self.song.play()
                        except:pass
                        self.meal_time_count = self.mealtime_edit.time()
                        self.FLAG[2] = False
                        self.state.setText('{}교시 진행중'.format(self.classes+1))
                        self.current_meal.setStyleSheet(stylesheet.TEXT_OFF)
                        del self.mtimes[0]
                        return
    # 업데이트 
    def checkDate(self):
        self.current_date.setText(time.strftime('%Y년 %m월 %d일'))
        try:
            c_date = open('./log/'+ utils.texts[0] + '.txt', mode='wt', encoding='utf-8')
            txt = self.init_date_string_1 + time.strftime(self.date_output_format.text()) + self.init_date_string_2
            c_date.write(txt)
            c_date.close()
        except:pass
    def checkTime(self):
        self.current_time.setText(time.strftime('%H시 %M분 %S초'))
        try:
            c_time = open('./log/'+ utils.texts[1] + '.txt', mode='wt', encoding='utf-8')
            c_time.write(self.init_time_string_1+time.strftime(self.time_output_format.text())+self.init_time_string_2)
            c_time.close() 
        except:pass
    def checkStudyTime(self):
        self.current_study.setText(self.study_time_count.toString("hh시간 mm분 ss초"))
        try:
            t = self.study_time_count.toString(self.study_output_format.text())
            xx = self.study_output_string.text().split('%')
    
            c_date = open('./log/'+ utils.texts[2] + '.txt', mode='wt', encoding='utf-8')
            c_date.write(xx[0]+t+xx[2])
            c_date.close()
        except:pass
    def checkBreakCount(self):
        self.current_break.setText(self.break_time_count_m.toString("hh시간 mm분 ss초"))
        try:
            t = self.break_time_count.toString(self.break_output_format.text())
            xx = self.break_output_string.text().split('%')
            c_date = open('./log/'+ utils.texts[3] + '.txt', mode='wt', encoding='utf-8')
            c_date.write(xx[0]+t+xx[2])
            c_date.close()
        except:pass
    def checkMealCount(self):
        self.current_meal.setText(self.meal_time_count_m.toString("hh시간 mm분 ss초"))
        try:
            t = seconds=self.meal_time_count.toString(self.meal_output_format.text())
            xx = self.meal_output_string.text().split('%')
            c_date = open('./log/'+ utils.texts[4] + '.txt', mode='wt', encoding='utf-8')
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
            self.endtime_edit.setText('+ {}일 '.format(days)+QtCore.QTime(hours,mins,secs).toString("hh시 mm분 ss초"))
        else:
            self.endtime_edit.setText(QtCore.QTime(hours,mins,secs).toString("hh시 mm분 ss초"))
    def addTotalTime(self):

        at = [int(i) for i in self.addtime.split(':')]
        pt = [int(i) for i in self.totaltime.split(':')]
        ct = [int(i) for i in self.study_time_count.toString("hh:mm:ss").split(':')]
        self.addtime = self.study_time_count.toString("hh:mm:ss")
        sh = pt[0]+ct[0]-at[0]
        sm = pt[1]+ct[1]-at[1]
        ss = pt[2]+ct[2]-at[2]

        mins,secs = divmod(ss,60)
        hours,mins = divmod(sm + mins,60)
        hours = hours + sh
        self.totaltime = "{}:{}:{}".format(hours,mins,secs)
        self.addFLAG = True
        self.saveConfing()
        self.update()
        self.addFLAG = False

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

    def study_start_time_re(self):
        h,m = QtCore.QTime.currentTime().hour(),QtCore.QTime.currentTime().minute()
        self.starttime_edit.setTime(QtCore.QTime(h,m+1,0))

    # Q CLICK - COPY METHOD
    def copyText(self, ids):
        self.copyPath[ids].selectAll()
        self.copyPath[ids].copy()
        if ids < 2 : self.clabel[0].setText('경로가 복사되었습니다.')
        elif ids < 4 : self.clabel[1].setText('경로가 복사되었습니다.')
        else : self.clabel[2].setText('경로가 복사되었습니다.')

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

class TimerWidget(QDialog,utils.CLASS[1]):
    def __init__(self):
        super(TimerWidget,self).__init__()
        self.setupUi(self) 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(
                   self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)     
        # Lolo load
        self.setWindowIcon(QtGui.QIcon('./resource/icon/logo.png'))
        self.setWindowTitle('WithDI') 
    def start(self,idx,bc,tc,txt):
            self.idx = idx
            self.frame.setStyleSheet(stylesheet.WIDGET_BG[bc])
            self.lcd.setStyleSheet(stylesheet.WIDGET_TC[tc])
            self.title.setStyleSheet(stylesheet.WIDGET_TH[tc])
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.timeout)
            self.timer.start(100)

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
            currentTime =  open('./log/'+ utils.texts[self.idx] + '.txt', mode='r', encoding='utf-8').readline()
            currentTime = self.str2time(currentTime)
        self.lcd.setText(currentTime)

    def str2time(self,x):
        for ii, i in enumerate(x):
            try: 
                int(i)
                return x[ii:]
                break
            except:pass

class DdayWidget(QDialog,utils.CLASS[1]):
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

class TitleWidget(QDialog,utils.CLASS[1]):
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

class TableWidget(QDialog,utils.CLASS[4]):
    def __init__(self):
        super(TableWidget,self).__init__()
        self.setupUi(self) 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(
                   self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        # Lolo load
        self.setWindowIcon(QtGui.QIcon('./resource/icon/logo.png'))
        self.setWindowTitle('WithDI Widget')
    def initTable(self,rowcount,starttime,breaktime,studytime,mealtime,mealcount):
        self.table.setRowCount(rowcount+mealcount.count(1))
        self.setFixedSize(450,110+(37*(rowcount+mealcount.count(1))))
        self.tablecount = rowcount+mealcount.count(1)
        k = 0
        for i in range(rowcount):
            t, mi = self.study_end_time(starttime,studytime)
            self.table.setItem(k,0, QTableWidgetItem(str(i+1)+'교시'))
            self.table.setItem(k,1, QTableWidgetItem(starttime.toString("hh:mm")))
            self.table.setItem(k,2, QTableWidgetItem('~'))
            self.table.setItem(k,3, QTableWidgetItem(t.toString("hh:mm")))
            self.table.setItem(k,4, QTableWidgetItem(str(mi)+'분'))
            starttime = t
            if i == (rowcount - 1) : break
            if mealcount[i] == 1:
                k = k + 1 
                t, mi = self.study_end_time(starttime,mealtime)
                self.table.setItem(k,0, QTableWidgetItem('식사 시간'))
                self.table.setItem(k,1, QTableWidgetItem(starttime.toString("hh:mm")))
                self.table.setItem(k,2, QTableWidgetItem('~'))
                self.table.setItem(k,3, QTableWidgetItem(t.toString("hh:mm")))
                self.table.setItem(k,4, QTableWidgetItem(str(mi)+'분'))
                starttime = t
            else:
                starttime, _ = self.study_end_time(starttime,breaktime)
            k = k + 1 
            
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0,  QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1,  QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2,  QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3,  QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4,  QtWidgets.QHeaderView.ResizeToContents)
        self.table.setItemDelegate( AlignDelegate(self.table))
        self.table.update()
        self.cdate = None
        # self.timer = QtCore.QTimer(self)
        # self.timer.timeout.connect(self.run)
        # self.timer.start(1000)
    # def run(self):
    #     if self.cdate is None : return
    #     ctime = datetime.now().hour,datetime.now().minute
    #     for i in range(self.tablecount):
    #         stime = [int(ii) for ii in self.table.item(i,1).text().split(':')]
    #         etime = [int(ii) for ii in self.table.item(i,3).text().split(':')]
    #         # 0 ~ 24시
    #         if (self.time2int(stime) - self.time2int(ctime) <= 0) and \
    #             (self.time2int(etime) - self.time2int(ctime) >= 0) and \
    #                 (datetime.now().day - self.cdate) == 0:
    #                     for j in range(5):
    #                         self.table.item(i,j).setBackground(QtGui.QColor(125,125,125))
    #                     break
    #         # 24시 시작 0시 종료 타이머는 24시 
    #         if (self.time2int(stime) - self.time2int(ctime) <= 0) and \
    #             (self.time2int(etime) - self.time2int(ctime) <= 0) and \
    #                 (datetime.now().day - self.cdate) == 0:
    #                     for j in range(5):
    #                         self.table.item(i,j).setBackground(QtGui.QColor(125,125,125))
    #                     break
            
    #         # 24시 시작 0시 종료 타이머는 0시 
    #         if (self.time2int(stime) - self.time2int(ctime) >= 0) and \
    #             (self.time2int(etime) - self.time2int(ctime) >= 0) and \
    #                 (datetime.now().day - self.cdate) != 0:
    #                     for j in range(5):
    #                         self.table.item(i,j).setBackground(QtGui.QColor(125,125,125))
    #                     break
                    
            # if (stime[0] - ctime[0]) > 0  
            
        #     s = datetime.(int(stime[0])
            
        #     print(stime)
        #     print(etime)
            # x = time2-time1
            # x = time2-time4
            
    def start(self,bc,tc,txt):
            self.frame.setStyleSheet(stylesheet.WIDGET_BG[bc])
            self.table.setStyleSheet(stylesheet.TABLE_TH_T[tc])
            self.title.setStyleSheet(stylesheet.TABLE_TH_T[tc])
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

    def study_end_time(self,starttime,studytime):

        # 공부시간
        sh = studytime.hour()
        sm = studytime.minute()
        ss = studytime.second()
        k = sm + + sh*60
        sh = starttime.hour() + sh
        sm = starttime.minute() + sm
        ss = starttime.second() + ss

        mins,secs = divmod(ss,60)
        
        hours,mins = divmod(sm + mins,60)
        hours = hours + sh

        days,hours = divmod(hours,24)

        return QtCore.QTime(hours,mins),k
    def time2int(self,times):
        
        h = times[0] * 60
        return h + times[1]
        
        
        
            
            
            
class RankingWidget(QDialog,utils.CLASS[3]):
    def __init__(self,parent):    
        super(RankingWidget,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(
                   self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)       
        self.show()
        self.setWindowIcon(QtGui.QIcon('./resource/icon/logo.png'))
        self.setWindowTitle('Rank DI')
        self.nickname.setText('사용자 #'+time.strftime("%H%M%S"))
        self.no.clicked.connect(self.close)
        self.yes.clicked.connect(self.apply)
    def close(self):
        self.parent().refresh()
        self.deleteLater()
    def apply(self):
        self.parent().nickname = self.nickname.text()
        self.parent().refresh()
        self.parent().update()
        self.deleteLater()

class VersionWidget(QDialog,utils.CLASS[2]):
    def __init__(self,parent):
        super(VersionWidget,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(
                   self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)       
        self.show()
        self.setWindowIcon(QtGui.QIcon('./resource/icon/logo.png'))
        self.setWindowTitle('WithDI Updater')
        self.cver = None
        self.flags = False
        self.but_update.clicked.connect(self.updates)
        self.but_close.clicked.connect(self.close)

    def close(self):
        if self.flags == True:
            self.parent().path()
        else:
            self.parent().vercheck = self.vercheck.isChecked()
            self.deleteLater()
    def sleep(self):
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(500, loop.quit) # msec
        loop.exec_()
    def updates(self):
        try:
            cv = self.cver.split('.')
            cv = (int(cv[0])*100 + int(cv[1])*10 + int(cv[2]))
            self.progressBar.setValue(10)
            self.log.setText('서버 접속중...')
            self.sleep()
            ftp = FTP(withDI.server_ip)
            try:
                self.log.setText('최신 버전 확인중...')
                self.sleep()
                self.progressBar.setValue(20)
                ftp.login(withDI.user_id, withDI.user_pw)
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
                        self.log.setText('최신 패치파일 설치 중...')
                        self.sleep()
                        self.progressBar.setValue(30)
                        ftp.cwd('/html/WithDIupdate/')
                        fd = open('path.exe','wb')
                        ftp.retrbinary ("RETR " + 'path.exe', fd.write)
                        fd.close()
                        self.progressBar.setValue(100)
                        self.log.setText('패치를 위해 확인을 눌러주세요.')
                        self.flags = True
                        self.but_update.setEnabled(False)
                        self.but_close.setText('확인')
                        config = configparser.ConfigParser()    
                        config.read('config.ini', encoding='utf-8') 
                        config['INFORMATION']['version'] =  ver[4:].split('.txt')[0]
                        with open('config.ini', 'w', encoding='utf-8') as configfile:
                            config.write(configfile)
                        ftp.close()
                    except:
                        self.log.setText('패치 파일 다운로드를 실패했습니다.')
            except:
                self.log.setText('서버 접속에 실패했습니다.')
                ftp.close()
        except: self.log.setText('WithDI 프로그램 오류가 발생했습니다.')

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ShowApp = WithDI()
    ShowApp.show()
    sys.exit(app.exec_())