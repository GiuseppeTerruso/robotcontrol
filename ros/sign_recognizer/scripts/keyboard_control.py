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
from std_msgs.msg import String


class KeyboardNode:
    def __init__(self):
        rospy.init_node('keaboard_sign', anonymous=True)

        self.signs_topic = rospy.get_param('signs_topic','/parloma/signs_topic')

        self.pub = rospy.Publisher(self.signs_topic, String, queue_size=10)
        while not rospy.is_shutdown():
            something = raw_input()
            for l in something:
                self.pub.publish(l)
                rospy.sleep(1.0)

if __name__ == '__main__':
     KeyboardNode()




