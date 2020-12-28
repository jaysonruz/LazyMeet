##imports
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5 import uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 

from threading import Thread , Condition# ---- threading
import time
from backports import configparser

from configManager import ConfigManager
from googleMeetBot import meet_bot
#----------------------------------------------------------
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi("gui.ui", self)
        #-------------------------------------------------------------------  
            
        self.settings = QSettings('LazyMeet','App state')
        self.configManager = ConfigManager()
        self.config = configparser.ConfigParser()
        self.timeLabel = self.findChild(QLabel,"timelabel")

        self.stop_threads = False  # ---- threading
        self.thread_condition = Condition()
        try:
            ####
            #loads application previous state like size n position 
            ###
            self.updateconfig()
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
        except :
            pass
        
        ##
        #linking apply button and reset button to their respective function
        self.button_Apply = self.findChild(QPushButton,"pushButton_Apply")
        self.button_Apply.clicked.connect(self.onApply)
        self.button_reset = self.findChild(QPushButton,"pushButton_Reset")
        self.button_reset.clicked.connect(self.onReset)
        self.button_Browse = self.findChild(QPushButton,"pushButton_Browse")
        self.button_Browse.clicked.connect(self.change_cookie_directory)
        self.button_start = self.findChild(QPushButton,"pushButton_Start")
        self.button_start.clicked.connect(self.start)
        self.button_stop = self.findChild(QPushButton,"pushButton_Stop")
        self.button_stop.clicked.connect(self.stop)
        self.button_test = self.findChild(QPushButton,"pushButton_TEST")
        self.button_test.clicked.connect(self.test)
    
    def _countdown(self,stop):
        print("debug: function running")

        x = int(self.config["timings"]["deltatime"])
        y = int(self.config["timings"]["deltameetingtime"])
        print(x,y)
        if x < 0:
            self.timeLabel.setText("Please check if date/time is set correctly.")

        for i in range(x,0,-1):
            print("starting countdown")
            print(i)
            time.sleep(1)
            self.timeLabel.setText(self.configManager.deltaTime()[0])
            if i < 60:
                self.timeLabel.setText(str(i))
                if i == 1:
                    print("starting meeting")
                    self.timeLabel.setText("starting meeting")

                    self.obj = meet_bot(cookie_directory= self.cookie_directory,gmeet_link=self.meeting_link)
                    self.obj.login()

                    for j in range(y,0,-1):
                        print("starting meeting timer")
                        time.sleep(1)
                        self.timeLabel.setText(str(j))
                        if j == 1:
                            self.stop()
            if stop(): 
                break



    def start(self):
        """
        docstring
        """
        self.t = Thread(target=self._countdown,args =(lambda : self.stop_threads, )) # ---- threading
        self.t.start() # ---- threading

    def stop(self):
        """
        docstring
        """
        #TODO here rather then stoping the thread we want to pause the thread instead and kill the thread only when we kill the application 

        # self.stop_threads = True
        
        # self.t.join()
        print("acquiring lock...")
        self.thread_condition.acquire()
        try:
            self.thread_condition.wait(15)
            print("waiting")
        # finally:
        #     self.thread_condition.release()
        ##
        # logs out
        try:
            self.obj.logout()
            self.timeLabel.setText('welcome to LazyMeet')
        except:
            pass
          
    def test(self):
        """
        docstring
        """
        self.obj = meet_bot(cookie_directory= self.cookie_directory,gmeet_link=self.meeting_link)
        self.obj.login()
        time.sleep(2)
        self.stop()
        pass    

    def dateToQdate(self,_date):
        '''
        takes date of type str eg 2020-12-31 and return Qdate(2020,12,31)
        ''' 
        d=_date.split("-")
        return QDate(int(d[0]),int(d[1]),int(d[2]))
    def timeTOQtime(self,_time):
        '''
        takes time of type str eg.04:03:00 and return Qtime(04,03,00)
        '''
        d=_time.split(":")
        return QTime(int(d[0]),int(d[1]),int(d[2]))

    def updateconfig(self):
        #####
        #Loads userconfig from file if it is available 
        #####
        self.config.read('config.ini')
        #----defining interface
        self.lineEdit_cookieDirectory = self.findChild(QLineEdit,"lineEdit_cookieDirectory")
        self.lineEdit_meetingLink = self.findChild(QLineEdit,"lineEdit_meetingLink")
        self.DateEdit = self.findChild(QDateEdit,"dateEdit")
        self.timeEdit_Start = self.findChild(QTimeEdit,"timeEdit_Start")
        self.timeEdit_End = self.findChild(QTimeEdit,"timeEdit_End")
        #----update interface
        self.lineEdit_cookieDirectory.setText(self.config["UserConfig"]["cookiedirectory"])
        self.lineEdit_meetingLink.setText(self.config["UserConfig"]["googlemeetlink"])
        self.DateEdit.setDate(self.dateToQdate(self.config["UserConfig"]['date']))
        self.timeEdit_Start.setTime(self.timeTOQtime(self.config["UserConfig"]['starttime']))
        self.timeEdit_End.setTime(self.timeTOQtime(self.config["UserConfig"]['endtime']))
        #---update variables 
        self.cookie_directory = self.config["UserConfig"]['cookiedirectory']
        self.meeting_link= self.config["UserConfig"]['googlemeetlink']

    def onApply(self):
        '''
        creates dictionary of values that user has provided and writes to config file using configmanager
        '''
        d = {'CookieDirectory': self.lineEdit_cookieDirectory.text(),'GoogleMeetLink': self.lineEdit_meetingLink.text(),'Date':self.DateEdit.date().toPyDate(),
            'startTime':self.timeEdit_Start.time().toString(),'endTime':self.timeEdit_End.time().toString()}
        
        self.configManager.setUserconfig(d)
        self.configManager.setDeltaTime()
        self.updateconfig()
        self.pushButton_Apply.setText('Apply')

    def onReset(self):
        '''
        overwrites user config reseting it to default
        '''
        self.configManager.resetConfig()
        try:
            self.updateconfig()
        except:
            pass

    def change_cookie_directory(self):

        try:
            self.folder = str(QFileDialog.getExistingDirectory(None, "Select Directory",self.lineEdit_cookieDirectory.text()))
        except:
            self.folder = str(QFileDialog.getExistingDirectory(None, "Select Directory","c:/Users/"))

        self.lineEdit_cookieDirectory = self.findChild(QLineEdit,"lineEdit_cookieDirectory")
        self.lineEdit_cookieDirectory.setText(self.folder)
        self.cookie_directory = self.folder


    def closeEvent(self,event):
        '''
        this method is executed when exiting app
        '''

        close = QMessageBox.question(self,
                                    "QUIT",
                                    "Are you sure want to stop process?",
                                    QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())
        #stops the active thread 
        try:
            self.stop_threads = True
            self.t.join()
        except:
            pass

 

 
 
 
 
 
#-----x----------x-----------x----------
app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())