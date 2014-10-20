#! /usr/bin/env python
#Parameters: RF First Classification Layer - RF Second Classification Layer

#Import required
import sys
from os import path,sep,mkdir
from cv2 import *
from hand_grabber import PyOpenNIHandGrabber
from pose_recognizer import PyPoseRecognizer
import Image

from hand_msgs.msg import hand_skeleton
from geometry_msgs.msg import Point

import rospy


WIDTH=640
HEIGHT=480
RADIUS = 150.0
USE_CPU = False

JOINT_IDX2NAME = ["thumb_3_R", "thumb_2_R", "thumb_1_R",
                  "pinky_3_R", "pinky_2_R", "pinky_1_R",
                  "ring_3_R", "ring_2_R", "ring_1_R",
                  "middle_3_R", "middle_2_R", "middle_1_R",
                  "index_3_R", "index_2_R", "index_1_R",
                  "thumb_palm_R", "pinky_palm_R", "ring_palm_R", "middle_palm_R", "index_palm_R",
                  "palm_R", "wrist_R"]

MAX_POSES = 160


if __name__=="__main__":

        rospy.init_node('skeleton_node', anonymous=True)
        namedWindow("rgb")
        namedWindow("masc")
        namedWindow("segno")
        #OpenNi tracker and Cypher Initialization
        recog = PyPoseRecognizer(22, WIDTH, HEIGHT,
                                 '/Users/ludus/develop/parloma/rc2/RF/forest-1layer.xml',
                                 USE_CPU, 320)
        grabber = PyOpenNIHandGrabber()

        pub = rospy.Publisher('/skeleton', hand_skeleton, queue_size=10)
        #OpenNi wave to start tracking
        while True:
            print("Wave the hand in front of the sensor \n")
            while True:
                rgb, depth = grabber.grabFrames()
                pos = grabber.getHand3DPos() 
                if len(pos) > 2:
                    if pos[0] or pos[1] or pos[2]:
                        break
            while True:
                rgb, depth = grabber.grabFrames()
                pos = grabber.getHand3DPos() 
                if len(pos) <= 2:
                    break
                mask = grabber.segment(depth, pos, RADIUS)
                prediction = recog.predict(depth, mask)
                joints = recog.getJoints(depth, mask)

                imshow("rgb", cvtColor(rgb, COLOR_RGB2BGR))
                imshow("masc", mask)
                k = waitKey(100)
                print joints

                msg = hand_skeleton()
                for j in joints:
                    msg.joints.append(Point(j[0], j[1],j[2]))
                pub.publish(msg)

