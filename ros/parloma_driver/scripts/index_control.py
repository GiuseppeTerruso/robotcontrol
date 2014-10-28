#! /usr/bin/env python

# Copyright (C) 2014 Politecnico di Torino
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#
# This software is developed within the PARLOMA project, which aims
# at developing a communication system for deablinf people (www.parloma.com)
# The PARLOMA project is developed with the Turin node of AsTech laboraroies
# network of Italian CINI (Consorzio Interuniversitario Nazionale di Informatica)
#
# Contributors:
#	Ludovico O. Russo (ludovico.russo@polito.it)


import rospy
from hand_msgs.msg import hand_skeleton
from math import sqrt, pow, acos
import numpy as np
from serial_bridge.msg import generic_serial
from geometry_msgs.msg import Point

class IndexControl:
    def __init__(self):
        self.val= 180
        rospy.init_node('sing_recoignizer', anonymous=True)

        self.serial_topic = rospy.get_param('serial_topic','/serial_topic')
        self.skeleton_topic = rospy.get_param('skeleton_topic','/skeleton')

        rospy.Subscriber(self.skeleton_topic, hand_skeleton, self.callback_skeleton)
        self.pub = rospy.Publisher(self.serial_topic, generic_serial, queue_size=10)
        rospy.spin()

    def callback_skeleton(self, data):
        l = 0.9995
        j1 = data.joints[19]
        j2 = data.joints[14]
        j3 = data.joints[13]


        v1 = Point(j1.x-j2.x, j1.y-j2.y, j1.z-j2.z)
        v2 = Point(j3.x-j2.x, j3.y-j2.y, j3.z-j2.z)

        n1 = sqrt(pow(v1.x,2) + pow(v1.y,2) + pow(v1.z,2))
        n2 = sqrt(pow(v2.x,2) + pow(v2.y,2) + pow(v2.z,2))
        c = v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

        if n1 == 0 or n2 == 0:
            return

        m = acos(c/(n1*n2))*180/3.14

        self.val = (1-l)*self.val + l*m
        print int(m)

        msg = generic_serial()
        msg.msg = [242, 1, int(m)]

        self.pub.publish(msg)

if __name__ == '__main__':
     IndexControl()




