from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import serial



class SerialConsoleWidget(QWidget):

    

    def __init__(self,*args,**kwargs):
        super(SerialConsoleWidget,self).__init__(*args,**kwargs)

        self.consoleString = []
        
        layout = QHBoxLayout()


        ## Create the Widgets
        self.consoleLabel = QLabel('Console')
        self.consoleLabel.setMaximumHeight(20)
        self.consoleLabel.setAlignment(Qt.AlignLeft |Qt.AlignTop)
        self.console = QLabel('Waiting...')
        self.commands = QLabel('Commands')

        layout.addWidget(self.consoleLabel)
        
        self.setLayout(layout)

        self.show()
        self.setMinimumWidth(600)
        
    def send_btn_clicked(self):
        pass
            
    
    def set_timer(self):
        timer = QTimer(self)
        #timer.timeout.connect(self.update_serial_buffer)
        timer.start(250)

    def add_string(self,string):
        self.consoleString.append(string)



if __name__ == "__main__":            
    class MainWindow(QMainWindow):

        def __init__(self,*args,**kwargs):
            super(MainWindow,self).__init__(*args,**kwargs)

            self.setWindowTitle("Main Test Window")
            layout = QVBoxLayout()
            self.SerialPort = SerialConsoleWidget()

            
            layout.addWidget(self.SerialPort)

            
            widget = QWidget()
            widget.setLayout(layout)

            self.setCentralWidget(widget)
        
            self.setGeometry(200,200,300,300)


            self.SerialPort.set_timer()

    app = QApplication(sys.argv)

    #window = SensorType()
    window = MainWindow()
    window.show()


    app.exec_()
