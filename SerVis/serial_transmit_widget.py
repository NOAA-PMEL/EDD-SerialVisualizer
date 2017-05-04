from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import serial



class SerialTransmitWidget(QWidget):

    

    def __init__(self,*args,**kwargs):
        super(SerialTransmitWidget,self).__init__(*args,**kwargs)
        titlefont = QFont("Times", 12, QFont.Bold)
        
        #layout = QGridLayout()
        layout = QVBoxLayout()
        gridlayout = QGridLayout()

        sizePolicy  = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
  


##        verticalLine = QFrame()
##        verticalLine.setFrameStyle(QFrame.VLine)
##        verticalLine.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
##
##        horizontalLine = QFrame()
##        horizontalLine.setFrameStyle(QFrame.HLine)
##        horizontalLine.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
##
##        horizontalLine2 = QFrame()
##        horizontalLine2.setFrameStyle(QFrame.HLine)
##        horizontalLine2.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

        
        #left = QFrame(self)
        #left.setFrameShape(QFrame.StyledPanel)
        #left.setWindowTitle("Serial Traffic")
 
        #right = QFrame(self)
        #right.setSizePolicy(sizePolicy)
        #right.setFrameShape(QFrame.StyledPanel)

        ## Create the Widgets
        self.label = QLabel('Serial Transmit')
        self.label.setFont(titlefont)
        self.label.setMaximumHeight(24)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        #self.label.setGeometry(0,0,20,20)
        
##        self.consoleLabel = QLabel('Console')
##        self.consoleLabel.setMaximumHeight(20)
##        self.consoleLabel.setAlignment(Qt.AlignLeft |Qt.AlignTop)
##        self.console = QLabel('Waiting...')
##        self.commands = QLabel('Commands')

        self.sendmsgLabel = QLabel('Send Message')
        self.sendmsgLabel.setAlignment(Qt.AlignLeft |Qt.AlignTop)
        self.sendmsgText = QLineEdit('Enter text here...')
        self.sendmsgText.setMinimumWidth(150)
        self.sendmsgButton = QPushButton('Send')
        
        self.crLabel = QLabel('Carriage Return (\\n)?')
        self.crBox = QCheckBox()
        
        self.nlLabel = QLabel('New Line (\\n)?')
        self.nlBox = QCheckBox()
        
        self.repeatLabel = QLabel('Repeat?')
        self.repeatBox = QCheckBox()
        self.repeatNumLabel = QLabel('Num. Repeats')
        self.repeatNumBox = QSpinBox()
        self.repeatNumBox.setMinimum(0)
        self.repeatNumBox.setMaximum(1000)
        self.repeatNumBox.setMinimumWidth(50)
        self.repeatNumBox.setMaximumWidth(75)
        self.repeatNumLabel2 = QLabel('0 = Forever')
        
        self.timeRepeatLabel = QLabel('Time between repeats')
        self.timeRepeatBox = QSpinBox()
        self.timeRepeatLabel2 = QLabel('(ms)')
        self.timeRepeatBox.setMaximumWidth(50)
        self.timeRepeatBox.setMinimum(1)
        self.timeRepeatBox.setMaximum(5000)
        self.timeRepeatBox.setMaximumWidth(75)


                
     

        #layout.addWidget(self.commands)
        layout.addWidget(self.label)
##        layout.addWidget(self.sendmsgLabel,1,0)
##        layout.addWidget(self.sendmsgText,1,1)
##        layout.addWidget(self.sendmsgButton,1,2)
##        layout.addWidget(self.crLabel,2,0)
##        layout.addWidget(self.crBox,2,1)
##        layout.addWidget(self.nlLabel,3,0)
##        layout.addWidget(self.nlBox,3,1)
##        layout.addWidget(self.repeatLabel,4,0)
##        layout.addWidget(self.repeatBox,4,1)
##        layout.addWidget(self.repeatNumLabel,5,0)
##        layout.addWidget(self.repeatNumBox,5,1)
##        layout.addWidget(self.repeatNumLabel2,5,2)
##        layout.addWidget(self.timeRepeatLabel,6,0)
##        layout.addWidget(self.timeRepeatBox,6,1)
##        layout.addWidget(self.timeRepeatLabel2,6,2)
        

        gridlayout.addWidget(self.sendmsgLabel,1,0)
        gridlayout.addWidget(self.sendmsgText,1,1)
        gridlayout.addWidget(self.sendmsgButton,1,2)
        gridlayout.addWidget(self.crLabel,2,0)
        gridlayout.addWidget(self.crBox,2,1)
        gridlayout.addWidget(self.nlLabel,3,0)
        gridlayout.addWidget(self.nlBox,3,1)
        gridlayout.addWidget(self.repeatLabel,4,0)
        gridlayout.addWidget(self.repeatBox,4,1)
        gridlayout.addWidget(self.repeatNumLabel,5,0)
        gridlayout.addWidget(self.repeatNumBox,5,1)
        gridlayout.addWidget(self.repeatNumLabel2,5,2)
        gridlayout.addWidget(self.timeRepeatLabel,6,0)
        gridlayout.addWidget(self.timeRepeatBox,6,1)
        gridlayout.addWidget(self.timeRepeatLabel2,6,2)

        #gridlayout.setMinimumHeight(250)
        
        layout.addLayout(gridlayout)


        
        self.setLayout(layout)

        self.show()
        #self.resize(QSizePolicy.Minimum)
        self.setMinimumWidth(300)
        
    def send_btn_clicked(self):
        pass
            
    
    def set_timer(self):
        timer = QTimer(self)
        #timer.timeout.connect(self.update_serial_buffer)
        timer.start(250)



if __name__ == "__main__":            
    class MainWindow(QMainWindow):

        def __init__(self,*args,**kwargs):
            super(MainWindow,self).__init__(*args,**kwargs)

            self.setWindowTitle("Main Test Window")
            layout = QVBoxLayout()
            self.SerialPort = SerialTransmitWidget()

            
            layout.addWidget(self.SerialPort)

            
            widget = QWidget()
            widget.setLayout(layout)

            self.setCentralWidget(widget)
        
            self.setGeometry(100,100,100,100)


            self.SerialPort.set_timer()

    app = QApplication(sys.argv)

    #window = SensorType()
    window = MainWindow()
    window.show()


    app.exec_()
