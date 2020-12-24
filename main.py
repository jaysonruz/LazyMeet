##imports
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5 import uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 

from backports import configparser

from configManager import ConfigManager
#----------------------------------------------------------
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi("gui.ui", self)
        #-------------------------------------------------------------------       
        self.settings = QSettings('LazyMeet','App state')
        self.configManager = ConfigManager()
        self.config = configparser.ConfigParser()
        
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

    def onApply(self):
        '''
        creates dictionary of values that user has provided and writes to config file using configmanager
        '''
        d = {'CookieDirectory': self.lineEdit_cookieDirectory.text(),'GoogleMeetLink': self.lineEdit_meetingLink.text(),'Date':self.DateEdit.date().toPyDate(),
            'startTime':self.timeEdit_Start.time().toString(),'endTime':self.timeEdit_End.time().toString()}
        self.configManager.setUserconfig(d)
        self.updateconfig()
        self.pushButton_Apply.setText('Applied')

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
        
 

 
 
 
 
 
#-----x----------x-----------x----------
app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())