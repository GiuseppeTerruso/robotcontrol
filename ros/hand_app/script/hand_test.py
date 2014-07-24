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

from hand_msgs.msg import parloma


class HandTestNode():
    def __init__(self):
        # get parameters
        self.topic = rospy.get_param('~topic', '/hand_topic');

        # init topics
        pub = rospy.Publisher(self.topic, parloma)

        rospy.loginfo(rospy.get_caller_id()+ " Node Initialized")
        r = rospy.Rate(20) # 10hz
        state = 0

        msg = parloma();
        msg.thumb = 10
        msg.index = 10
        msg.middle = 10
        msg.ring = 10
        msg.pinky= 10

        pub.publish(msg)
        r.sleep()
        rospy.sleep(2.0)
        while not rospy.is_shutdown():
            if state == 0:
                msg.thumb = msg.thumb + 10
                if msg.thumb > 160:
                    state = 1
            elif state == 1:
                msg.index= msg.index + 10
                if msg.index > 160:
                    state = 2
            elif state == 2:
                msg.middle= msg.middle+ 10
                if msg.middle> 160:
                    state = 3
            elif state == 3:
                msg.ring = msg.ring + 10
                if msg.ring > 160:
                    state = 4
            elif state == 4:
                msg.pinky= msg.pinky+ 10
                if msg.pinky > 160:
                    state = 5
            elif state == 5:
                msg.thumb = msg.thumb - 10
                if msg.thumb < 20:
                    state = 6
            elif state == 6:
                msg.index= msg.index - 10
                if msg.index < 20:
                    state = 7
            elif state == 7:
                msg.middle= msg.middle - 10
                if msg.middle< 20:
                    state = 8
            elif state == 8:
                msg.ring = msg.ring - 10
                if msg.ring < 20:
                    state = 9
            elif state == 9:
                msg.pinky= msg.pinky - 10
                if msg.pinky< 20:
                    state = 0
            pub.publish(msg)
            r.sleep()

if __name__ == '__main__':
    rospy.init_node('hand_test', anonymous=True)
    try:
        ne =HandTestNode()
    except rospy.ROSInterruptException: pass
