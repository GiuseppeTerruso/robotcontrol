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

#Import required
import sys
from os import path,sep,mkdir
import numpy as np
from cv2 import *
import xml.etree.ElementTree as ET
import Image
from random import *
import time
from my_fun import *
from sklearn.externals import joblib
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
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

#Parameters
WIDTH=640
HEIGHT=480
RADIUS = 150.0
USE_CPU = False
USE_PROB = False

#Joints Names and Signs List
JOINT_IDX2NAME = ["thumb_3_R", "thumb_2_R", "thumb_1_R",
                  "pinky_3_R", "pinky_2_R", "pinky_1_R",
                  "ring_3_R", "ring_2_R", "ring_1_R",
                  "middle_3_R", "middle_2_R", "middle_1_R",
                  "index_3_R", "index_2_R", "index_1_R",
                  "thumb_palm_R", "pinky_palm_R", "ring_palm_R", "middle_palm_R", "index_palm_R",
                  "palm_R", "wrist_R"]

SIGN_LIST = ['A','B','C','D','F','I','L','O','R','S','U','V','W','X','Y']
SIGN_INDEX = 0
SIGN_SIZE = 15
MAX_POSES = 30

#Communication Parameters
PASSCODE = 'PARLOMA3'*2
SIGN_WINDOW_NUMBER = 5
#IP = 'localhost'
IP = '10.10.0.1'
#PORT = 8089
#IP = '192.168.85.201'
PORT = 9091

#Class managing the Client Socket used to send messages to the Haptic Interface Controller (acting as a server)
class ClientSocket:
    def __init__(self, IP, PORT, PASSCODE, sock=None):
        if sock is None:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((IP, PORT))
        else:
            self.client_socket = sock

    def send_msg(self,msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.client_socket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError, "Connection to Server is DOWN!"
            totalsent = totalsent + sent

#Create Random List of Signs
def create_list():
    today = datetime.datetime.now()
    timems = today.strftime("%S")
    seed(10 + int(float(timems)))
    timem = today.strftime("%M")
    seed(7 + randint(1,3*int(float(timem))))
    sign_lista = SIGN_LIST*2
    lista = []
    M_POSES = 30
    while M_POSES>0:
        num = randint(0,MAX_POSES-1)
        lista.append(sign_lista[num])
        sign_lista[num] = sign_lista[M_POSES-1]
        M_POSES = M_POSES-1
    #print lista
    return lista
    
#main
if __name__=="__main__":

    time.sleep(10)

    client = ClientSocket(IP, PORT, 'P'*16)

    #CV2 Window
    namedWindow("segno")

    lista = create_list()
    crypt = AES.new(PASSCODE)
    results = "Iteration \t Sign Required \t Sign recognized \n"

    for i in range(0,MAX_POSES):

        #Sign to be performed - shown for 5 seconds ca. after tracker is acquired
        sign = lista[i]
        print("Perform sign %s\n"%sign)
        # image = imread(".."+sep+"signs reduced set"+sep+sign+".png")

        for j in range(0,50):
            # imshow("segno", image)
            k = waitKey(1)

        signRecog = sign
        prob = 1
        signRecogC = EncodeAES(crypt,signRecog)

        tmp = ""+str(i)+"\t"+sign+"\t"+signRecog+" \n"
        print tmp
        results = results + tmp

        #Send and acknowledge
        client.send_msg(signRecogC)
        print("Recognized and sent sign %s\n"%signRecog)
        #The hand will hold on the sign for 5 seconds
        time.sleep(8)
        #prediction = recog.predict(depth, mask)

        #At the end of each iteration save the results related to the volunteer
        results = results + "\n"

