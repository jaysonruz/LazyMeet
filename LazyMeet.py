##imports
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5 import uic
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
import queue

from threading import Thread , Condition# ---- threading
import time
from backports import configparser
# from concurrent.futures import ThreadPoolExecutor

from configManager import ConfigManager
from googleMeetBot import meet_bot
#----------------------------------------------------------
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi("gui.ui", self)
        #-------------------------------------------------------------------  
        
        self.threadpool = QtCore.QThreadPool()	
        self.threadpool.setMaxThreadCount(1)
        self.q = queue.Queue(maxsize=20)

        #--
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
        self.button_start.clicked.connect(self.start_worker)
        
        self.button_stop = self.findChild(QPushButton,"pushButton_Stop")
        self.button_stop.clicked.connect(self.stop_worker)
        
        self.button_test = self.findChild(QPushButton,"pushButton_TEST")
        self.button_test.clicked.connect(self.test)

        self.worker = None
        self.go_on = False
    ##-----------------------------------------------------------------------------------------------------------
    # def run_io_tasks_in_parallel(self,tasks):
    #     with ThreadPoolExecutor() as executor:
    #         running_tasks = [executor.submit(task) for task in tasks]
    #         for running_task in running_tasks:
    #             running_task.result()

    def guiDisplay(self):
        
        # QtWidgets.QApplication.processEvents()	
 
        y = self.meetingduration
        x = self.timetilmeet
        print(x,y)
        if x < 0 or y < 0 :
            self.timeLabel.setText("Please check if date/time is set correctly.")
            time.sleep(5)  
            self.stop_worker()

        print("starting countdown")#                                                                                 | starts countdown 
        for i in range(x,0,-1):
            if self.go_on:
                self.timeLabel.setText('welcome to LazyMeet')
                break
                                                                                         
            print(i)
            time.sleep(1)
            self.timeLabel.setText("Time Remaining: "+str(i))
            if i < 60: #                                                                                              | about one minute remaining 
                self.timeLabel.setText("Time Remaining: "+str(i)) 
                if i == 1:#                                                                                           |  starts meeting 
                    print("starting meeting")
                    self.timeLabel.setText("starting meeting")

                    #-------------------------------------------------------------------------------------------------|
                    self.obj = meet_bot(cookie_directory= self.cookie_directory,gmeet_link=self.meeting_link)#        | --- selenium starts 
                    self.obj.login()#                                                                                 |
                    #-------------------------------------------------------------------------------------------------|
                    if self.go_on:
                        self.timeLabel.setText('welcome to LazyMeet')
                        break
                    #-------------------------------------------------------------------------------------------------|
                    
                    for j in range(y,0,-1):# 
                        print(j,y/2,j%2)
                        if (self.checkbox1.isChecked() and  (j < y/2)): # if checked and past time it will check if ppl are less then threshold 
                            if j%2 == 0:
                                try :
                                    ppl = self.obj.check_folks_joined()
                                    print(ppl)
                                    if int(ppl) < int(self.spinbox1.value()):
                                        self.stop_worker() 
                                    if j > 20 :
                                        j-=20 
                                except Exception as e:
                                    print("ERROR: ",e)
                                    pass
                            
                            # if int(self.obj.check_folks_joined()) <  int(self.spinbox1.value()):
                            #     print("kam log hai , nikalte hai !")
                            print('its {} checking if number of ppl joined are less then {}'.format(j,self.spinbox1.value()))
                            
                        if self.go_on:
                            self.timeLabel.setText('welcome to LazyMeet')
                            break                                                                            
                        # print("running meeting timer")#                                                              
                        time.sleep(1)#                                                                                
                        self.timeLabel.setText(str(j))#                                                               |--- displays meeting duration and quits on completion 
                        if j == 1:#
                            self.timeLabel.setText('welcome to LazyMeet')
                            print("THE END")                                                                               
                            self.stop_worker()                                                                             
                    #-------------------------------------------------------------------------------------------------|


    def start_worker(self):
        try:
            self.onApply()
        except:
            pass
        self.go_on = False
        self.worker = Worker(self.start_stream, )
        self.threadpool.start(self.worker)

    def stop_worker(self):
        
        self.go_on=True
        with self.q.mutex:
            self.q.queue.clear()

          
        try:
            self.obj.logout()
            
        except Exception as e:
            print("ERROR: ",e)
            pass
        
        

    def start_stream(self):
            
            self.guiDisplay()


    




    #----------------------------------------------------------------------------------------------------------------------    
    def test(self):
        """
        docstring
        """
        close = QMessageBox.information(self,
                                    "hey!",
                                    "are you sure Chrome browser is closed before starting this app?",
                                    QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            
            self.obj = meet_bot(cookie_directory= self.cookie_directory,gmeet_link=self.meeting_link)
            self.obj.login()
            time.sleep(2)
            self.stop_worker()
        else:
            
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
        self.checkbox1 = self.findChild(QCheckBox,"checkBox1")
        self.spinbox1 = self.findChild(QSpinBox,"spinBox1")
        
        print('configs : defining interface succesful')
        #----update interface
        self.lineEdit_cookieDirectory.setText(self.config["UserConfig"]["cookiedirectory"])
        self.lineEdit_meetingLink.setText(self.config["UserConfig"]["googlemeetlink"])
        self.DateEdit.setDate(self.dateToQdate(self.config["UserConfig"]['date']))
        self.timeEdit_Start.setTime(self.timeTOQtime(self.config["UserConfig"]['starttime']))
        self.timeEdit_End.setTime(self.timeTOQtime(self.config["UserConfig"]['endtime']))
        
        if self.config['UserConfig']['minthreshold_ischecked'] == "True":
            self.checkbox1.setChecked(True)
            
        else:
            self.checkbox1.setChecked(False)
        self.spinbox1.setValue(int(self.config['UserConfig']['minthreshold_value']))

        print('configs : updating interface succesful')
        #---update variables 
        self.cookie_directory = self.config["UserConfig"]['cookiedirectory']
        self.meeting_link= self.config["UserConfig"]['googlemeetlink']
        #--update Delta timings
        self.meetingduration = int(self.config["timings"]["meetingduration"])
        self.timetilmeet = int(self.config["timings"]["timetilmeet"])
        self.timeLabel.setText('welcome to LazyMeet')
        
        print('configs : updating variables succesful')
    def onApply(self):
        '''
        creates dictionary of values that user has provided and writes to config file using configmanager
        '''

        d = {'CookieDirectory': self.lineEdit_cookieDirectory.text(),'GoogleMeetLink': self.lineEdit_meetingLink.text(),'Date':self.DateEdit.date().toPyDate(),
            'startTime':self.timeEdit_Start.time().toString(),'endTime':self.timeEdit_End.time().toString(),
            'minThreshold_ischecked': str(self.checkbox1.isChecked()),'minThreshold_value':self.spinbox1.value()}
        
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

class Worker(QtCore.QRunnable):

	def __init__(self, function, *args, **kwargs):
		super(Worker, self).__init__()
		self.function = function
		self.args = args
		self.kwargs = kwargs

	@pyqtSlot()
	def run(self):

		self.function(*self.args, **self.kwargs)	

 
StyleSheet = """
QPushButton{
	background-color: #C1C6DD;
}
QWidget#tab_2{
image: url(lazymeet.ico);
}
QLabel#timelabel{font: 25 14pt "Segoe UI Light";
	background-color: #515570;
    color: #FFD8C9;
}

"""
 
 
 
#-----x----------x-----------x----------
app = QApplication(sys.argv)
app.setStyleSheet(StyleSheet);
app.setWindowIcon(QtGui.QIcon('lazymeet.ico'))
window = MyApp()
window.show()
sys.exit(app.exec_())