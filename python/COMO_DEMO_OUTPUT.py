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
#     Giuseppe Airo' Farulla (giuseppe.airofarulla@polito.it)
#	  Andrea Bulgarelli

# TCP Server interface
# Usage python Exp_OUTPUT.py serial_port

#Import required
import sys
from os import path,sep,mkdir
import thread
import xml.etree.ElementTree as ET
from random import *
import time
from hand_control import *
import base64
import datetime
import socket
from Crypto.Cipher import AES # encryption library

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'
BLOCK_SIZE = 64

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

SIGN_LIST = ['A','B','C','D','F','I','L','O','R','S','U','V','W','X','Y']

#SIGN_INDEX = 0
#SIGN_SIZE = 15
#MAX_POSES = 100

#Communication Parameters
PASSCODE = 'PARLOMA3'*2
SIGN_WINDOW_NUMBER = 5
IP = 'localhost'
#IP = '10.10.0.1'
PORT = 8089
#PORT = 9091
MSGLEN = 88

class ServerSocket:
    def __init__(self, IP, PORT, PASSCODE, ser, d):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind((IP,PORT))
        self.server_socket.listen(1)

        self.hand = Hand(ser, d)
        #self.hand.perform_hardCalibration()
        #self.hand.perform_softCalibration()
        
        time.sleep(5)
        #self.hand.test()
        #time.sleep(25)
        
        self.hand.perform_rest2()
        #self.hand = 0
        

    def start(self, crypt):
        print 'Waiting on IP '+IP+' and PORT '+str(PORT)
        while True:
            client_socket, address = self.server_socket.accept();
            print 'Listening to client, address:'
            print address
            thread.start_new_thread(self.handController, (self.hand, crypt, client_socket, address))
        
        
    def handController(self, hand, crypt, client_socket, address, *args):
        while True:
            msg = ''
            while len(msg) < MSGLEN:
                chunk = client_socket.recv(MSGLEN-len(msg))
                if chunk == '':
                    print "Connection to Client is DOWN!"
                    print address
                    client_socket.close()
                    return
                msg = msg + chunk
            buf = msg

            if len(buf) != MSGLEN: # client closed or network error
                print 'Client Closed or Communication Error'
                print address
                client_socket.close()
                return
            else:
                buf = DecodeAES(crypt, buf)
                print buf + ' RECEIVED'

                if buf == 'quit':
                    print 'Ok, Quitting'
                    return
                else:
                    x = buf in SIGN_LIST
                    if x == False:
                        hand.perform_rest2()
                    else:
                        res = hand.perform_sign(buf)
                        hand.perform_rest2()

#main
if __name__=="__main__":

    if len(sys.argv)!=3:
        print("Usage: > python script_name serial_port hand_delay")
    else:
        server = ServerSocket(IP, PORT, 'P'*16, sys.argv[1], sys.argv[2])
        crypt = AES.new(PASSCODE)
        server.start(crypt)
