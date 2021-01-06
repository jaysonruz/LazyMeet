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

from configManager import ConfigManager
from googleMeetBot import meet_bot
#----------------------------------------------------------
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi("gui.ui", self)
        #--------------------------------------------------
        self.threadpool = QtCore.QThreadPool()	
        self.threadpool.setMaxThreadCount(1)
        self.q = queue.Queue(maxsize=20)
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
        
        ######################
        #linking all Buttons #
        ######################

        self.button_create_cookies = self.findChild(QPushButton,"pushButton_create_cookies")# Create cookie Button
        self.button_create_cookies.clicked.connect(self.CreateCookie)

        self.button_Apply = self.findChild(QPushButton,"pushButton_Apply") # Apply Button
        self.button_Apply.clicked.connect(self.onApply)
        self.button_reset = self.findChild(QPushButton,"pushButton_Reset") # Reset Button
        self.button_reset.clicked.connect(self.onReset)


        self.button_start = self.findChild(QPushButton,"pushButton_Start") # Start Button
        self.button_start.clicked.connect(self.start_worker)
        
        self.button_stop = self.findChild(QPushButton,"pushButton_Stop")  # Stop Button
        self.button_stop.clicked.connect(self.stop_worker)
        
        self.button_test = self.findChild(QPushButton,"pushButton_TEST")  # test Button
        self.button_test.clicked.connect(self.test)
        ## setting icon to the button 
        # self.button_test.setIcon(QIcon('warning.png')) 
        self.worker = None #-|custom flags
        self.go_on = False #-|custom flags


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
                    self.obj = meet_bot(gmeet_link=self.meeting_link)#        | --- selenium starts 
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
                                    print(ppl) # number of ppl in meeting atm
                                    if int(ppl) < int(self.spinbox1.value()):
                                        self.timeLabel.setText('Stopping Meeting ! {folks < MinTh} ')
                                        self.stop_worker() 
                                    # if j > 20 :
                                    #     j-=20 
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
                        self.timeLabel.setText("Meeting duration :"+str(j))#                                                               |--- displays meeting duration and quits on completion 
                        if j == 1:#
                            self.timeLabel.setText('welcome to LazyMeet')
                            print("THE END")                                                                               
                            self.stop_worker()                                                                             
                    #-------------------------------------------------------------------------------------------------|

   #Multithreading at play 
    #start button function
    def start_worker(self):
        try:
            self.onApply()
        except:
            pass
        self.go_on = False
        self.worker = Worker(self.start_stream, )
        self.threadpool.start(self.worker)
    #stop button function
    def stop_worker(self):
        self.go_on=True
        with self.q.mutex:
            self.q.queue.clear()  
        try:
            self.obj.logout() 
        except :
            pass
        
    def start_stream(self):
            self.guiDisplay()
    #--------------------------

    #----------------------------------------------------------------------------------------------------------------------    
    def test(self):
        """
        Test button implementation
        """
        close = QMessageBox.information(self,
                                    "hey!",
                                    "note: please allow mic and video if notification pops up on meeting screen."
                                    " \n   have you set cookies? ",
                                    QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            
            self.obj = meet_bot(gmeet_link=self.meeting_link)
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
        self.lineEdit_meetingLink = self.findChild(QLineEdit,"lineEdit_meetingLink")
        self.DateEdit = self.findChild(QDateEdit,"dateEdit")
        self.timeEdit_Start = self.findChild(QTimeEdit,"timeEdit_Start")
        self.timeEdit_End = self.findChild(QTimeEdit,"timeEdit_End")
        self.checkbox1 = self.findChild(QCheckBox,"checkBox1")
        self.spinbox1 = self.findChild(QSpinBox,"spinBox1")
        
        print('configs : defining interface succesful')
        #----update interface
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
        self.meeting_link= self.config["UserConfig"]['googlemeetlink']
        #--update Delta timings
        self.meetingduration = int(self.config["timings"]["meetingduration"])
        self.timetilmeet = int(self.config["timings"]["timetilmeet"])
        self.timeLabel.setText('welcome to LazyMeet')
        
        print('configs : updating variables succesful')
        #-----------------------------------------------
    def CreateCookie(self):
        '''
        cookie button function is implemeted here 
        '''
        self.obj = meet_bot(gmeet_link=self.meeting_link)#        | --- selenium starts 
        self.obj.cookiecreator()#    
                                             
        

    def onApply(self):
        '''
        creates dictionary of values that user has provided and writes to config file using configmanager
        '''

        d = {'GoogleMeetLink': self.lineEdit_meetingLink.text(),'Date':self.DateEdit.date().toPyDate(),
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