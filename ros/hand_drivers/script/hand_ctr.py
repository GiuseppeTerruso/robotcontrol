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
