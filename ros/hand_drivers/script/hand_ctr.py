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
import hand_control

from hand_msgs.msg import parloma


class HandDriverNode():
    def __init__(self):
        # get parameters
        self.port = rospy.get_param('~port', '/dev/ttyACM0');
        self.topic = rospy.get_param('~topic', '/hand_topic');

        # init topics
        rospy.Subscriber(self.topic, parloma, self.hand_msg_callback)
        self.hand = hand_control.Hand(self.port)

        rospy.loginfo(rospy.get_caller_id()+ " Node Initialized")
        rospy.spin()


    def hand_msg_callback(self, hand_data):
        self.commands = [hand_data.index, hand_data.middle, hand_data.ring, hand_data.pinky, hand_data.thumb,  0];
        self.hand.set_all_position(self.commands)


if __name__ == '__main__':
    rospy.init_node('hand_driver', anonymous=True)
    try:
        ne = HandDriverNode()
    except rospy.ROSInterruptException: pass
