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
from hand_msgs.msg import hand_skeleton
from sklearn.externals import joblib



class SignClassifier:
    def __init__(self, forest_file):
        clf = joblib.load(forest_file)


class SignClassifierNode:
    def __init__(self):
        rospy.init_node('sing_recoignizer', anonymous=True)
        self.classifier = SignClassifier('test')
        rospy.Subscriber("skeleton_topic", hand_skeleton, self.callback_skeleton)
        rospy.spin()

    def classify_skeleton(self, joints):
        prob = clf.predict_proba([joints2dist(joints)])
        mm = prob.argmax()
        signRecog = signs[mm]
        prob = prob[0][mm]


    def callback_skeleton(self, data):
        rospy.loginfo(rospy.get_caller_id() + "skeleton: ")
        print data.joints

    
if __name__ == '__main__':
    SignClassifierNode()




