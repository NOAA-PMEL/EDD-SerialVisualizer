from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import serial



class SerialConsoleWidget(QWidget):

    

    def __init__(self,*args,**kwargs):
        super(SerialConsoleWidget,self).__init__(*args,**kwargs)

        layout = QHBoxLayout()

        sizePolicy  = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        leftLayout = QVBoxLayout()
        rightLayout = QGridLayout()

        verticalLine = QFrame()
        verticalLine.setFrameStyle(QFrame.VLine)
        verticalLine.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

        horizontalLine = QFrame()
        horizontalLine.setFrameStyle(QFrame.HLine)
        horizontalLine.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

        horizontalLine2 = QFrame()
        horizontalLine2.setFrameStyle(QFrame.HLine)
        horizontalLine2.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

        
        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)
        left.setWindowTitle("Serial Traffic")
 
        right = QFrame(self)
        #right.setSizePolicy(sizePolicy)
        right.setFrameShape(QFrame.StyledPanel)

        ## Create the Widgets
        self.consoleLabel = QLabel('Console')
        self.consoleLabel.setMaximumHeight(20)
        self.consoleLabel.setAlignment(Qt.AlignLeft |Qt.AlignTop)
        self.console = QLabel('Waiting...')
        self.commands = QLabel('Commands')

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


                
        leftLayout.addWidget(self.console)
        left.setLayout(leftLayout)
        left.setMinimumWidth(150)

        #rightLayout.addWidget(self.commands)
        rightLayout.addWidget(self.sendmsgLabel,0,0)
        rightLayout.addWidget(self.sendmsgText,0,1)
        rightLayout.addWidget(self.sendmsgButton,0,2)
        rightLayout.addWidget(self.crLabel,1,0)
        rightLayout.addWidget(self.crBox,1,1)
        rightLayout.addWidget(self.nlLabel,2,0)
        rightLayout.addWidget(self.nlBox,2,1)
        rightLayout.addWidget(self.repeatLabel,3,0)
        rightLayout.addWidget(self.repeatBox,3,1)
        rightLayout.addWidget(self.repeatNumLabel,4,0)
        rightLayout.addWidget(self.repeatNumBox,4,1)
        rightLayout.addWidget(self.repeatNumLabel2,4,2)
        rightLayout.addWidget(self.timeRepeatLabel,5,0)
        rightLayout.addWidget(self.timeRepeatBox,5,1)
        rightLayout.addWidget(self.timeRepeatLabel2,5,2)
        

        right.setLayout(rightLayout)

        
        self.mainSplitter = QSplitter(Qt.Horizontal)
        self.mainSplitter.addWidget(left)
        self.mainSplitter.addWidget(right)

        layout.addWidget(self.mainSplitter)
        
        self.setLayout(layout)

        self.show()
        #self.resize(QSizePolicy.Minimum)
        self.setMinimumWidth(600)
        
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
