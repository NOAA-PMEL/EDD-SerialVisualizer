from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import serial


class SerialReceiveParser(QWidget):

    def __init__(self,*args,**kwargs):
        super(SerialReceiveParser,self).__init__(*args,**kwargs)
        titlefont = QFont("Times", 12, QFont.Bold)
        groupfont = QFont("Times", 10, QFont.Bold)

        
        layout = QVBoxLayout()
        delimLayout = QGridLayout()
        termLayout = QGridLayout()
        numberLayout = QGridLayout()
        
        sizePolicy  = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        ## Deliminator Layouts
        self.label = QLabel('Serial Receive')
        self.label.setFont(titlefont)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.label.setGeometry(0,0,20,20)
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
        self.delimCommaBox.setChecked(True)
        self.delimCommaBox.clicked.connect(lambda:self.update_delim('Comma'))
        self.delimSpaceBox = QCheckBox()
        self.delimSpaceBox.clicked.connect(lambda:self.update_delim('Space'))
        self.delimColonBox = QCheckBox()
        self.delimColonBox.clicked.connect(lambda:self.update_delim('Colon'))
        self.delimSemiCBox = QCheckBox()
        self.delimSemiCBox.clicked.connect(lambda:self.update_delim('SemiC'))
        self.delimOtherBox = QCheckBox()
        self.delimOtherBox.clicked.connect(lambda:self.update_delim('Other'))
        self.delimOtherLine = QLineEdit()

        
        ## Terminator Layouts
        self.termLabel = QLabel('Line Termination')
        self.termLabel.setFont(groupfont)
        self.termCr = QLabel('<CR> (\\r)')
        self.termCrLf = QLabel('<CR><LF> (\\r\\n)')
        self.termLf = QLabel('<LF> (\\n)')
        self.termEOT = QLabel('<EOT> (0x04)')
        self.termOther = QLabel('Other')

        self.termLabelBox = QCheckBox()
        self.termCrBox = QCheckBox()
        self.termCrBox.clicked.connect(lambda:self.update_term('CR'))
        self.termCrLfBox = QCheckBox()
        self.termCrLfBox.clicked.connect(lambda:self.update_term('CRLF'))
        self.termCrLfBox.setChecked(True)
        self.termLfBox = QCheckBox()
        self.termLfBox.clicked.connect(lambda:self.update_term('LF'))
        self.termEOTBox = QCheckBox()
        self.termEOTBox.clicked.connect(lambda:self.update_term('EOT'))
        self.termOtherBox = QCheckBox()
        self.termOtherBox.clicked.connect(lambda:self.update_term('Other'))
        self.termOtherLine = QLineEdit()

        ## Number Layout
        self.numLabel = QLabel('Number of Data Fields')
        self.numLabel.setFont(groupfont)

        self.numValues = QLabel('#Data in Rx')
        self.numValuesBox = QSpinBox()
        self.numValuesBox.setMinimum(1)
        self.numValuesBox.setMaximum(8)
        self.numValuesBox.setValue(8)

        
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
        layout.addWidget(self.label)
        layout.addWidget(self.delimLabel)
        layout.addLayout(delimLayout)
        layout.addWidget(self.termLabel)
        layout.addLayout(termLayout)
        layout.addWidget(self.numLabel)
        layout.addLayout(numberLayout)
        
        self.setLayout(layout)
        self.show()
        #self.setMinimumWidth(300)
        
    def delim_state_changed(self,int):
        pass
        
    def parse_string(self,string):
        term = []
        substring = []
        #print(string)
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
        #print("Substring=")
        #print(substring)
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

        #print(delim)
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
            if(len(temp) == (self.numValuesBox.value())):
                for t in temp:
                    #print(t)
                    if(t == ''):
                        pass
                    else:
                        subdata.append(float(t))

                data.append(subdata)
            #print(subdata)
        ## Return the data if valid
        return data


    
    def update_delim(self,value):
        #print("Here Value = ")
        #print(value)
        if(value == 'Comma'):
            self.delimSpaceBox.setCheckState(False)
            self.delimColonBox.setCheckState(False)
            self.delimSemiCBox.setCheckState(False)
            self.delimOtherBox.setCheckState(False)
        elif(value == 'Space'):
            self.delimCommaBox.setCheckState(False)
            self.delimColonBox.setCheckState(False)
            self.delimSemiCBox.setCheckState(False)
            self.delimOtherBox.setCheckState(False)
        elif(value == 'Colon'):
            self.delimSpaceBox.setCheckState(False)
            self.delimCommaBox.setCheckState(False)
            self.delimSemiCBox.setCheckState(False)
            self.delimOtherBox.setCheckState(False)
        elif(value == 'SemiC'):
            self.delimSpaceBox.setCheckState(False)
            self.delimColonBox.setCheckState(False)
            self.delimCommaBox.setCheckState(False)
            self.delimOtherBox.setCheckState(False)
        elif(value == 'Other'):
            self.delimSpaceBox.setCheckState(False)
            self.delimColonBox.setCheckState(False)
            self.delimSemiCBox.setCheckState(False)
            self.delimCommaBox.setCheckState(False)
            
        return

    def update_term(self,value):
        if(value == 'CR'):
            self.termCrLfBox.setCheckState(False)
            self.termLfBox.setCheckState(False)
            self.termEOTBox.setCheckState(False)
            self.termOtherBox.setCheckState(False)
        elif(value == 'LF'):
            self.termCrBox.setCheckState(False)
            self.termCrLfBox.setCheckState(False)
            self.termEOTBox.setCheckState(False)
            self.termOtherBox.setCheckState(False)
        elif(value == 'CRLF'):
            self.termCrBox.setCheckState(False)
            self.termLfBox.setCheckState(False)
            self.termEOTBox.setCheckState(False)
            self.termOtherBox.setCheckState(False)
        elif(value == 'EOT'):
            self.termCrBox.setCheckState(False)
            self.termCrLfBox.setCheckState(False)
            self.termLfBox.setCheckState(False)
            self.termOtherBox.setCheckState(False)
        elif(value == 'Other'):
            self.termCrBox.setCheckState(False)
            self.termCrLfBox.setCheckState(False)
            self.termLfBox.setCheckState(False)
            self.termEOTBox.setCheckState(False)

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


    
   
