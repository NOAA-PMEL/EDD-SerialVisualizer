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

from serial_console_widget import SerialConsoleWidget
from serial_widget import SerialWidget
from clock_widget import DigitalClock
from plot_raw import RawPlotWidget

import sys
import serial 


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

        self.d0 = Dock("Description",size=(50,25))
        self.d1 = Dock("Serial Port",size=(60,200))
        self.d3 = Dock("Date/Time",size=(60,25))
        self.d4 = Dock("PMEL Logo",size=(60,60))
        self.d5 = Dock("Data Plot",size=(550,550))
        self.d5a = Dock("Data",size=(200,50))
        self.d6 = Dock("Serial Console",size=(200,300))
        

        self.area.addDock(self.d0,'left')
        self.area.addDock(self.d1,'bottom',self.d0)
        self.area.addDock(self.d5,'right',self.d1)

        self.area.addDock(self.d5a,'bottom',self.d5)
        self.area.addDock(self.d6,'bottom',self.d5a)
        self.area.addDock(self.d3,'bottom',self.d1)
        self.area.addDock(self.d4,'bottom',self.d3)
        
        
        ## Add widgets into each dock
        ## GUI Description 
        self.w0 = pg.LayoutWidget()
        self.w0.setAutoFillBackground(True)
        palette = self.w0.palette()
        palette.setColor(QtGui.QPalette.Window,QtGui.QColor('black'))
        label = QtGui.QLabel(""" SerVis  (Serial Visualizer) """)
        font = QtGui.QFont( "Helvetica", 18)
        font.setBold(True)
        label.setFont(font)
        label.setStyleSheet("color: black")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.w0.addWidget(label, row=0, col=0)
        self.d0.addWidget(self.w0)
        self.d0.hideTitleBar()

        #self.w0.setConfigOption('background','w')
        #self.w0.setConfigOption('foreground','k')



        ## SERIAL PORT Widget
        self.w1 = SerialWidget()
        self.d1.addWidget(self.w1)

        ## UTC CLOCK Widget
        self.w3 = DigitalClock()
        self.d3.addWidget(self.w3)

        ## MEATBALL
        self.w4 = pg.LayoutWidget()
        pic = QtGui.QLabel()
        pixmap = QtGui.QPixmap("PMEL.png")
        pic.setPixmap(pixmap)
        pic.setScaledContents(True)
        pic.setMaximumSize(150,150)
        self.w4.addWidget(pic, row=0, col=0)
        self.d4.addWidget(self.w4)
        self.d4.hideTitleBar()

        ## DATA PLOT Widget
        self.w5 = RawPlotWidget()
        self.d5.addWidget(self.w5)

        ## CURRENT Data Widget
        #self.w5a = CurrentDataWidget()
        #self.d5a.addWidget(self.w5a)

        ## SERIAL CONSOLE Widget
        self.w6 = SerialConsoleWidget()
        self.d6.addWidget(self.w6)
##        self.w6 = pg.LayoutWidget()
##        self.label6 = QtGui.QLabel("""  SERIAL CONSOLE """)
##        self.label6.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
##        self.w6.addWidget(self.label6, row=0, col=0)
##        self.d6.addWidget(self.w6)
##        self.d6.setMaximumHeight(250)

        ## SYSTEM SETTING Parameters
        #self.w7 = SystemSettingWidget()
        #self.d7.addWidget(self.w7)

        ## SENSOR TYPE Widget
        #self.w8 = ImageWidget()
        #self.d8.addWidget(self.w8)


        ## System Event Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

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

    
        ## Update the Serial Buffer (read the port)
        self.w1.update_serial_buffer()
        
        ## If there is actually data, parse it and append it to the string buffer for the serial console
        if(len(self.w1.data) > 0):
            try:
                ## Parse the string
                self.parse_serial_data(self.w1.data)

                ## Append the string to the running buffer
                self.dataStr.append(self.w1.data)  
            except:
                pass
        try:
            ## Set the console 'label' to the 
            self.label6.setText(''.join(self.dataStr))

            ## Maintain a buffer depth of 20
            if(len(self.dataStr) > 19):
                self.dataStr.pop(0)
        except:
            pass

        

    def parse_serial_data(self,buf):
        """ Parse the data on the serial port

        Determines which method of parsing should be accomplished based on current sensor settings

        Possible modes:
          Streaming - Raw Data
          Streaming - Instantaneous Data
          Streaming - Statistical Data

        Args:
          buf: Current Serial Port Buffer string

        Returns:
          There are no returns for this function

        Raises:
          None
        """
        if(self.stream_mode == 'Raw'):
            self.parse_raw(buf)
        if(self.stream_mode == 'Inst'):
            self.parse_instantaneous(buf)
        if(self.stream_mode == 'Stats'):
            print("In Stats")
            self.parse_statistical(buf)

    def parse_instantaneous(self,buf):
        """ Parse instantaneous mode data
        Takes the serial port buffer string and parses it based on instantaneous
        mode for the following variables:

          %s - Timestamp (YYYY/MM/DD HH:MM:SS)
          %f - Net Radiation (W/m^2)
          %f - Dome Temperature (Deg C)    <-- Ignored in Short Wave Sensor
          %f - Case Temperature (Deg C)
          %f - Downwell Radiation (Compensated)

        Args:
          buf: Current serial port buffer string to be parsed

        Returns:
          There are no returns for this function

        Raises:
          ValueError: An error occured splitting the buffer

        """
        try:
            buf = buf.split('\r\n')
            values = buf[0].split(' ')
        except ValueError:
            pass
        pass

    def parse_statistical(self,buf):
        """ Parse statistical mode data
        Takes the serial port buffer string and parses it based on raw mode
        for the following variables:

          %s - Timestamp (YYYY/MM/DD HH:MM:SS)
          %d - Thermopile voltage (Raw Counts)
          %d - Dome Thermistor Voltage (Raw Counts)
          %d - Case Thermistor Voltage (Raw Counts)

        Args:
          buf: Current serial port buffer string to be parsed
        Returns:
          There are no returns for this function
        Raises:
          Value Error: An error occured splitting the buffer

        """
        try:
            buf = buf.split('\r\n')
            values = buf[0].split(' ')
        except ValueError:
            pass

        for val in values:
            if val[0] == 'R':
                rad = float(val[1:])
            if val[0] == 'S':
                std = float(val[1:])
            if val[0] == 'D':
                dome = float(val[1:])
            if val[0] == 'C':
                case = float(val[1:])


        print(dome)
        print(case)
        self.w5.addData(rad,std,dome,case)

    def parse_raw(self,buf):
        """ Parse raw mode data
        Takes the serial port buffer string and parses it based on raw mode
        for the following variables:

          %s - Timestamp (YYYY/MM/DD HH:MM:SS)
          %d - Thermopile voltage (Raw Counts)
          %d - Dome Thermistor Voltage (Raw Counts)
          %d - Case Thermistor Voltage (Raw Counts)

        Args:
          buf: Current serial port buffer string to be parsed
        Returns:
          There are no returns for this function
        Raises:
          Value Error: An error occured splitting the buffer
          
        """
        try:
            buf = buf.split('\r\n')
            values = buf[0].split(' ')
        except ValueError:
            pass

        
        for val in values:
            if val[0] == 'R':
                raw = float(val[1:])
            if val[0] == 'D':
                dome = float(val[1:])
            if val[0] == 'C':
                case = float(val[1:])


        self.w5.addData(raw,dome,case)
##        self.w5a.SetRnet(raw)
##        self.w5a.SetDome(dome)
##        self.w5a.SetCase(case)
##        
##        self.data1.append(np.array([raw]))
##        self.data2.append(np.array([dome]))
##        self.data3.append(np.array([case]))
##        self.data4.append(np.array([0]))
##        
##
##        self.count += 1
##
##        self.plot_raw()
    
        pass

   

    def plot_raw(self):
        """ Plot the raw data values
        Takes the current buffer of raw values and plots them.
        """

        if(len(self.data1)>=100):
            self.data1.pop(0)
            self.data2.pop(0)
            self.data3.pop(0)
            self.data4.pop(0)

        self.curve1.setData(np.hstack(self.data1))
        self.curve2.setData(np.hstack(self.data2))
        self.curve3.setData(np.hstack(self.data3))
        self.curve4.setData(np.hstack(self.data4))
        
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
