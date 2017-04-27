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
        self.curve5 = self.plt1.plot(pen=(0,63,63),name=('D5'))
        self.curve6 = self.plt1.plot(pen=(63,63,0),name=('D6'))
        self.curve7 = self.plt1.plot(pen=(63,63,63),name=('D7'))
        
        self.plt1.setLabel('left',"",units='Counts')
        

        ## Set up the layout
        vbox.addWidget(self.win1)


        self.setLayout(vbox)
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

    def addTimer(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.fake_data)
        timer.start(100)

    def fake_data(self):
        val = float(np.random.normal(size=1))
        self.addData(val,val+10,val+15,val+17.5,val+18.75, val+19.375,val+19.6875,val+19.84375)

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    Data = RawPlotWidget()
    Data.show()
    Data.addTimer()
    sys.exit(app.exec_())
        
        
