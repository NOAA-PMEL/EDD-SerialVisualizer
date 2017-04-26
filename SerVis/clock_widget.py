from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

#class DigitalClock(QLCDNumber):
class DigitalClock(QWidget):
    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        # Create the label
        vbox = QVBoxLayout()
        self.time = QDateTime()
        self.tlabel = QLabel('time', self)
        self.tlabel.setFont(QFont("Droid Sans",11))
        self.label = QLabel('Current Date/Time (UTC)',self)
        self.label.setFont(QFont("Droid Sans",11))

        

        #Create and set a timer
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.showTime()

        self.setWindowTitle("Digital Clock")
        self.resize(160, 30)


        vbox.addWidget(self.label)
        vbox.addWidget(self.tlabel)

        self.setLayout(vbox)
        self.show()

    def showTime(self):
        self.tlabel.setText(self.time.currentDateTime().toUTC().toString('yyyy/MM/dd hh:mm:ss'))


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())
