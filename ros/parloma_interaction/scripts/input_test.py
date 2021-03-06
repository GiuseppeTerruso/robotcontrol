#! /usr/bin/env python
#Parameters: RF First Classification Layer - RF Second Classification Layer

#Import required
from cv2 import *
from hand_grabber import PyOpenNIHandGrabber
from pose_recognizer import PyPoseRecognizer
import Image

from parloma_msgs.msg import hand_skeleton
from geometry_msgs.msg import Point

import rospy
import numpy as np


WIDTH=640
HEIGHT=480
RADIUS = 150.0
USE_CPU = False



class SkeletonTrackerNode:
    def __init__(self):
        rospy.init_node('skeleton_node', anonymous=True)
        # self.recog = PyPoseRecognizer(22, WIDTH, HEIGHT,self.forest_file,USE_CPU, 320)
        self.grabber = PyOpenNIHandGrabber()

    def run(self):
        while not rospy.is_shutdown():
            print("Wave the hand in front of the sensor \n")
            self.found_mask = False
            while not rospy.is_shutdown() and not self.find_hand():
                pass
            self.found_mask = True
            while not rospy.is_shutdown() and self.track_skeleton():
                pass

    def find_hand(self):
        self.rgb, self.depth = self.grabber.grabFrames()
        # pos = self.grabber.getHand3DPos()
        self.show_image()
        # if len(pos) > 2:
            # if pos[0] or pos[1] or pos[2]:
                # return True
        return False

    def track_skeleton(self):
        self.rgb, self.depth = self.grabber.grabFrames()
        pos = self.grabber.getHand3DPos()

        if not pos[0] and not pos[1] and not pos[2]:
            print ("Hand position lost...")
            return False

        self.mask = self.grabber.segment(self.depth, pos, RADIUS)
        joints = self.recog.getJoints(self.depth, self.mask)

        self.pub_skeleton(joints)
        self.show_image()
        return True

    def show_image(self):
        to_show = cvtColor(self.rgb, COLOR_RGB2BGR)
        # if (self.found_mask):
        #     blank_image = np.zeros(to_show.shape, np.uint8)
        #     blank_image[:,:] = (0,0,255)

        #     rows,cols = self.mask.shape
        #     M = np.float32([[1,0,-20],[0,1,0]])
        #     self.mask = warpAffine(self.mask,M,(cols, rows))
        #     blank_image = bitwise_and(blank_image, blank_image, mask = self.mask)
        #     to_show = addWeighted(to_show, 1, blank_image, 0.4, 0)
        imshow("Image", to_show)
        k = waitKey(30)

    def pub_skeleton(self, joints):
        msg = hand_skeleton()
        for j in joints:
            msg.joints.append(Point(j[0], j[1],j[2]))
        self.skeleton_pub.publish(msg)


if __name__=="__main__":
    tracker_node = SkeletonTrackerNode()
    tracker_node.run()

