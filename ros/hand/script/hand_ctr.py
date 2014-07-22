#! /usr/bin/env python
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
#
# contributors:
#     Ludovico Russo



# Import required Python code.
import roslib
import rospy
import sys
import hand_control

from hand_msgs.msg import parloma

hand = hand_control.Hand('/dev/tty.usbmodem1411')

def hand_msg_callback(hand_data):
    rospy.loginfo(rospy.get_caller_id()+"%d", hand_data.thumb)
    hand.set_all_position([hand_data.index, hand_data.middle, hand_data.ring, hand_data.pinky, hand_data.thumb,  0])

def hand_controll():
    print 'init'
    rospy.init_node('hand_driver', anonymous=True)
    rospy.Subscriber("hand_topic", parloma, hand_msg_callback)
    rospy.spin()

if __name__ == '__main__':
    hand_controll()
