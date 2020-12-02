# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 11:58:42 2020

@author: pod LAB. Kim Jongwon
"""
import sys
import os
import datetime
import timeit
import time
import pyglet
import random
import glob
from icon import icon
from matplotlib import font_manager
 
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5 import QtCore

path = glob.glob('*.ui')
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

FROM_CLASS = uic.loadUiType("main.ui")[0]

class WithDI(QMainWindow,FROM_CLASS):
    def __init__(self):
        
        super().__init__() 
        global TEST
        self.setupUi(self) 
        self.show()

        self.setWindowIcon(QtGui.QIcon('./icon/logo.png')) 
        self.setWindowTitle('ver.0.2.0 | With DI' )
        self.FLAG = [False,False,False]
        self.iter = 0       # 교시
        self.mealTime = 99  # 디폴트 점심시간
        open('./log/현재시간.txt', mode='wt', encoding='utf-8')
        open('./log/현재날짜.txt', mode='wt', encoding='utf-8')
        open('./log/공부시간카운트_up.txt', mode='wt', encoding='utf-8')
        open('./log/공부시간카운트_down.txt', mode='wt', encoding='utf-8')
        open('./log/쉬는시간카운트_up.txt', mode='wt', encoding='utf-8')
        open('./log/쉬는시간카운트_down.txt', mode='wt', encoding='utf-8')        
        open('./log/식사시간카운트_down.txt', mode='wt', encoding='utf-8')          
       

        self.breakFlag = True
        
        
        self.start_basic.clicked.connect(self.flagPush_1)
        self.start_adv.clicked.connect(self.flagPush_2)
        self.save_config.clicked.connect(self.flagPush_3)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(1000)
        
        #%% 날짜 INIT
        self.init_date_format = "%Y년 %m월 %d일"
        self.init_date_string_1 = "오늘은 "
        self.init_date_string_2 = " 입니다."

        abs_path = os.getcwd()
        self.date_output_path.setText(os.path.join(abs_path, 'log/현재날짜.txt'))
        

        self.date_pc.setText(time.strftime("%Y년 %m월 %d일"))
        self.date_output_live.setText(self.init_date_string_1 + 
                                      time.strftime("%Y년 %m월 %d일") + 
                                      self.init_date_string_2)
        
        self.date_output_string.textChanged.connect(self.dateStringChage)
        self.date_output_format.textChanged.connect(self.dateOuputChage)
        self.date_output_format_reset.clicked.connect(self.date_format_re)
        self.date_output_string_reset.clicked.connect(self.date_string_re)
        
        #%% 시간 INIT
        self.init_time_format = "%H : %M : %S"
        self.init_time_string_1 = "지금은 "
        self.init_time_string_2 = " 입니다."

        abs_path = os.getcwd()
        self.time_output_path.setText(os.path.join(abs_path, 'log/현재시간.txt'))
        

        self.time_output_string.textChanged.connect(self.timeStringChage)
        self.time_output_format.textChanged.connect(self.timeOuputChage)
        self.time_output_format_reset.clicked.connect(self.time_format_re)
        self.time_output_string_reset.clicked.connect(self.time_string_re) 
        
        #%% 공부시간 INIT
        self.init_study_format = "hh : mm : ss"
        self.init_study_string_1 = "공부시간 : "
        self.init_study_string_2 = ""
        self.stuy_count = True
        
        self.study_slider.setValue(0)
        self.studytime_edit.setTime(QTime(1,15))  
        self.study_min = self.studytime_edit.time().minute()
        self.study_hour = self.studytime_edit.time().hour()
        

        abs_path = os.getcwd()
        self.study_output_path.setText(os.path.join(abs_path, 'log/공부시간카운트_up.txt'))
        self.study_slider.valueChanged.connect(self.studyMode)
        
        self.study_output_format_reset.clicked.connect(self.study_format_re)
        self.study_output_string_reset.clicked.connect(self.study_string_re) 
        
        #%% 휴식 시간 INIT
        
        self.init_break_format = "hh : mm : ss"
        self.init_break_string_1 = "쉬는시간 : "
        self.init_break_string_2 = ""
        self.break_count = True
        
        self.break_slider.setValue(0)
        self.breaktime_edit.setTime(QTime(0,15))  
        self.break_min = self.studytime_edit.time().minute()
        self.break_hour = self.studytime_edit.time().hour()
        
        abs_path = os.getcwd()
        self.break_output_path.setText(os.path.join(abs_path, 'log/쉬는시간카운트_up.txt'))
        self.break_slider.valueChanged.connect(self.breakMode)  
        
        self.break_output_format_reset.clicked.connect(self.break_format_re)
        self.break_output_string_reset.clicked.connect(self.break_string_re) 
        
        #%% 식사 시간 INIT
        self.init_meal_format = "hh : mm : ss"
        self.init_meal_string_1 = "식사시간 : "
        self.init_meal_string_2 = ""        
        
        abs_path = os.getcwd()
        self.meal_output_path.setText(os.path.join(abs_path, 'log/식사시간카운트_up.txt'))        
        self.meal_slider.valueChanged.connect(self.mealMode)  
        
        self.meal_output_format_reset.clicked.connect(self.meal_format_re)
        self.meal_output_string_reset.clicked.connect(self.meal_string_re) 
        self.mealFlag = False

        #%% 휴게 시간
        abs_path = os.getcwd()
        self.break_start_sound_path.setText(os.path.join(abs_path, 'sound/breaktime.mp3'))    
        self.break_sound_path.setText(os.path.join(abs_path, 'music/music_1.wav'))   
        self.break_end_sound_path.setText(os.path.join(abs_path, 'sound/breaktime.mp3'))   
        
        self.play_1.clicked.connect(lambda: self.playMusic(0))
        self.play_2.clicked.connect(lambda: self.playMusic(1))
        self.play_3.clicked.connect(lambda: self.playMusic(2))
        self.sound_slider.valueChanged.connect(self.soundMode)
        
        self.path = [self.path_1,self.path_2,self.path_3]
        self.path[0].clicked.connect(lambda: self.searchFile(0))
        self.path[1].clicked.connect(lambda: self.searchFile(1))
        self.path[2].clicked.connect(lambda: self.searchFile(2))
        
        self.sound_path = [self.break_start_sound_path,self.break_sound_path,self.break_end_sound_path]
        
    def refresh(self):
        self.study_sec = self.studytime_edit.time().second()
        self.study_min = self.studytime_edit.time().minute()
        self.study_hour = self.studytime_edit.time().hour()
        
        self.break_min = self.breaktime_edit.time().minute()
        self.break_hour = self.breaktime_edit.time().hour()
        self.break_sec = self.breaktime_edit.time().second()
        
        self.count_down =  self.study_hour * 3600 + 60 * self.study_min + self.study_sec
        self.breaking_time = self.break_hour * 3600 + 60 * self.break_min+ self.break_sec

        self.breakFlag = True
        self.widget_timetable.setText('{}교시 진행중'.format(self.iter))
        self.study_time_count_up   = QTime(0, 0, 0)                   
        self.study_time_count_down = QTime(self.study_hour, self.study_min, self.study_sec)           
        self.break_time_count_down = QTime(self.break_hour, self.break_min, self.break_sec)           
        self.break_time_count_up   = QTime(0, 0, 0)                        
        
        self.checkStudyCount()
        self.checkBreakCount()
        self.checkBreakTime()
        self.checkStudyTime()
        self.checkDate()
        
    def Mealrefresh(self):
        self.mealTime = self.meal_slider.value()
        self.mealFlag = True
        self.meal_min = self.mealtime_edit.time().minute()
        self.meal_hour = self.mealtime_edit.time().hour()
        self.meal_sec = self.mealtime_edit.time().second()
        self.meal_time = self.meal_hour * 3600 + 60 * self.meal_min 
        self.meal_time_count_down =  QTime(self.meal_hour, self.meal_min, self.meal_sec)          
        self.checkMealCount()
        
    def run(self):
        
        # settings
        self.time_pc.setText(time.strftime(self.init_time_format))
        self.time_output_live.setText(self.init_time_string_1 + 
                                      time.strftime(self.init_time_format) + 
                                      self.init_time_string_2)

        # Default 
        # 시간 업데이트
        if self.FLAG[0] ==True:
            self.checkTime()
            
        
        if self.breakFlag == True and self.FLAG[1] == True: 
            self.study_time_count_up = self.study_time_count_up.addSecs(1)
            self.study_time_count_down =  self.study_time_count_down.addSecs(-1)
            
            # 공부시간 업 업데이트
            self.checkStudyTime()
            # 공부시간 다운 업데이트
            self.checkStudyCount()
           

            if self.study_time_count_down.hour() == 0 \
                and self.study_time_count_down.minute() == 0 \
                    and self.study_time_count_down.second() == 0:
                
                if self.iter == self.mealTime:
                    self.mealFlag =True
                else:
                    self.breakFlag = False
                self.study_time_count_down = self.count_down
                
                
                song = pyglet.media.Player()
                x= pyglet.media.load(self.break_start_sound_path.text())
                song.queue(x)
                song.volume = self.sound_slider.value()/100.0
                song.play()
                
                
                self.widget_timetable.setText('{}교시 종료'.format(self.iter))
                self.iter += 1
        
        elif  self.breakFlag == False and self.FLAG[1] == True and self.mealFlag == True:    
            self.meal_time_count_down  =  self.meal_time_count_down .addSecs(-1)
            self.checkMealCount()  
            
            if self.meal_time_count_down.hour() == 0 \
                and self.meal_time_count_down.minute() == 0 \
                    and self.meal_time_count_down.second() == 5:
                        
                self.mealFlag = False
                song = pyglet.media.Player()
                x= pyglet.media.load(self.break_end_sound_path.text())
                song.queue(x)
                song.volume = self.sound_slider.value()/100.0
                song.play()
                self.widget_timetable.setText('{}교시 진행중'.format(self.iter))
                self.meal_time_count_down =QTime(self.meal_hour, self.meal_min, self.meal_sec)  

        elif  self.breakFlag == False and self.FLAG[1] == True:
            
            self.break_time_count_up  = self.break_time_count_up.addSecs(1)
            self.break_time_count_down =  self.break_time_count_down.addSecs(-1)
            
            # 쉬는시간 업 업데이트
            self.checkBreakTime()
            # 쉬는시간 다운 업데이트
            self.checkBreakCount()     
            
            if self.break_time_count_down.hour() == 0 \
                and self.break_time_count_down.minute() == 0 \
                    and self.break_time_count_down.second() == 0:
                self.breakFlag = True
                
                self.study_time_count_down = QTime(self.study_hour, self.study_min, self.study_sec)  
                self.break_time_count_down  =QTime(self.break_hour, self.break_min, self.break_sec)  
                song = pyglet.media.Player()
                x= pyglet.media.load(self.break_end_sound_path.text())
                song.queue(x)
                song.volume = self.sound_slider.value()/100.0
                song.play()
                self.widget_timetable.setText('{}교시 진행중'.format(self.iter))
                self.checkBreakCount()
                self.checkBreakTime()
                
            if self.break_time_count_down.hour() == 0 \
                and self.break_time_count_down.minute() == 0 \
                    and self.break_time_count_down.second() == 5:
                song = pyglet.media.Player()
                x= pyglet.media.load(self.break_sound_path.text())
                song.queue(x)
                song.volume = self.sound_slider.value()/100.0              

    def checkDate(self):
        c_date = open('./log/현재날짜.txt', mode='wt', encoding='utf-8')
        txt = self.init_date_string_1 + time.strftime(self.date_output_format.text()) + self.init_date_string_2
        c_date.write(txt)
        c_date.close()
    def checkTime(self):
        c_time = open('./log/현재시간.txt', mode='wt', encoding='utf-8')
        c_time.write(self.init_time_string_1+time.strftime(self.time_output_format.text())+self.init_time_string_2)
        c_time.close() 
        
    def checkStudyTime(self):
        t = self.study_time_count_up.toString(self.study_output_format.text())
        xx = self.study_output_string.text().split('%')
        
        c_date = open('./log/공부시간카운트_up.txt', mode='wt', encoding='utf-8')
        c_date.write(xx[0]+t+xx[2])
        c_date.close() 
        
    def checkStudyCount(self):
        try:
            t = self.study_time_count_down.toString(self.study_output_format.text())
            xx = self.study_output_string.text().split('%')
            c_date = open('./log/공부시간카운트_down.txt', mode='wt', encoding='utf-8')
            c_date.write(xx[0]+t+xx[2])
            c_date.close() 
        except:pass
    def checkBreakTime(self):
        try:
            t = self.break_time_count_up.toString(self.break_output_format.text())
            xx = self.break_output_string.text().split('%')
            c_date = open('./log/쉬는시간카운트_up.txt', mode='wt', encoding='utf-8')
            c_date.write(xx[0]+t+xx[2])
            c_date.close() 
        except:pass
    def checkBreakCount(self):
    
        try:
            t = self.break_time_count_down.toString(self.break_output_format.text())
            xx = self.break_output_string.text().split('%')
            c_date = open('./log/쉬는시간카운트_down.txt', mode='wt', encoding='utf-8')
            c_date.write(xx[0]+t+xx[2])
            c_date.close()       
        except:pass
    def checkMealCount(self):
        try:
            t = seconds=self.meal_time_count_down.toString(self.meal_output_format.text())
            xx = self.meal_output_string.text().split('%')
            c_date = open('./log/식사시간카운트_down.txt', mode='wt', encoding='utf-8')
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





    def studyMode(self):
        if self.study_slider.value() == 0:
            abs_path = os.getcwd()
            self.study_output_path.setText(os.path.join(abs_path, 'log/공부시간카운트_up.txt'))
            self.stuy_count = True
        else: 
            abs_path = os.getcwd()
            self.study_output_path.setText(os.path.join(abs_path, 'log/공부시간카운트_down.txt'))    
            self.stuy_count = False
    def breakMode(self):
        if self.break_slider.value() == 0:
            abs_path = os.getcwd()
            self.break_output_path.setText(os.path.join(abs_path, 'log/쉬는시간카운트_up.txt'))
            self.break_count = True
        else: 
            abs_path = os.getcwd()
            self.break_output_path.setText(os.path.join(abs_path, 'log/쉬는시간카운트_down.txt'))    
            self.break_count = False            
    
    def mealMode(self):
            self.meal_times.setText('{}교시 종료 후'.format(self.meal_slider.value()+1))
            
    def soundMode(self):
        self.sound_val.setText(str(self.sound_slider.value()))
        
        try:
            self.song
            self.song.volume = self.sound_slider.value() / 100.0
        except:pass
        
    def flagPush_1(self):
        self.FLAG[0] = True
        self.start_basic_status.setText('Today 타이머가 시작되었습니다')
        self.refresh()
    def flagPush_2(self):
        self.FLAG[1] = True
        self.start_adv_status.setText('Study 타이머가 시작되었습니다')
        self.refresh()
    def flagPush_3(self):
        self.save_config_status.setText('Lunch 타이머가 시작되었습니다')
        self.Mealrefresh()          
        
    def date_format_re(self):
        self.date_output_format.setText("%Y년 %m월 %d일")
        self.dateOuputChage()

    def date_string_re(self):
        self.date_output_string.setText("오늘은 %DATE% 입니다.")
        self.dateStringChage()
        
    def time_format_re(self):
        self.time_output_format.setText("%H : %M : %S")
        self.timeOuputChage()

    def time_string_re(self):
        self.time_output_string.setText("지금 시간은 %DATE% 입니다.")
        self.timeStringChage()        

    def study_format_re(self):
        self.study_output_format.setText("%H : %M : %S")

    def study_string_re(self):
        self.init_study_string_1 = "공부시간 : "
        self.init_study_string_2 = ""
        self.study_output_string.setText("공부시간 : %TIME%")
  
    def break_format_re(self):
        self.break_output_format.setText("%H : %M : %S")
    
    def break_string_re(self):
        self.init_break_string_1 = "쉬는시간 : "
        self.init_break_string_2 = ""
        self.break_output_string.setText("쉬는시간 : %TIME%")
        
    def meal_format_re(self):
        self.meal_output_format.setText("%H : %M : %S")
    
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


        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ShowApp = WithDI()
    sys.exit(app.exec_())


