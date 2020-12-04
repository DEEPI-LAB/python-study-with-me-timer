# -*- coding: utf-8 -*-
"""
With DI ver. 0.4.0
@author: Deep.I Inc. @Jongwon Kim
Revision date: 2020-12-04
See here for more information :
    https://deep-eye.tistory.com
    https://deep-i.net
"""
import sys
import os
import datetime
import timeit
import time
import pyglet
import random
import glob
import webbrowser

from resource.icon import icon

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication,QAction, QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5 import QtCore

path = glob.glob('./resource/*.ui')
for ui_path in path:
    ui_ = open(ui_path, 'r', encoding='utf-8')
    lines_ = ui_.readlines()
    ui_.close()
    for ii, i in enumerate(lines_):
        if 'include location' in i:
            lines_[ii] = i.replace('.qrc', '.py')
    ui_ = open(ui_path, 'w', encoding='utf-8')
    [ui_.write(i) for i in lines_]
    ui_.close()
    print('{} update'.format(ui_path))    

FROM_CLASS = uic.loadUiType("./resource/main.ui")[0]


class WithDI(QMainWindow,FROM_CLASS):
    def __init__(self):
        
        super().__init__() 
        # System Font Init
        _id1 = QtGui.QFontDatabase.addApplicationFont("./resource/font/Gong Gothic Bold.ttf")
        _id2 = QtGui.QFontDatabase.addApplicationFont("./resource/font/Gong Gothic Light.ttf")
        _id3 = QtGui.QFontDatabase.addApplicationFont("./resource/font/Gong Gothic Medium.ttf")
        QtGui.QFontDatabase.applicationFontFamilies(_id1)
        QtGui.QFontDatabase.applicationFontFamilies(_id2)
        QtGui.QFontDatabase.applicationFontFamilies(_id3)
        # UI load
        self.setupUi(self) 
        self.show()
        # Lolo load
        self.setWindowIcon(QtGui.QIcon('./resource/icon/logo.png')) 
        self.setWindowTitle('ver.0.4.0 | With DI' )
        
        # break time  lunch time
        self.FLAG = [False,False,False]
        self.iter = 0       # 교시
        
        # Log file init
        open('./log/[현재시간]_카운트.txt', mode='wt', encoding='utf-8')
        open('./log/[현재날짜]_카운트.txt', mode='wt', encoding='utf-8')
        open('./log/[공부시간]_카운트.txt', mode='wt', encoding='utf-8')
        open('./log/[쉬는시간]_카운트.txt', mode='wt', encoding='utf-8')        
        open('./log/[식사시간]_카운트.txt', mode='wt', encoding='utf-8')          
       
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(1000)
        
        # log pah linking
        abs_path = os.getcwd()
        self.date_output_path.setText(os.path.join(abs_path, 'log/[현재날짜]_카운트.txt'))
        self.time_output_path.setText(os.path.join(abs_path, 'log/[현재시간]_카운트.txt'))
        self.study_output_path.setText(os.path.join(abs_path, 'log/[공부시간]_카운트.txt'))
        self.break_output_path.setText(os.path.join(abs_path, 'log/[쉬는시간]_카운트.txt'))
        self.meal_output_path.setText(os.path.join(abs_path, 'log/[식사시간]_카운트.txt'))  
        
        self.default_date_format = "%Y년%m월%d일"
        self.default_time_format = "%H:%M:%S"
        self.default_count_format =  "hh:mm:ss"
        
        self.withdistart.clicked.connect(self.startTimer)
        
        #%% 날짜 INIT
        self.init_date_format = self.default_date_format
        self.init_date_string_1 = "오늘은 "
        self.init_date_string_2 = " 입니다."

        
        self.date_output_string.textChanged.connect(self.dateStringChage)
        self.date_output_format.textChanged.connect(self.dateOuputChage)
        self.date_output_format_reset.clicked.connect(self.date_format_re)
        self.date_output_string_reset.clicked.connect(self.date_string_re)
        
        #%% 시간 INIT
        self.init_time_format = self.default_time_format
        self.init_time_string_1 = "지금은 "
        self.init_time_string_2 = " 입니다."
        
        self.time_output_string.textChanged.connect(self.timeStringChage)
        self.time_output_format.textChanged.connect(self.timeOuputChage)
        self.time_output_format_reset.clicked.connect(self.time_format_re)
        self.time_output_string_reset.clicked.connect(self.time_string_re) 
        
        #%% 공부시간 INIT
        self.init_study_format = self.default_count_format
        self.init_study_string_1 = "공부시간 : "
        self.init_study_string_2 = ""
        
        self.studytime_edit.setTime(QTime(1,15,0))  
        h,m = QTime.currentTime().hour(),QTime.currentTime().minute()
        self.starttime_edit.setTime(QTime(h,m+1,0))
        self.study_end_time()
        self.studytime_edit.timeChanged.connect(self.study_end_time)
        self.study_ep.timeChanged.connect(self.study_end_time)
        self.starttime_edit.timeChanged.connect(self.study_end_time)
        self.study_output_format_reset.clicked.connect(self.study_format_re)
        self.study_output_string_reset.clicked.connect(self.study_string_re) 
        
        #%% 휴식 시간 INIT
        self.init_break_format = self.default_count_format
        self.init_break_string_1 = "쉬는시간 : "
        self.init_break_string_2 = ""
        
        self.breaktime_edit.setTime(QTime(0,15,0))  
        
        self.break_output_format_reset.clicked.connect(self.break_format_re)
        self.break_output_string_reset.clicked.connect(self.break_string_re) 
        
        #%% 식사 시간 INIT
        self.init_meal_format = self.default_count_format
        self.init_meal_string_1 = "식사시간 : "
        self.init_meal_string_2 = ""       
        
        self.mealtime_edit.setTime(QTime(0,45,0))  
        self.meal_slider.valueChanged.connect(self.mealMode)  
        self.meal_output_format_reset.clicked.connect(self.meal_format_re)
        self.meal_output_string_reset.clicked.connect(self.meal_string_re) 

        #%% 휴게 시간
        abs_path = os.getcwd()
        self.break_start_sound_path.setText(os.path.join(abs_path, 'resource/sound/breaktime.mp3'))    
        self.break_sound_path.setText(os.path.join(abs_path, 'resource/music/music.wav'))   
        self.break_end_sound_path.setText(os.path.join(abs_path, 'resource/sound/breaktime.mp3'))   
        # Sound button
        self.asmr.clicked.connect(lambda: webbrowser.open('https://asoftmurmur.com/'))
        self.play_1.clicked.connect(lambda: self.playMusic(0))
        self.play_2.clicked.connect(lambda: self.playMusic(1))
        self.play_3.clicked.connect(lambda: self.playMusic(2))
        self.sound_slider.valueChanged.connect(self.soundMode)
        # Sound path button
        self.path = [self.path_1,self.path_2,self.path_3]
        self.path[0].clicked.connect(lambda: self.searchFile(0))
        self.path[1].clicked.connect(lambda: self.searchFile(1))
        self.path[2].clicked.connect(lambda: self.searchFile(2))
        self.sound_path = [self.break_start_sound_path,self.break_sound_path,
                           self.break_end_sound_path]
        # read me
        self.lablink.clicked.connect(lambda: webbrowser.open('https://deep-eye.tistory.com/32?category=442879'))
        self.gitlink.clicked.connect(lambda: webbrowser.open('https://deep-eye.tistory.com/32?category=442879'))
                                     
    def refresh(self):
        
        # study / break / lunch time init
        self.study_time_count = QTime(0, 0, 0)             
        self.study_time_count_m = self.studytime_edit.time()   
        
        self.break_time_count = self.breaktime_edit.time()  
        self.break_time_count_m = QTime(0, 0, 0)
        
        self.mealTime = self.meal_slider.value()
        self.meal_time_count = self.mealtime_edit.time()
        self.meal_time_count_m = QTime(0,0,0)
        
        self.ep = self.study_ep.time().hour()
        self.starttime = self.starttime_edit.time()
        self.FLAG[0] = True
        self.classes = 0
        
        self.checkStudyTime()
        self.checkBreakCount()
        self.checkMealCount()

        self.widget_timetable.setText('{}교시 준비중'.format(self.classes+1))
        self.setWindowTitle('ver.0.4.0 | With DI | Live 대기중' )
        self.tabWidget.setCurrentIndex(3)
        
    def run(self):
        
        # Today 시스템 시간 활성화
        self.time_pc.setText(time.strftime(self.init_time_format))
        self.date_pc.setText(time.strftime(self.init_date_format))
        # Today 업데이트 활성화
        self.time_output_live.setText(self.init_time_string_1 + 
                                      time.strftime(self.init_time_format) + 
                                      self.init_time_string_2)
        
        self.date_pc.setText(time.strftime(self.default_date_format))
        self.date_output_live.setText(self.init_date_string_1 + 
                                      time.strftime(self.default_date_format) + 
                                      self.init_date_string_2)
        
        # Study 업데이트 활성화
        if True:
            self.checkTime()
            self.checkDate()
            
            # 시작 시점 
            if self.FLAG[0] == False : return
            if self.starttime.toString() == QTime.currentTime().toString():
                print('스터디윗미 시작')
                self.setWindowTitle('ver.0.4.0 | With DI | Live 공부 중' )
                self.FLAG[1] = True
                return

            if  self.ep <= self.classes : 
                self.setWindowTitle('ver.0.4.0 | With DI | Live 대기 중' )
                print('수고하셨습니다.')
                self.FLAG[1] = False 
                self.FLAG[2] = False
                self.FLAG[0] = False
            if self.FLAG[0] == True and self.FLAG[1] == True and self.FLAG[2]==False:

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
                    # 종소리 
                    if self.bh  == 10:
                        self.song = pyglet.media.Player()
                        x= pyglet.media.load(self.break_sound_path.text())
                        self.song.queue(x)
                        self.song.volume = self.sound_slider.value()/100.0
                        self.song.play()
  
                    elif self.break_time_count.toString() == '00:00:00':
                        
                        self.song = pyglet.media.Player()
                        x= pyglet.media.load(self.break_end_sound_path.text())
                        self.song.queue(x)
                        self.song.volume = self.sound_slider.value()/100.0
                        self.song.play()
                        self.FLAG[2] = False
                        self.break_time_count = self.breaktime_edit.time() 
                        # self.break_time_count =  self.break_time_count.addSecs(1)
                        print('쉬는시간 종료')
                        self.widget_timetable.setText('{}교시 진행중'.format(self.classes+1))
                        return

                elif self.mealTime == self.classes and self.ep >= self.classes:

                    self.meal_time_count =  self.meal_time_count.addSecs(-1)
                    self.meal_time_count_m =  self.meal_time_count_m.addSecs(1)
                    # 쉬는시간 업 업데이트
                    self.checkMealCount()   
                
                    if self.meal_time_count.toString() == '00:00:00':
                        self.song = pyglet.media.Player()
                        x= pyglet.media.load(self.break_end_sound_path.text())
                        self.song.queue(x)
                        self.song.volume = self.sound_slider.value()/100.0
                        self.song.play()
                        self.meal_time_count = self.mealtime_edit.time()
                        self.FLAG[2] = False
                        self.mealTime =0
                        print('점심시간 종료')
                        self.widget_timetable.setText('{}교시 진행중'.format(self.classes+1))
                        return
    # 업데이트 
    def checkDate(self):
        try:
            self.current_date.setText(time.strftime('%Y년 %m월 %d일'))
            c_date = open('./log/[현재날짜]_카운트.txt', mode='wt', encoding='utf-8')
            txt = self.init_date_string_1 + time.strftime(self.date_output_format.text()) + self.init_date_string_2
            c_date.write(txt)
            c_date.close()
        except:pass         
    def checkTime(self):
        try:
            self.current_time.setText(time.strftime('%H시 %M분 %S초'))
            c_time = open('./log/[현재시간]_카운트.txt', mode='wt', encoding='utf-8')
            c_time.write(self.init_time_string_1+time.strftime(self.time_output_format.text())+self.init_time_string_2)
            c_time.close() 
        except:pass
    def checkStudyTime(self):
        self.current_study.setText(self.study_time_count.toString("hh시간 mm분 ss초"))
        t = self.study_time_count.toString(self.study_output_format.text())
        xx = self.study_output_string.text().split('%')
        
        c_date = open('./log/[공부시간]_카운트.txt', mode='wt', encoding='utf-8')
        c_date.write(xx[0]+t+xx[2])
        c_date.close() 

    def checkBreakCount(self):
    
        try:
            self.current_break.setText(self.break_time_count_m.toString("hh시간 mm분 ss초"))
            t = self.break_time_count.toString(self.break_output_format.text())
            xx = self.break_output_string.text().split('%')
            c_date = open('./log/[쉬는시간]_카운트.txt', mode='wt', encoding='utf-8')
            c_date.write(xx[0]+t+xx[2])
            c_date.close()       
        except:pass
    
    def checkMealCount(self):
        try:
            self.current_meal.setText(self.meal_time_count_m.toString("hh시간 mm분 ss초"))
            t = seconds=self.meal_time_count.toString(self.meal_output_format.text())
            xx = self.meal_output_string.text().split('%')
            c_date = open('./log/[식사시간]_카운트.txt', mode='wt', encoding='utf-8')
            c_date.write(xx[0]+t+xx[2])
            c_date.close()
        except:pass           
    
    def dateOuputChage(self):
        try:
            x = time.strftime(self.date_output_format.text())
            
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
            self.endtime_edit.setText('+ {}일 '.format(days)+QTime(hours,mins,secs).toString("hh시 : mm분 : ss초"))
        else:
            self.endtime_edit.setText(QTime(hours,mins,secs).toString("hh시 : mm분 : ss초"))
    

    def mealMode(self):
            self.meal_times.setText('{}교시 종료 후'.format(self.meal_slider.value()))
            
    def soundMode(self):
        self.sound_val.setText(str(self.sound_slider.value()))
        
        try:
            self.song
            self.song.volume = self.sound_slider.value() / 100.0
        except:pass
        
        
    def date_format_re(self):
        self.date_output_format.setText("%Y년%m월%d일")
        self.dateOuputChage()

    def date_string_re(self):
        self.date_output_string.setText("오늘은 %DATE% 입니다.")
        self.dateStringChage()
        
    def time_format_re(self):
        self.time_output_format.setText("%H:%M:%S")
        self.timeOuputChage()

    def time_string_re(self):
        self.time_output_string.setText("지금 시간은 %DATE% 입니다.")
        self.timeStringChage()        

    def study_format_re(self):
        self.study_output_format.setText("%H:%M:%S")

    def study_string_re(self):
        self.init_study_string_1 = "공부시간 : "
        self.init_study_string_2 = ""
        self.study_output_string.setText("공부시간 : %TIME%")
  
    def break_format_re(self):
        self.break_output_format.setText("%H:%M:%S")
    
    def break_string_re(self):
        self.init_break_string_1 = "쉬는시간 : "
        self.init_break_string_2 = ""
        self.break_output_string.setText("쉬는시간 : %TIME%")
        
    def meal_format_re(self):
        self.meal_output_format.setText("%H:%M:%S")
    
    def meal_string_re(self):
        self.init_meal_string_1 = "식사시간 : "
        self.init_meal_string_2 = ""
        self.meal_output_string.setText("식사시간 : %TIME%")   
        
    def playMusic(self,ids):
        
        try:
            self.song
            self.song.pause()
            self.song.delete()
        except: pass
        self.song = pyglet.media.Player()
        if ids == 0:
            x= pyglet.media.load(self.break_start_sound_path.text())
        elif ids == 1:
            x= pyglet.media.load(self.break_sound_path.text())
        elif ids == 2:
            x= pyglet.media.load(self.break_end_sound_path.text())
            
        self.song.queue(x)  
        self.song.volume = self.sound_slider.value()/100.0
        self.song.play()
        

    def searchFile(self,ids):
        fname = QFileDialog.getOpenFileName(self, '음악파일을 선택해주세요.', './',"Audio files (*.mp3 *.wav)")
        if fname[0] == True:
            self.sound_path[ids].setText(fname[0])
            
    def startTimer(self):
        self.refresh()
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ShowApp = WithDI()
    sys.exit(app.exec_())


