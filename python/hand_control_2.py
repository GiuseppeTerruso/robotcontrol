#! /usr/bin/env python

# Copyright (C) 2014 Politecnico di Torino

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# This software is developed within the PARLOMA project, which aims
# at developing a communication system for deablinf people (www.parloma.com)
# The PARLOMA project is developed with the Turin node of AsTech laboraroies
# network of Italian CINI (Consorzio Interuniversitario Nazionale di Informatica)

# Contributors:
#     Ludovico O. Russo (ludovico.russo@polito.it)


import serial
import time

def constant(prop):
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)


class Hand:

    def __init__(self, hand_port):
        self.serial_comm = serial.Serial(port=hand_port, baudrate=9600)
        if (self.serial_comm.isOpen()):
            print 'Communication Opened!'
        else:
            print 'Error: impossible to establish communication!'
    def __del__(self):
        self.serial_comm.close()
        print 'Communication Closed!'

    def send_command(self, cmds):
        cmds2send = []
        for cmd in cmds:
            cmds2send += chr(cmd)
        self.serial_comm.write(cmds2send)

    def send_command_and_read(self, cmds, num):
        cmds2send = []
        for cmd in cmds:
            cmds2send += chr(cmd)
        self.serial_comm.write(cmds2send)
        return self.serial_comm.read(num)

    def set_all_position(self, positions):
        cmds = [255] + positions
        self.send_command(cmds)

if __name__ == "__main__":
    hand = Hand("/dev/tty.usbmodem1421")
    while True:
        hand.set_all_position([20, 20, 20, 20, 10, 250 ,200, 200, 200]);
        time.sleep(1.0);
