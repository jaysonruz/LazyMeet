from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit ,QMessageBox
from PyQt5 import uic
import sys
from PyQt5.QtCore import QSettings 
 
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi("gui.ui", self)
        #------------------------------------------------------------------------------------
        self.settings = QSettings('LazyMeet','App state')
        
        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
            
        except :
            pass
        # find the widgets in the xml file
 
        # self.textedit = self.findChild(QTextEdit, "textEdit")
        # self.button = self.findChild(QPushButton, "pushButton")
        # self.button.clicked.connect(self.clickedBtn)
        self.button_Apply = self.findChild(QPushButton,"pushButton_Apply")
        self.button_Apply.clicked.connect(self.onApply)
    
    def onApply(self):
        print(self.settings.fileName())
        


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