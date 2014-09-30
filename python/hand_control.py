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

# PARLOMA hand driver

import serial
import time

def constant(prop):
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)


class Hand:

	# ToDo: These should be constant values	
    THUMB = 0x00
    INDEX = 0x01
    MIDDLE = 0x02
    RING = 0x03
    LITTLE = 0x04
    THUMB_A = 0x05
    INDEX_A = 0x06
    MIDDLE_A = 0x07
    WRIST = 0x08
    
    joint_set = {'thumb':THUMB, 'index':INDEX, 'middle':MIDDLE, 'ring':RING, 'little':LITTLE, 'thumb_a': THUMB_A, 'index_a': INDEX_A, 'middle_a': MIDDLE_A, 'wrist': WRIST}

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
        self.serial_comm.write(''.join(cmds2send))

    def send_command_and_read(self, cmds, num):
        cmds2send = []
        for cmd in cmds:
            cmds2send += chr(cmd)
        self.serial_comm.write(cmds2send)
        return self.serial_comm.read(num)

    def set_all_position(self, positions):
        cmds = [241] + positions
        self.send_command(cmds)

    def test(self):
        cmds = [246]
        self.send_command(cmds)

    def set_finger_position(self, finger, position):
        cmds = [242] + [self.joint_set[finger], position]
        self.send_command(cmds)

    def get_sign(self):
        res = ''
        self.send_command([243])
        for joint in self.joint_set:
		    value = ord(self.serial_comm.read())
		    res = res + str(value) + ' '
        return res


    def perform_a(self):
        for joint in ['little', 'ring', 'middle', 'index', 'thumb']:
            self.set_finger_position(joint, 180)


    def perform_b(self):
        time.sleep(1)

    def perform_c(self):
        time.sleep(1)

    def perform_d(self):
        time.sleep(1)

    def perform_f(self):
        time.sleep(1)

    def perform_h(self):
        time.sleep(1)

    def perform_i(self):
        time.sleep(1)

    def perform_l(self):
        time.sleep(1)

    def perform_o(self):
        time.sleep(1)

    def perform_r(self):
        time.sleep(1)

    def perform_s(self):
        time.sleep(1)

    def perform_u(self):
        time.sleep(1)
			
    def perform_v(self):
        time.sleep(1)

    def perform_w(self):
        time.sleep(1)

    def perform_x(self):
        time.sleep(1)

    def perform_y(self):
        time.sleep(1)

    def perform_rest2(self):
        time.sleep(1)


    SIGN_LIST = ['A','B','C','D','F','I','L','O','R','S','U','V','W','X','Y']
    FNCT_LIST = {'A':perform_a, 'B':perform_b, 'C':perform_c, 'D':perform_d, 'F':perform_f, 'I':perform_i, 'L':perform_l, 'O':perform_o, 'R':perform_r, 'S':perform_s, 'U':perform_u, 'V':perform_v, 'W':perform_w, 'X':perform_x, 'Y':perform_y}       


    def perform_sign(self, msg):
        #print 'Segno da stampare ' + msg
        self.FNCT_LIST[msg](self)
        time.sleep(5)
        return self.get_sign()


if __name__=="__main__":
    hand = Hand('/dev/ttyACM0')

    #for msg in hand.SIGN_LIST:
    for msg in ['A']:
        hand.perform_rest2()
        #print 'Performin Sign ' + msg
        time.sleep(2)
        hand.FNCT_LIST[msg](hand)
        time.sleep(5)
        hhh = hand.get_sign()
        print hhh
