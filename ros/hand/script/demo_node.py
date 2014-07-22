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



PACKAGE='hand_demo_node'
# Import required Python code.
import roslib
import rospy
import sys
import hand_control


def hand_demo_controll():
    hand = hand_control.Hand('/dev/tty.usbmodem1411')
    hand.demo_bulga()

if __name__ == '__main__':
    hand_demo_controll()
