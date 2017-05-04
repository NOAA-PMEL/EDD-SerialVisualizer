# -*- coding: utf-8 -*-
"""
This program is a GUI for the PMEL Eppley Radiation Sensors (LW and SW).

"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.Point import Point
from pyqtgraph.dockarea import *
import pyqtgraph.console

import numpy as np

from serial_rxtx_widget2 import SerialRxTxWidget
from serial_console_widget2 import SerialConsoleWidget
from serial_receive_widget import SerialReceiveParser
from serial_widget import SerialWidget
from clock_widget import DigitalClock
from plot_raw import RawPlotWidget

import sys
import serial

import time


class MainWindow(QtGui.QMainWindow):

    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)

        ## Initialize common variables
        self.sensorType = []
        self.serialNumPMEL = []
        self.serialNumMan = []
        self.firmware = []
        self.dome_gain = []
        self.dome_refV = []
        self.dome_res = []
        self.case_gain = []
        self.case_refV = []
        self.case_res = []
        self.data_report = []
        self.data_rate = []
        self.stream_mode = "Stats"

        

        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'w')

       
        ## Create docks, place them into the window one at a time.
        ## Note that size arguments are only a suggestion; docks will still have to
        ## fill the entire dock area and obey the limits of their internal widgets.
        self.area = DockArea()

        self.dock0 = Dock("Description",size=(50,25))
        self.dock1 = Dock("Serial Port",size=(60,200))
        self.dock2 = Dock("Date/Time",size=(60,25))
        self.dock3 = Dock("PMEL Logo",size=(60,60))
        self.dock5 = Dock("Data Plot",size=(550,550))
        #self.dock6 = Dock("Data",size=(200,50))
        self.dock7 = Dock("Serial Console",size=(200,300))
        self.dock6 = Dock("Serial Rx/Tx Settings",size=(200,300))
        

        self.area.addDock(self.dock0,'left')
        self.area.addDock(self.dock1,'bottom',self.dock0)
        self.area.addDock(self.dock5,'right',self.dock1)

        self.area.addDock(self.dock6,'bottom',self.dock5)
        self.area.addDock(self.dock7,'bottom',self.dock6)
        self.area.addDock(self.dock2,'bottom',self.dock1)
        self.area.addDock(self.dock3,'bottom',self.dock2)
        self.area.moveDock(self.dock6,'above',self.dock7)
        #self.area.addDock(self.dock8,'right',self.dock7)
        
        
        ## Add widgets into each dock
        ## GUI Description 
        self.w_title = pg.LayoutWidget()
        self.w_title.setAutoFillBackground(True)
        palette = self.w_title.palette()
        palette.setColor(QtGui.QPalette.Window,QtGui.QColor('black'))
        label = QtGui.QLabel(""" SerVis  (Serial Visualizer) """)
        font = QtGui.QFont( "Helvetica", 18)
        font.setBold(True)
        label.setFont(font)
        label.setStyleSheet("color: black")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.w_title.addWidget(label, row=0, col=0)
        self.dock0.addWidget(self.w_title)
        self.dock0.hideTitleBar()

        #self.w_title.setConfigOption('background','w')
        #self.w_title.setConfigOption('foreground','k')



        ## SERIAL PORT Widget
        self.w_port = SerialWidget()
        self.dock1.addWidget(self.w_port)

        ## UTC CLOCK Widget
        self.w_clock = DigitalClock()
        self.dock2.addWidget(self.w_clock)

        ## MEATBALL
        self.w_pmel = pg.LayoutWidget()
        pic = QtGui.QLabel()
        pixmap = QtGui.QPixmap("PMEL.png")
        pic.setPixmap(pixmap)
        pic.setScaledContents(True)
        pic.setMaximumSize(150,150)
        self.w_pmel.addWidget(pic, row=0, col=0)
        self.dock3.addWidget(self.w_pmel)
        self.dock3.hideTitleBar()

        ## DATA PLOT Widget
        self.w_plot = RawPlotWidget()
        self.dock5.addWidget(self.w_plot)

        ## CURRENT Data Widget
        #self.w_plota = CurrentDataWidget()
        #self.dock6.addWidget(self.w_plota)

        ## SERIAL CONSOLE Widget
        self.w_serial = SerialConsoleWidget()
        self.dock7.addWidget(self.w_serial)

        ## SERIAL RECEIVE WIDGET
        self.w_rxtx = SerialRxTxWidget()
        self.dock6.addWidget(self.w_rxtx)


        ## System Event Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)


        ## Add All Button Connects that aren't internal to 

        self.setCentralWidget(self.area)

    def update(self):
        """ GUI Update Function
        Updates GUI on QTimer Call, currently set to 100ms.  During call, Serial Port is read,
        parsed and plotted (if valid).  Serial Console is also read.

        Args:
          There are no arguments for this function

        Returns:
          There are no returns for this function

        Raises:
          None

        """

        #self.timer.start(self.w_rxtx.tx.

    
        ## Update the Serial Buffer (read the port)
        self.w_port.update_serial_buffer()
        #print(self.w_port.data)
        ## If there is actually data, parse it and append it to the string buffer for the serial console
        if(len(self.w_port.data) > 0):
            try:
                #print(self.w_port.data)
                ## Parse the string
                #self.parse_serial_data(self.w_port.data)
                data = self.w_rxtx.rx.parse_string(self.w_port.data)
                #print(data[0])

                ## Append the string to the running buffer
                #self.dataStr.append(self.w_port.data)

                ## Add data to plot
                #print("enter")
                self.w_plot.addArray(data[0])
            except:
                #print("failed")
                pass
        try:
            ## Set the console 'label' to the 
            self.label6.setText(''.join(self.dataStr))

            ## Maintain a buffer depth of 20
            if(len(self.dataStr) > 19):
                self.dataStr.pop(0)
        except:
            pass

        

    
    def plot_inst(self):
        pass


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        #QtGui.QApplication.instance().exec_()

        app = QtGui.QApplication([])
        win = MainWindow()

        p = win.palette()
        #p.setColor(win.backgroundRole(),QtCore.Qt.darkGray)
        #p.setColor(win.foregroundRole(),QtCore.Qt.blue)
        win.setPalette(p)
        
        #win.setCentralWidget(area)
        win.resize(900,600)
        win.setWindowTitle('Serial Visualizer')

        win.show()

        app.exec_()
