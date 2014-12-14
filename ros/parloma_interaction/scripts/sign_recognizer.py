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
from parloma_msgs.msg import hand_skeleton
from sklearn.externals import joblib
from math import sqrt, pow
import numpy as np
from std_msgs.msg import String

#signs = ['A','B','C','D','F','I','L','R','REST','S','U','V','W','X','Y']

class SignClassifier:
    def __init__(self, forest_file, signs_list_file):
        self.clf = joblib.load(forest_file)
        self.signs = joblib.load(signs_list_file)
        print self.signs

    def classify_skeleton(self, jointsdists):
        prob = self.clf.predict_proba(jointsdists)
        mm = prob.argmax()
        #signRecogIndex = signs[mm]
        signRecogIndex = self.signs[mm]
        prob = prob[0][mm]
        return signRecogIndex, prob


class SignClassifierNode:
    def __init__(self):
        rospy.init_node('sing_recoignizer', anonymous=True)

        self.classifier_path = rospy.get_param('~classifier', 'forest-2layer-Beppe-REST.pkl')
        self.signs_list_path = rospy.get_param('~signs_list', 'SIGN_LIST.pkl')
        self.signs_topic = rospy.get_param('signs_topic','/signs_topic')
        self.skeleton_topic = rospy.get_param('skeleton_topic','/skeleton')

        self.classifier = SignClassifier(self.classifier_path, self.signs_list_path)
        rospy.Subscriber(self.skeleton_topic, hand_skeleton, self.callback_skeleton)
        self.pub = rospy.Publisher(self.signs_topic, String, queue_size=10)
        rospy.spin()

    def classify_skeleton(self, joints_dists):
        signRecogIndex, prob = self.classifier.classify_skeleton(joints_dists)
        return signRecogIndex, prob


    def callback_skeleton(self, data):
        rospy.loginfo(rospy.get_caller_id() + "skeleton: ")
        jointdists = self.joints2dist(data.joints)
        sign, prob = self.classify_skeleton(jointdists)
        if (prob > 0.3):
            self.pub.publish(sign)


    def joints2dist(self, joints):
        dists = []
        for i in range(0,len(joints)):
            for j in range(i+1,len(joints)):
                d = sqrt(pow(joints[i].x - joints[j].x,2) + pow(joints[i].y - joints[j].y,2) + pow(joints[i].z - joints[j].z,2))
                dists.append(d)
        return np.array(dists)


if __name__ == '__main__':
    SignClassifierNode()
