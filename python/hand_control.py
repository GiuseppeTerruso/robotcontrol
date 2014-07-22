# Copyright (c) 2014 CINI Consorzio Interuniversitario Nazionale di Informatica
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Contributors:
#
#       Ludovico Russo

import serial
import time

def constant(prop):
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)


class Hand:
    sign_set = {'s':[   0, 180, 180, 180, 180,   0], 'v':[ 180,   0,   0, 180, 180,   0], 'w':[ 180,   0,   0,   0, 180,   0], 'corna':[    0,  170, 170,   0, 170], 'fuck':[   170,    0,  170,    170,    0], 'rock':[ 170, 170, 170, 0, 0], 'pugno':[    160,    160,    160,    160,    160,    160], 'rest':[   0,   0,   0,   0,   0,   0], 'f':[ 90, 100, 0,   0, 0,   50]}




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

    def perform_sign(self, sign):
        if (sign in self.sign_set):
            self.set_all_position(self.sign_set[sign])

    def demo_bulga(self):
        self.perform_sign('s')
        time.sleep(2)
        self.perform_sign('v')
        time.sleep(2)
        self.perform_sign('w')
        time.sleep(2)
        self.perform_sign('f')
        time.sleep(2)
        self.perform_sign('pugno')
        time.sleep(2)
        self.perform_sign('rest')
        time.sleep(2)
        self.perform_sign('corna')
        time.sleep(2)
        self.perform_sign('rock')
        time.sleep(2)
        self.perform_sign('fuck')
        time.sleep(2)
        self.perform_sign('rest')
        time.sleep(2)
