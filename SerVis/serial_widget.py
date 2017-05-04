from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import serial



class SerialWidget(QWidget):

    

    def __init__(self,*args,**kwargs):
        super(SerialWidget,self).__init__(*args,**kwargs)


        #timer = QTimer(self)
        #timer.timeout.connect(self.update_serial_buffer)
        #timer.start(250)

        self.data = []
        

        self.ser = serial.Serial()


        #set the labels
        self.port_lbl = QLabel("Port", self)
        self.port_lbl.setFont(QFont("Droid Sans",11))
        self.baud_label = QLabel("Baudrate",self)
        self.baud_label.setFont(QFont("Droid Sans",11))
        self.data_lbl = QLabel("Data Bits",self)
        self.data_lbl.setFont(QFont("Droid Sans",11))
        self.parity_lbl = QLabel("Parity",self)
        self.parity_lbl.setFont(QFont("Droid Sans",11))
        self.stop_lbl = QLabel("Stop Bits",self)
        self.stop_lbl.setFont(QFont("Droid Sans",11))
        
        #set the default values
        self.baudrate = 9600
        self.bits = []
        self.port = []
        self.portnames = []
        self.timeout = 1
        
        #Setup the Port
        self.find_available_ports()
        self.port_combo = QComboBox(self)
        self.port_combo.setFixedWidth(75)
        self.port_combo.highlighted.connect(self.find_available_ports)
        for port in self.portnames:
            self.port_combo.addItem(str(port))
        

        #Setup the baudrate
        self.baud_combo = QComboBox(self)
        self.baud_combo.setFixedWidth(75)
        #br = list(serial.Serial.BAUDRATES)
        for baud in list(serial.Serial.BAUDRATES):
            self.baud_combo.addItem(str(baud))
        self.baud_combo.setCurrentIndex(serial.Serial.BAUDRATES.index(9600))

        #Setup the parity
        self.parity_combo = QComboBox(self)
        self.parity_combo.setFixedWidth(75)
        #par = list(serial.Serial.PARITIES)
        for parity in list(serial.Serial.PARITIES):
            self.parity_combo.addItem(parity)
        self.parity_combo.setCurrentIndex(serial.Serial.PARITIES.index('N'))

        #Setup the data bits
        self.data_combo = QComboBox(self)
        self.data_combo.setFixedWidth(75)
        #par = list(serial.Serial.PARITIES)
        for databits in list(serial.Serial.BYTESIZES):
            self.data_combo.addItem(str(databits))
        self.data_combo.setCurrentIndex(serial.Serial.BYTESIZES.index(8))

        #Setup the stop bits
        self.stop_combo = QComboBox(self)
        self.stop_combo.setFixedWidth(75)
        #par = list(serial.Serial.PARITIES)
        for stopbits in list(serial.Serial.STOPBITS):
            self.stop_combo.addItem(str(stopbits))
        self.stop_combo.setCurrentIndex(serial.Serial.STOPBITS.index(1))

        #Setup the Connect to Port button
        self.port_btn = QPushButton(u"Press to Connect",self)
        self.port_btn.setCheckable(True)
        self.port_btn.setStatusTip("Connect to the Serial Port")
        self.port_btn.clicked.connect(self.port_btn_clicked)
        #self.port_btn.released.connect(self.disconnect_from_port)
        self.port_btn.setFixedWidth(165)
        self.port_btn.setFont(QFont("Droid Sans",11))


        
        #Move the labels and boxes into place
        self.port_lbl.move(10,10)
        self.port_combo.move(100,10)
        self.baud_label.move(10,40)
        self.baud_combo.move(100,40)
        self.parity_lbl.move(10,70)
        self.parity_combo.move(100,70)
        self.data_lbl.move(10,100)
        self.data_combo.move(100,100)
        self.stop_lbl.move(10,130)
        self.stop_combo.move(100,130)
        self.port_btn.move(10,160)

        self.show()
        
    def port_btn_clicked(self):
        if self.port_btn.isChecked():
            self.connect_to_port()
        else:
            self.disconnect_from_port()
            
    def connect_to_port(self):
        self.port_btn.setText('Press to Disconnect')
        self.ser.port = self.port_combo.currentText()
        self.ser.baud = int(self.baud_combo.currentText())
        self.ser.parity = self.parity_combo.currentText()
        self.ser.bytesize = int(self.data_combo.currentText())
        self.ser.stopbits = int(self.stop_combo.currentText())
        self.ser.timeout = self.timeout
        try:
            self.ser.open()
            print("Connected!")
        except:
            self.ser.close()
            print("Unable to Connect")

    def disconnect_from_port(self):
        self.port_btn.setText('Press to Connect')
        self.ser.close()
        #print("Disconnected!")

    def find_available_ports(self):
        #sself.port_combo
        
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i+1) for i in range(256)]
            #print(ports)
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported Platform')

        del(self.portnames)
        self.portnames = []

        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.portnames.append(port)
            except (OSError,serial.SerialException):
                pass

    def update_serial_buffer(self):
        data = []
        self.data = []
        #print(self.data)
        if self.ser.isOpen() == True:
            #while(self.ser.inWaiting() > 0):
            try:
                #print("Collecting data!")
                data = self.ser.readline()
                self.ser.flushInput()
                data = data.decode("utf-8")
                if(len(data) > 1):
                    #print(self.data)
                    #self.data.append(str(data))
                    self.data = data
                    #print(self.data)
                #print(self.data)
            except:
                #print("Port Not Open")
                pass

    def set_timer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_serial_buffer)
        timer.start(250)



if __name__ == "__main__":            
    class MainWindow(QMainWindow):

        def __init__(self,*args,**kwargs):
            super(MainWindow,self).__init__(*args,**kwargs)

            self.setWindowTitle("Main Test Window")
            layout = QVBoxLayout()
            self.SerialPort = SerialWidget()

            
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
