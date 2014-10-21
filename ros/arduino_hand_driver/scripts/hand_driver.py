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



# Import required Python code.
import roslib
import rospy
import sys

from serial_bridge.msg import generic_serial
from std_msgs.msg import String


MOVE_ALL_CMD = 241

class HandDriver():
    def sign_callback(self, sign):
        if sign.data == 'U':
            msg = generic_serial()
            msg.msg = [244, 20]
            self.serial_pub.publish(msg)
        elif sign.data == 'V':
            msg = generic_serial()
            msg.msg = [244, 21]
            self.serial_pub.publish(msg)
        else:
            self.send_rest()

    def send_rest(self):
        msg = generic_serial()
        msg.msg = [MOVE_ALL_CMD, 180, 180, 180, 180, 180, 70, 90 ,50 ,120]
        self.serial_pub.publish(msg)

    def __init__(self):
        # get parameters
        self.input_topic = rospy.get_param('~signs_topic', '/signs_topic');
        self.output_topic = rospy.get_param('~serial_topic', '/serial_topic');

        # init topics
        rospy.Subscriber(self.input_topic, String, self.sign_callback)
        self.serial_pub = rospy.Publisher(self.output_topic, generic_serial, queue_size=10)

        rospy.loginfo(rospy.get_caller_id()+ " Node Initialized")
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('arduino_hand_driver', anonymous=True)
    try:
        ne = HandDriver()
    except rospy.ROSInterruptException: pass
