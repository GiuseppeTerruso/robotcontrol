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

from hand_msgs.msg import parloma


class HandTestNode():
    def __init__(self):
        # get parameters
        self.topic = rospy.get_param('~topic', '/hand_topic');

        # init topics
        pub = rospy.Publisher(self.topic, parloma)

        rospy.loginfo(rospy.get_caller_id()+ " Node Initialized")
        r = rospy.Rate(10) # 10hz
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
