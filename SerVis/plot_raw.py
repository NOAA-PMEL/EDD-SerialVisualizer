# -*- coding: utf-8 -*-
"""
This program is a GUI for the PMEL Eppley Radiation Sensors (LW and SW).

"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.Point import Point
from pyqtgraph.dockarea import *
import pyqtgraph.console

import sys
import time

import numpy as np


class RawPlotWidget(QtGui.QWidget):

    def __init__(self,*args,**kwargs):
        super(RawPlotWidget, self).__init__(*args,**kwargs)

        self.d0 = []
        self.d1 = []
        self.d2 = []
        self.d3 = []
        self.d4 = []
        self.d5 = []
        self.d6 = []
        self.d7 = []
        
        self.countData = []
        self.x = []
        self.count = 0
        ## Setup the layout
        layout = QtGui.QVBoxLayout()
        cbLayout = QtGui.QGridLayout()
        vbox = QtGui.QVBoxLayout()
 
        ## Create the first plot (Thermocouples)
        self.win1 = pg.GraphicsWindow()
        self.win1.setWindowTitle("Raw Thermopile Counts")
        self.plt1 = self.win1.addPlot()
        self.plt1.addLegend()
        self.curve0 = self.plt1.plot(pen=(255,0,0),name=('D0'))
        self.curve1 = self.plt1.plot(pen=(0,255,0),name=('D1'))
        self.curve2 = self.plt1.plot(pen=(0,0,255),name=('D2'))
        self.curve3 = self.plt1.plot(pen=(0,127,127),name=('D3'))
        self.curve4 = self.plt1.plot(pen=(127,127,0),name=('D4'))
        self.curve5 = self.plt1.plot(pen=(127,0,127),name=('D5'))
        self.curve6 = self.plt1.plot(pen=(200,100,0),name=('D6'))
        self.curve7 = self.plt1.plot(pen=(0,200,100),name=('D7'))
        
        self.plt1.setLabel('left',"",units='Counts')

        self.d0_en = QtGui.QCheckBox()
        self.d0_en.setChecked(True)
        self.d0_en.clicked.connect(lambda:self.update_check('D0'))
        self.d0_lbl = QtGui.QLabel('D0')
        self.d0_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.d0_val = QtGui.QLCDNumber()
        self.d0_val.setSegmentStyle(QtGui.QLCDNumber.Flat)
        
        self.d1_en = QtGui.QCheckBox()
        self.d1_en.setChecked(True)
        self.d1_lbl = QtGui.QLabel('D1')
        self.d1_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.d1_val = QtGui.QLCDNumber()
        self.d1_val.setSegmentStyle(QtGui.QLCDNumber.Flat)
        
        self.d2_en = QtGui.QCheckBox()
        self.d2_en.setChecked(True)
        self.d2_lbl = QtGui.QLabel('D2')
        self.d2_val = QtGui.QLCDNumber()
        self.d2_val.setSegmentStyle(QtGui.QLCDNumber.Flat)
        
        self.d3_en = QtGui.QCheckBox()
        self.d3_en.setChecked(True)
        self.d3_lbl = QtGui.QLabel('D3')
        self.d3_val = QtGui.QLCDNumber()
        self.d3_val.setSegmentStyle(QtGui.QLCDNumber.Flat)
        
        self.d4_en = QtGui.QCheckBox()
        self.d4_en.setChecked(True)
        self.d4_lbl = QtGui.QLabel('D4')
        self.d4_val = QtGui.QLCDNumber()
        self.d4_val.setSegmentStyle(QtGui.QLCDNumber.Flat)
        
        self.d5_en = QtGui.QCheckBox()
        self.d5_en.setChecked(True)
        self.d5_lbl = QtGui.QLabel('D5')
        self.d5_val = QtGui.QLCDNumber()
        self.d5_val.setSegmentStyle(QtGui.QLCDNumber.Flat)
        
        self.d6_en = QtGui.QCheckBox()
        self.d6_en.setChecked(True)
        self.d6_lbl = QtGui.QLabel('D6')
        self.d6_val = QtGui.QLCDNumber()
        self.d6_val.setSegmentStyle(QtGui.QLCDNumber.Flat)
        
        self.d7_en = QtGui.QCheckBox()
        self.d7_en.setChecked(True)
        self.d7_lbl = QtGui.QLabel('D7')
        self.d7_val = QtGui.QLCDNumber()
        self.d7_val.setSegmentStyle(QtGui.QLCDNumber.Flat)
        
        cbLayout.addWidget(self.d0_en,0,0,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d1_en,0,1,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d2_en,0,2,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d3_en,0,3,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d4_en,0,4,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d5_en,0,5,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d6_en,0,6,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d7_en,0,7,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d0_lbl,1,0,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d1_lbl,1,1,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d2_lbl,1,2,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d3_lbl,1,3,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d4_lbl,1,4,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d5_lbl,1,5,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d6_lbl,1,6,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d7_lbl,1,7,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d0_val,2,0,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d1_val,2,1,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d2_val,2,2,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d3_val,2,3,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d4_val,2,4,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d5_val,2,5,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d6_val,2,6,QtCore.Qt.AlignCenter)
        cbLayout.addWidget(self.d7_val,2,7,QtCore.Qt.AlignCenter)
        ## Set up the layout
        vbox.addWidget(self.win1)

        layout.addLayout(vbox)
        layout.addLayout(cbLayout);

        self.setLayout(layout)
        self.setMinimumWidth(250)
        self.setMinimumHeight(250)
        self.show()

    def addData(self,d0,d1,d2,d3,d4,d5,d6,d7):
        if(len(self.d0)>=100):
            self.x.pop(0)
            self.d0.pop(0)
            self.d1.pop(0)
            self.d2.pop(0)
            self.d3.pop(0)
            self.d4.pop(0)
            self.d5.pop(0)
            self.d6.pop(0)
            self.d7.pop(0)

        self.count += 1
        self.x.append(np.array([self.count]))
        
        self.d0.append(np.array([d0]))
        self.d1.append(np.array([d1]))
        self.d2.append(np.array([d2]))
        self.d3.append(np.array([d3]))
        self.d4.append(np.array([d4]))
        self.d5.append(np.array([d5]))
        self.d6.append(np.array([d6]))
        self.d7.append(np.array([d7]))
 
        
        self.curve0.setData(np.hstack(self.x),np.hstack(self.d0))
        self.curve1.setData(np.hstack(self.x),np.hstack(self.d1))
        self.curve2.setData(np.hstack(self.x),np.hstack(self.d2))
        self.curve3.setData(np.hstack(self.x),np.hstack(self.d3))
        self.curve4.setData(np.hstack(self.x),np.hstack(self.d4))
        self.curve5.setData(np.hstack(self.x),np.hstack(self.d5))
        self.curve6.setData(np.hstack(self.x),np.hstack(self.d6))
        self.curve7.setData(np.hstack(self.x),np.hstack(self.d7))
        
        self.plt1.setXRange(min=self.count-100,max=self.count)

    def addArray(self,d0):
        #print("Array")
        #print(d0)
        if(len(self.d0)>=100):
            self.x.pop(0)
            self.d0.pop(0)
            self.d1.pop(0)
            self.d2.pop(0)
            self.d3.pop(0)
            self.d4.pop(0)
            self.d5.pop(0)
            self.d6.pop(0)
            self.d7.pop(0)

        self.count += 1
        
        ##Append the values to the respective arrays
        self.x.append(np.array([self.count]))
        
        
        temp = np.array([])
        for i in range(0,len(self.x)):
            temp = np.append(temp,[np.nan])

       
        try:
            self.d0.append(np.array([d0[0]]))
            num = u'%8.2f' % d0[0]
            self.d0_val.display(d0[0])
            if(self.d0_en.isChecked()):
                self.curve0.setData(np.hstack(self.x),np.hstack(self.d0))
            else:
                self.curve0.setData(np.hstack(self.x),temp)
                
        except:
            print("Failed in false")
            pass
        
        try:
            self.d1.append(np.array([d0[1]]))
            #num = u'%6.2f' % d0[1]
            self.d1_val.display(d0[1])
            if self.d1_en.isChecked() == True:
                self.curve1.setData(np.hstack(self.x),np.hstack(self.d1))
            else:
                self.curve1.setData(np.hstack(self.x),temp)

        except:
            pass

        try:
            self.d2.append(np.array([d0[2]]))
            #num = u'%.2f' % d0[2]
            self.d2_val.display(d0[2])
            if self.d2_en.isChecked() == True:
                
                self.curve2.setData(np.hstack(self.x),np.hstack(self.d2))
            else:
                self.curve2.setData(np.hstack(self.x),temp)
        except:
            pass

        try:
            self.d3.append(np.array([d0[3]]))
            #num = u'%.2f' % d0[3]
            self.d3_val.display(d0[3])
            if self.d3_en.isChecked() == True:
                
                self.curve3.setData(np.hstack(self.x),np.hstack(self.d3))
            else:
                self.curve3.setData(np.hstack(self.x),temp)
        except:
            pass

        try:
            self.d4.append(np.array([d0[4]]))
            #num = u'%.2f' % d0[4]
            self.d4_val.display(d0[4])
            if self.d4_en.isChecked() == True:
                
                self.curve4.setData(np.hstack(self.x),np.hstack(self.d4))
            else:
                self.curve4.setData(np.hstack(self.x),temp)
        except:
            pass

        try:
            self.d5.append(np.array([d0[5]]))
            #num = u'%.2f' % d0[5]
            self.d5_val.display(d0[5])
            if self.d5_en.isChecked() == True:
                
                self.curve5.setData(np.hstack(self.x),np.hstack(self.d5))
            else:
                self.curve5.setData(np.hstack(self.x),temp)
        except:
            pass

        try:
            self.d6.append(np.array([d0[6]]))
            #num = u'%.2f' % d0[6]
            self.d6_val.display(d0[6])
            if self.d6_en.isChecked() == True:
                
                self.curve6.setData(np.hstack(self.x),np.hstack(self.d6))
            else:
                self.curve6.setData(np.hstack(self.x),temp)
        except:
            pass

        try:
            self.d7.append(np.array([d0[7]]))
            #num = u'%.2f' % d0[7]
            self.d7_val.display(d0[7])
            if self.d7_en.isChecked() == True:
                
                self.curve7.setData(np.hstack(self.x),np.hstack(self.d7))
            else:
                self.curve7.setData(np.hstack(self.x),temp)
        except:
            pass
        #print("append=")
        #print(self.d0)

                
        
        
        
       
        
        
        
        
        
        self.plt1.setXRange(min=self.count-100,max=self.count)

    def update_check(self, value):
        pass
##        if(value == 'D0'):
##            for i in range(0,len(self.d0)):
##                self.d0[i] = np.NAN
##                pass
##        elif(value == 'D1'):
##            for i in range(0,len(self.d1)):
##                self.d1[i] = np.NAN
##        elif(value == 'D2'):
##            for i in range(0,len(self.d2)):
##                self.d2[i] = np.NAN
##        elif(value == 'D3'):
##            for i in range(0,len(self.d3)):
##                self.d3[i] = np.NAN
##        elif(value == 'D4'):
##            for i in range(0,len(self.d4)):
##                self.d4[i] = np.NAN
##        elif(value == 'D5'):
##            for i in range(0,len(self.d5)):
##                self.d5[i] = np.NAN
##        elif(value == 'D6'):
##            for i in range(0,len(self.d6)):
##                self.d6[i] = np.NAN
##        elif(value == 'D7'):
##            for i in range(0,len(self.d7)):
##                self.d7[i] = np.NAN

        return;
    def addTimer(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.fake_data)
        timer.start(100)

    def fake_data(self):
        val = float(np.random.normal(size=1))
        #self.addData(val,val+10,val+15,val+17.5,val+18.75, val+19.375,val+19.6875,val+19.84375)
        self.addArray([val,val+10,val+15,val+17.5,val+18.75, val+19.375,val+19.6875,val+19.84375])
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    Data = RawPlotWidget()
    Data.show()
    Data.addTimer()
    sys.exit(app.exec_())
        
        
