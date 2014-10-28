#! /usr/bin/env python

# Copyright (C) 2014 Politecnico di Torino

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# This software is developed within the PARLOMA project, which aims
# at developing a communication system for deablinf people (www.parloma.com)
# The PARLOMA project is developed with the Turin node of AsTech laboraroies
# network of Italian CINI (Consorzio Interuniversitario Nazionale di Informatica)

# Contributors:
#     Ludovico O. Russo (ludovico.russo@polito.it)



# Import required Python code.
import roslib; roslib.load_manifest('hand_driver')
import rospy
import sys

from serial_bridge.msg import generic_serial


from hand_widget import HandWidget
from hand_driver.modules import ParserCommands
from hand_driver.modules import ParserSigns


class HandCalbrator():
    def sign_callback(self, sign):
        cmds = self.ps.parse([sign.data])
        if len(cmds) == 0:
            self.send_rest()
        else:
            for cmd in cmds:
                msg = generic_serial()
                msg.msg = [self.pc.parse(['set_all_motors'])[0]]
                for c in cmd:
                    msg.msg.append(cmd[c])
                self.serial_pub.publish(msg)
                rospy.sleep(0.5)

    def send_sign(self):
        msg = generic_serial()
        msg.msg = [self.pc.parse('set_all_motors')] + self.widget.get_scrolls()
        self.serial_pub.publish(msg)


    def send_rest(self):
        msg = generic_serial()
        msg.msg = [241, 180, 180, 180, 180, 180, 70, 90 ,50 ,120]
        self.serial_pub.publish(msg)

    def __init__(self):

        # get parameters
        self.output_topic = rospy.get_param('serial_topic', '/serial_topic');

        self.xml_hand = rospy.get_param('xml_hand', '/Users/ludus/Desktop/XML/robot_hand_Bulga.xml')
        self.xml_signs = rospy.get_param('xml_signs', '/Users/ludus/hydro_ws/src/parloma/parloma_hand/hand_driver/xml/signs2pose.xml')
        self.xml_commands = rospy.get_param('xml_commands', '/Users/ludus/Desktop/XML/commands_list.xml')

        self.ps = ParserSigns(self.xml_hand, self.xml_signs)
        self.pc = ParserCommands(self.xml_commands)

        # init topics
        self.serial_pub = rospy.Publisher(self.output_topic, generic_serial, queue_size=10)

        self.widget = HandWidget(9)
        self.widget.set_scrolls(100)
        self.widget.connect_button(self.send_sign)

        cmds = self.ps.parse(None)
        print cmds

        for sign in cmds.keys():
            cmd_dict = cmds[sign]
            for k in cmd_dict:
                cmd = []
                for c in cmd_dict[k]:
                    cmd.append(cmd_dict[k][c])
                    self.widget.add_config(sign + " - %s"%k, cmd)


        rospy.loginfo(rospy.get_caller_id() + " Node Initialized")
        self.widget.run()

if __name__ == '__main__':
    rospy.init_node('arduino_hand_calibrator', anonymous=True)
    try:
        ne = HandCalbrator()
    except rospy.ROSInterruptException: pass
