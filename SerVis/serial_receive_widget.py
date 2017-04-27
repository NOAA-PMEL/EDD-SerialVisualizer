from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import serial


class SerialReceiveParser(QWidget):

    def __init__(self,*args,**kwargs):
        super(SerialReceiveParser,self).__init__(*args,**kwargs)
        
        groupfont = QFont("Times", 12, QFont.Bold)

        
        layout = QVBoxLayout()
        delimLayout = QGridLayout()
        termLayout = QGridLayout()
        numberLayout = QGridLayout()
        


        ## Deliminator Layouts
        self.delimLabel = QLabel('Delimiter')
        self.delimLabel.setFont(groupfont)
        self.delimLabel.setAlignment(Qt.AlignLeft)
        self.delimComma = QLabel('Comma (,)')
        self.delimComma.setAlignment(Qt.AlignLeft)
        self.delimSpace = QLabel('Space ( )')
        self.delimSpace.setAlignment(Qt.AlignLeft)
        self.delimColon = QLabel('Colon (:)')
        self.delimColon.setAlignment(Qt.AlignLeft)
        self.delimSemiC = QLabel('Semicolon (;)')
        self.delimSemiC.setAlignment(Qt.AlignLeft)
        self.delimOther = QLabel('Other')
        self.delimOther.setAlignment(Qt.AlignLeft)

        self.delimCommaBox = QCheckBox()
        self.delimSpaceBox = QCheckBox()
        self.delimColonBox = QCheckBox()
        self.delimSemiCBox = QCheckBox()
        self.delimOtherBox = QCheckBox()
        self.delimOtherLine = QLineEdit()

        
        ## Terminator Layouts
        self.termLabel = QLabel('Line Termination')
        self.termLabel.setFont(groupfont)
        self.termCr = QLabel('\\r')
        self.termCrLf = QLabel('\\r\\n')
        self.termLf = QLabel('\\n')
        self.termEOT = QLabel('EOT (0x04)')
        self.termOther = QLabel('Other')

        self.termLabelBox = QCheckBox()
        self.termCrBox = QCheckBox()
        self.termCrLfBox = QCheckBox()
        self.termLfBox = QCheckBox()
        self.termEOTBox = QCheckBox()
        self.termOtherBox = QCheckBox()
        self.termOtherLine = QLineEdit()

        ## Number Layout
        self.numLabel = QLabel('Number of Data Fields')
        self.numLabel.setFont(groupfont)

        self.numValues = QLabel('#Data in Rx')
        self.numValuesBox = QSpinBox()
        self.numValuesBox.setMinimum(1)
        self.numValuesBox.setMaximum(8)
        

        
        #delimLayout.addWidget(self.delimLabel,0,0,4,0)
        delimLayout.addWidget(self.delimComma,1,1)
        delimLayout.addWidget(self.delimCommaBox,1,0)
        delimLayout.addWidget(self.delimSpace,1,3)
        delimLayout.addWidget(self.delimSpaceBox,1,2)
        delimLayout.addWidget(self.delimColon,2,1)
        delimLayout.addWidget(self.delimColonBox,2,0)
        delimLayout.addWidget(self.delimSemiC,2,3)
        delimLayout.addWidget(self.delimSemiCBox,2,2)
        delimLayout.addWidget(self.delimOtherBox,3,0)
        delimLayout.addWidget(self.delimOther,3,1)
        delimLayout.addWidget(self.delimOtherLine,3,2,1,2)

        #termLayout.addWidget(self.termLabel,4,0)
        termLayout.addWidget(self.termCr,5,1)
        termLayout.addWidget(self.termCrBox,5,0)
        termLayout.addWidget(self.termLf,5,3)
        termLayout.addWidget(self.termLfBox,5,2)
        termLayout.addWidget(self.termCrLf,6,1)
        termLayout.addWidget(self.termCrLfBox,6,0)
        termLayout.addWidget(self.termEOT,6,3)
        termLayout.addWidget(self.termEOTBox,6,2)
        termLayout.addWidget(self.termOther,7,1)
        termLayout.addWidget(self.termOtherBox,7,0)
        termLayout.addWidget(self.termOtherLine,7,2,1,2)

        ## Number layout
        numberLayout.addWidget(self.numValues,0,0)
        numberLayout.addWidget(self.numValuesBox,0,1)

        #.setColumnMinimumWidth(0,5)
        layout.addWidget(self.delimLabel)
        layout.addLayout(delimLayout)
        layout.addWidget(self.termLabel)
        layout.addLayout(termLayout)
        layout.addWidget(self.numLabel)
        layout.addLayout(numberLayout)
        
        self.setLayout(layout)
        self.show()

    def delim_state_changed(self,int):
        pass
        
    def parse_string(self,string):
        term = []
        substring = []
        # Determin delimiter
        if(self.termCrBox.isChecked()==True):
            term = '\r'
        elif(self.termLfBox.isChecked()==True):
            term = '\n'
        elif(self.termCrLfBox.isChecked()==True):
            term = '\r\n'
        elif(self.termEOTBox.isChecked()==True):
            term = hex(0x04)
        elif(self.termOtherBox.isChecked()==True):
            term = self.termOtherLine.text()

        # Determine the substring
        substring = string.split(term)
        data = []

        if(self.delimCommaBox.isChecked() == True):
            delim = ','
        elif(self.delimSpaceBox.isChecked()==True):
            delim = ' ' 
        elif(self.delimColonBox.isChecked()==True):
            delim = ':'
        elif(self.delimSemiCBox.isChecked()==True):
            delim = ';'
        elif(self.delimOtherBox.isChecked()==True):
            delim = self.delimOtherLine.text()
            
        ## Split the substring and create a multidimensional list of floats
        idx = 0
        for subs in substring:
            #print(subs)
            if(subs == ''):
                break;
            #print(delim)
            temp = subs.split(delim)
            subdata = []
            #print(len(temp))
            if(len(temp) == (self.numValuesBox.value()+1)):
                for t in temp:
                    #print(t)
                    if(t == ''):
                        pass
                    else:
                        subdata.append(float(t))

                data.append(subdata)

        ## Return the data if valid
        return data


if __name__ == "__main__":            
    class MainWindow(QMainWindow):

        def __init__(self,*args,**kwargs):
            super(MainWindow,self).__init__(*args,**kwargs)

            self.setWindowTitle("Main Test Window")
            layout = QVBoxLayout()
            self.SerialPort = SerialReceiveParser()

            
            layout.addWidget(self.SerialPort)

            
            widget = QWidget()
            widget.setLayout(layout)

            self.setCentralWidget(widget)
        
            #self.setGeometry(200,200,300,300)



    app = QApplication(sys.argv)

    #window = SensorType()
    window = MainWindow()
    window.show()


    app.exec_()


    
   
