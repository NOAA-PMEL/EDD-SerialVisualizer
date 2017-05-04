from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import serial

from serial_receive_widget import SerialReceiveParser
from serial_transmit_widget import SerialTransmitWidget

class SerialRxTxWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super(SerialRxTxWidget,self).__init__(*args,**kwargs)

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
        left.setWindowTitle("Serial Receive")
 
        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)
        right.setWindowTitle("Serial Transmit")
        
        self.rx = SerialReceiveParser()
        #self.rx.setGeometry(0,0,10,10)
        self.tx = SerialTransmitWidget()
        
        #self.tx.setGeometry(0,0,10,10)
        leftLayout.addWidget(self.rx)
        leftLayout.setAlignment(Qt.AlignTop)
        rightLayout.addWidget(self.tx)
        rightLayout.setAlignment(Qt.AlignTop)
        left.setLayout(leftLayout)
        
        left.setMinimumWidth(150)
        right.setLayout(rightLayout)
        

        self.mainSplitter = QSplitter(Qt.Horizontal)
        self.mainSplitter.addWidget(left)
        self.mainSplitter.addWidget(right)

        layout.addWidget(self.mainSplitter)
        
        self.setLayout(layout)
        self.show()





if __name__ == "__main__":            
    class MainWindow(QMainWindow):

        def __init__(self,*args,**kwargs):
            super(MainWindow,self).__init__(*args,**kwargs)

            self.setWindowTitle("Main Test Window")
            layout = QVBoxLayout()
            self.SerialPort = SerialRxTxWidget()

            
            layout.addWidget(self.SerialPort)

            
            widget = QWidget()
            widget.setLayout(layout)

            self.setCentralWidget(widget)
        
            #self.setGeometry(200,200,300,300)



    app = QApplication(sys.argv)

    #window = SensorType()
    window = MainWindow()
    window.show()

