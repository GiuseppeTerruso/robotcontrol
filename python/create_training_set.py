import sys
from os import sep, mkdir, chdir
import numpy as np
from cv2 import *
from hand_grabber import PyOpenNIHandGrabber
from pose_recognizer import PyPoseRecognizer
import xml.etree.ElementTree as ET


WIDTH=640
HEIGHT=480
RADIUS = 150.0
USE_CPU = False
MAX_FRAMES_PER_SIGN = 500

JOINT_IDX2NAME = ["thumb_3_R", "thumb_2_R", "thumb_1_R",
                  "pinky_3_R", "pinky_2_R", "pinky_1_R",
                  "ring_3_R", "ring_2_R", "ring_1_R",
                  "middle_3_R", "middle_2_R", "middle_1_R",
                  "index_3_R", "index_2_R", "index_1_R",
                  "thumb_palm_R", "pinky_palm_R", "ring_palm_R", "middle_palm_R", "index_palm_R",
                  "palm_R", "wrist_R"]
                  
#SIGN_LIST = ['A','B','C','D','F','I','L','R','S1','U','V','W','X','Y']
SIGN_LIST = ['REST']

# Usage: python scriptname 1_layer_forrest user_name

if __name__=="__main__":
    
    if len(sys.argv)==3:

        namedWindow("rgb")
        namedWindow("mask")
        namedWindow("sign")
    
        recog = PyPoseRecognizer(WIDTH, HEIGHT,
                                 sys.argv[1],
                                 False, 320)
        grabber = PyOpenNIHandGrabber()

        #mkdir("."+sep+sys.argv[2])
        chdir("."+sep+sys.argv[2])

        print("Wave the hand in front of the sensor")
        while True:
            rgb, depth = grabber.grabFrames()
            pos = grabber.getHand3DPos() 
            if pos[0] or pos[1] or pos[2]:
                break

        print("+/-: increase/decrease the segmentation radius")
        print("space: start/stop recording")
        print("q: exit")
        
       
        recording = False
        for sign in SIGN_LIST:
            joints = []
            weights = []
            depthmaps = []
            
            print("Perform sign %s, press spase to start/stop, q to exit from the sign\a" %sign)
            while len(joints)<MAX_FRAMES_PER_SIGN:
                rgb, depth = grabber.grabFrames()

                pos = grabber.getHand3DPos()
                mask = grabber.segment(depth, pos, RADIUS)

                currJoints = recog.getJoints(depth, mask)
                
                imshow("rgb", cvtColor(rgb, COLOR_RGB2BGR))
                imshow("mask", mask)
                
                k = waitKey(1)
                if k != -1:
                    k %= 256
                    if chr(k) == '+':
                        RADIUS += 1.0
                    elif chr(k) == '-':
                        RADIUS -= 1.0
                    elif chr(k) == ' ':
                        recording = not recording
                        if (recording):
                            print 'Start Recording'
                        else:
                            print 'Stop Recording'
                    elif chr(k) == 'q':
                        break
            
                if recording:
                    joints.append(currJoints)
                    depthmaps.append(depth.copy())
                    print len(joints)

            frameIdx = 0
            mkdir(sign+sep)
            for currJoints, depthmap in zip(joints, depthmaps):

                root = ET.Element('joints')
                tree = ET.ElementTree(root)
                jointIdx = 0
                for joint in zip(currJoints):
                    #print joint, joint[0]
                    jointNode = ET.SubElement(root, JOINT_IDX2NAME[jointIdx])
                    coordsNode = ET.SubElement(jointNode, "coords")
                    coordsNode.text = "%.3f %.3f %.3f"%(joint[0][0], joint[0][1], joint[0][2])
                    #weightNode = ET.SubElement(jointNode, "weight")
                    #weightNode.text = str(weight[0])
                    jointIdx += 1
                tree.write(sign+sep+"frame%d_joints.xml"%frameIdx)
                imwrite(sign+sep+"frame%d_depth.png"%frameIdx, depthmap)
                frameIdx += 1

            print("Wave the hand in front of the sensor")
            while True:
                rgb, depth = grabber.grabFrames()
                pos = grabber.getHand3DPos() 
                if pos[0] or pos[1] or pos[2]:
                    break
