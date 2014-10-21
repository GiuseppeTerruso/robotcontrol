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
from visualization_msgs.msg import Marker
import geometry_msgs.msg
import std_msgs.msg
import genpy

class SkeletonRvizNode:
    def __init__(self):
        self.m_id = 0
        rospy.init_node('skeleton_rviz', anonymous=True)

        self.skeleton_topic = rospy.get_param('skeleton_topic','/skeleton_topic')
        self.visualization_topic = rospy.get_param('visualization_topic','/skeleton_rviz')
        self.visualization_pub = rospy.Publisher(self.visualization_topic, Marker, queue_size=10)

        rospy.Subscriber(self.skeleton_topic, hand_skeleton, self.callback_skeleton)
        rospy.spin()


    def callback_skeleton(self, data):
        mk = Marker()
        mk.header.frame_id = '/map'
        mk.ns = 'skeletro'
        mk.id = self.m_id
        self.m_id = self.m_id + 1
        mk.type = Marker.SPHERE_LIST
        mk.points = data.joints
        mk.points.append(geometry_msgs.msg.Point(0,0,0))
        mk.scale = geometry_msgs.msg.Vector3(1,1,1)
        mk.pose.position = geometry_msgs.msg.Point(0,0,0)
        mk.pose.orientation = geometry_msgs.msg.Quaternion(0.0, 0.0, 0.0, 1.0)

        mk.lifetime = genpy.Duration(0.1)

        mk.color = std_msgs.msg.ColorRGBA(1.0,0.0,0.0,1.0)
        self.visualization_pub.publish(mk)

if __name__ == '__main__':
    SkeletonRvizNode()




