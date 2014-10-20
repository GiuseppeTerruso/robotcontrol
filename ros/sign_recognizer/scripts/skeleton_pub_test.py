#!/usr/bin/env python

import rospy
from hand_msgs.msg import hand_skeleton
from geometry_msgs.msg import Point



pub = rospy.Publisher('/skeleton_topic', hand_skeleton, queue_size=10)
rospy.init_node('skeleton_pubs')
r = rospy.Rate(10) # 10hz
while not rospy.is_shutdown():
    data = hand_skeleton()
    pi = Point(1,2,3)
    data.joints = [pi, Point(2,3,4)]
    pub.publish(data)
    r.sleep()
