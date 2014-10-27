#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore

class HandWidget(QtGui.QWidget):

    def __init__(self, numbs):
        self.app = QtGui.QApplication(sys.argv)
        super(HandWidget, self).__init__()
        self.initUI(numbs)

    def run(self):
        sys.exit(self.app.exec_())

    def initUI(self, numbs):
        vbox = QtGui.QVBoxLayout()

        self.slds = []
        for i in range(0,numbs):
            sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
            sld.setMinimum(0)
            sld.setMaximum(180)
            lcd = QtGui.QLCDNumber(self)
            sld.valueChanged.connect(lcd.display)
            hbox = QtGui.QHBoxLayout()
            hbox.addWidget(sld)
            hbox.addWidget(lcd)
            self.slds.append(sld)
            vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.button1 = QtGui.QPushButton('Send',self)
        vbox.addWidget(self.button1)

        self.setGeometry(300, 300, 250, 150)

        self.setWindowTitle('Signal & slot')
        self.show()

    def connect_button(self, signal):
        self.connect(self.button1, QtCore.SIGNAL('clicked()'), signal)

    def get_scrolls(self):
        values = [sld.value() for sld in self.slds]
        return values

    def set_scrolls(self, values):
        if isinstance(values, list):
            if len(values) == len(self.slds):
                for i in range(0,len(self.slds)):
                    self.slds[i].setValue(values[i])
        elif isinstance(values, int):
            for i in range(0,len(self.slds)):
                self.slds[i].setValue(values)

def ciao():
    print main.ex.get_scrolls()

def main():
    main.ex = HandWidget(9)
    main.ex.connect_button(ciao)
    main.ex.set_scrolls(100)
    main.ex.run()


if __name__ == '__main__':
    main()
