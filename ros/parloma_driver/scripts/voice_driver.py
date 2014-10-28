#!/usr/bin/env python

'''
The service as soon as receives from the client node 
the sentence will convert each letter to the upper case
and then transposes letter by letter in the corrispondent
in Morse code. In addition to letters and numbers 
it is possible to convert also some symbols. 
The Morse code is executed with both the Buzzer
and a led.
'''

import os
import rospy
from std_msgs.msg import String

class VoiceNode:
    def sign_callback(self, data):
        print data.data
        if self.lastPh == data.data:
            return
        self.lastPh = data.data
        for letter in data.data:
            os.system('espeak -v it '+letter )

    def __init__(self):
        self.lastPh = ''
        print "Ready to convert"
        rospy.init_node('voice_driver')
        self.input_topic = rospy.get_param("input_topic", '/signs_topic')
        self.subs = rospy.Subscriber(self.input_topic, String, self.sign_callback)
        rospy.spin()

if __name__=='__main__':
    nh = VoiceNode()
