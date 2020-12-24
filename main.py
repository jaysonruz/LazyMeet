from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit ,QMessageBox ,QLineEdit
from PyQt5 import uic
import sys
from PyQt5.QtCore import QSettings 

from backports import configparser

from configManager import ConfigManager

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
    
    def updateconfig(self):
        #####
        #Loads userconfig from file if it is available 
        #####
        self.config.read('config.ini')
        self.lineEdit_cookieDirectory = self.findChild(QLineEdit,"lineEdit_cookieDirectory")
        print(self.lineEdit_cookieDirectory.text())
        self.lineEdit_cookieDirectory.setText(self.config["UserConfig"]["cookiedirectory"])

        self.lineEdit_meetingLink = self.findChild(QLineEdit,"lineEdit_meetingLink")
        print(self.lineEdit_meetingLink.text())
        self.lineEdit_meetingLink.setText(self.config["UserConfig"]["googlemeetlink"])

    def onApply(self):
        '''
        creates dictionary of values that user has provided and writes to config file using configmanager
        '''
        #TODO implementing time and date to be stored in configfile
        print(self.settings.fileName())
        d = {'CookieDirectory': self.lineEdit_cookieDirectory.text(),'GoogleMeetLink': self.lineEdit_meetingLink.text(),}
        self.configManager.setUserconfig(d)
        self.updateconfig()

    def onReset(self):
        '''
        deletes user config and resets it to default
        '''
        self.configManager.resetConfig()
        self.updateconfig()

        


    def closeEvent(self,event):
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