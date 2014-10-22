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
from visualization_msgs.msg import Marker, MarkerArray
import geometry_msgs.msg
import std_msgs.msg
import genpy

class SkeletonRvizNode:
    def __init__(self):
        self.m_id = 0
        rospy.init_node('skeleton_rviz', anonymous=True)

        self.skeleton_topic = rospy.get_param('skeleton_topic','/skeleton_topic')
        self.visualization_topic = rospy.get_param('visualization_topic','/skeleton_rviz')
        self.visualization_pub = rospy.Publisher(self.visualization_topic, MarkerArray, queue_size=10)

        rospy.Subscriber(self.skeleton_topic, hand_skeleton, self.callback_skeleton)
        rospy.spin()

    def point_is_valid(self, point):
        if (point.x == -1 and point.y == -1 and point.z == -1):
            return False
        else:
            return True

    def vis_add_line(self, marker, points, i,j):
        if (self.point_is_valid(points[i]) and self.point_is_valid(points[j])):
            marker.points.append(points[i])
            marker.points.append(points[j])

    def callback_skeleton(self, data):
        mk = Marker()
        mk.header.frame_id = '/map'
        mk.ns = 'skeletro'
        mk.id = self.m_id
        mk.type = Marker.SPHERE_LIST
        mk.points = []
        for j in data.joints:
            if self.point_is_valid(j):
                mk.points.append(j)

        mk.scale = geometry_msgs.msg.Vector3(3,3,3)
        mk.pose.position = geometry_msgs.msg.Point(0,0,0)
        mk.pose.orientation = geometry_msgs.msg.Quaternion(0.0, 0.0, 0.0, 1.0)

        # mk.lifetime = genpy.Duration(0.1)
        mk.color = std_msgs.msg.ColorRGBA(1.0,0.0,0.0,1.0)


        linek = Marker()
        linek.header.frame_id = '/map'
        linek.ns = 'lines'
        linek.id = self.m_id
        linek.type = Marker.LINE_LIST
        linek.scale = geometry_msgs.msg.Vector3(0.3,0.3,0.3)
        linek.pose.position = geometry_msgs.msg.Point(0,0,0)
        linek.pose.orientation = geometry_msgs.msg.Quaternion(0.0, 0.0, 0.0, 1.0)

        linek.points = []
        self.vis_add_line(linek, data.joints, 0, 1)
        self.vis_add_line(linek, data.joints, 1, 2)

        self.vis_add_line(linek, data.joints, 3, 4)
        self.vis_add_line(linek, data.joints, 4, 5)

        self.vis_add_line(linek, data.joints, 6, 7)
        self.vis_add_line(linek, data.joints, 7, 8)


        self.vis_add_line(linek, data.joints, 9, 10)
        self.vis_add_line(linek, data.joints, 10, 11)

        self.vis_add_line(linek, data.joints, 12, 13)
        self.vis_add_line(linek, data.joints, 13, 14)

        # linek.lifetime = genpy.Duration(0.1)
        linek.color = std_msgs.msg.ColorRGBA(0.0,1.0,0.0,1.0)


        msg = MarkerArray()
        msg.markers = []
        msg.markers.append(mk)
        msg.markers.append(linek)
        self.visualization_pub.publish(msg)

        # self.m_id = self.m_id + 1
if __name__ == '__main__':
    SkeletonRvizNode()




