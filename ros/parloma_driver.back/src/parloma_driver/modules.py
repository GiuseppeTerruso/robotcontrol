#!/usr/bin/python
# -*- coding: utf-8 -*-

#    Copyright (C) 2014 Politecnico di Torino
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

#    This software is developed within the PARLOMA project, which aims
#    at developing a communication system for deaf-blind people (www.parloma.com)
#    The PARLOMA project is developed within the Turin node of AsTech laboratories
#    network sponsored by Consorzio Interuniversitario Nazionale di Informatica
#     (CINI, www.consorzio-cini.it, www.consorzio-cini.it/index.php/en/lab-astech)

#    Contributors:
#        Giuseppe Airò Farulla (giuseppe.airofarulla@polito.it)
#        Ludovico Orlando Russo (ludovico.russo@polito.it)

# Usage: python script_name
# This script parses the XML file that lists all the command, with the relative codes,
# to control a given robotic actuator.

import xml.etree.ElementTree as ET
import numpy as np
import sys

# Code for non valid commands
NON_VALID = None

class ParserCommands():
    def __init__(self, XML_COMMAND):

        # Try to access the XML file
        self.XML_COMMAND = XML_COMMAND
        try:
            self.tree = ET.parse(self.XML_COMMAND)
            self.root = self.tree.getroot()
        except:
            # Valid XML file?!
            self.tree = None
            self.root = None
            print "Unexpected error:", sys.exc_info()[0]

        # If valid XML, try to retrieve the commands list
        self.commands_list = []
        try:
            tmp_list = self.root.find('list')
            for child in tmp_list:
                self.commands_list.append(child.text)
        except Exception as e:
            # Correct XML file?!
            print e


    # Parse cmds (that may be a LIST of commands or a single command),
    # returning a dictionary with pairs (command, code as int) or a single code, respectively.
    def parse(self, cmds):
        if self.root is None:
            # XML not parsed correctly
            return {}

        # If valid XML, try to retrieve the codes list
        try:
            codes = self.root.find('codes')
        except Exception as e:
            # Correct XML file?!
            print e
            return {}

        if isinstance(cmds, list):
            # If cmds is a list
            # Create the dictionary to store pairs command - code
            cmds_dict = {}

            # Loop over all the commands
            for cmd in cmds:
                if cmd not in self.commands_list:
                    # Command non valid
                    cmds_dict[cmd] = NON_VALID
                else:
                    # Fill, and return, the dictionary with valid pairs (command, code as int)
                    code = int(codes.find(cmd).text)
                    cmds_dict[cmd] = code
            return cmds_dict
            #return cmds_dict.values()

        elif isinstance(cmds, str):
            # If cmds is a string
            if cmds not in self.commands_list:
                # Command non valid
                code = NON_VALID
            else:
                # Fill, and return, the dictionary with valid pairs (command, code as int)
                code = int(codes.find(cmds).text)
            return code
        else:
            # Cmds is not valid
            return NON_VALID


class ParserSigns:

    def __init__(self, XML_ROBOT, XML_SIGNS):

        self.XML_ROBOT = XML_ROBOT
        self.XML_SIGNS = XML_SIGNS
        self.XML_HEADER =''

        # Try to access the XML files
        try:
            self.tree_robot = ET.parse(self.XML_ROBOT)
            self.root_robot = self.tree_robot.getroot()

            self.tree_signs = ET.parse(self.XML_SIGNS)
            self.root_signs = self.tree_signs.getroot()
            self.ALPHABET =   [sign.tag for sign in self.root_signs.find('alphabet')]
        except:
            # Valid XML files?!
            self.tree_robot = None
            self.root_robot = None
            self.tree_signs = None
            self.root_signs = None
            print "Unexpected error:", sys.exc_info()[0]

        # If valid XML files, try to retrieve the joints list and the alphabet
        # all_joint_list is the list of all the valid joints
        # all_joints_dict is the dictionary of pairs {valid_joint, min_value}
        # min_value is 0 or 1 for flexion/extension joints or ad/abduction joints, respectively
        # (max value is always 1) (values are in percentage)
        self.all_joints_list = []
        self.all_joints_dict = {}

        self.right_hand_joints_list = []
        hands = self.root_robot.find("hands")
        right_hand = hands.find("right")
        for child in right_hand:
            if child.find("implemented").text == "True":
                    self.right_hand_joints_list.append(child.tag)

        try:
            tmp_joints = self.root_signs.find("joints")
            for child in tmp_joints:
                self.all_joints_list.append(child.text)
                # Comment this row below to have all the possible joints from XML_SIGNS in the graphic interface
                if child.text in self.right_hand_joints_list:
                    self.all_joints_dict[child.text] = child.attrib["min"]

            self.alph = self.root_signs.find("alphabet")
        except Exception as e:
            # Correct XML file?!
            print e

    # Parse valid implemented joints for graphic XML editor
    def parse_joints(self):
        return self.all_joints_dict

    # Overwrites a single row (pose_idx) of a single sign (sing) with percentages described in dictionary
    # (percentages_dict) of pairs {joint, new_percentage}
    def edit_sign(self, sign, pose_idx, percentages_dict):
        if isinstance(sign, str) == False:
            # Input sign is not valid
            print "Input " + str(sign) + " is not valid."
            return -1
        if isinstance(pose_idx, int) == False:
            # Input pose_idx is not valid
            print "Input " + str(pose_idx) + " is not valid."
            return -1
        if isinstance(percentages_dict, dict) == False:
            # Input pose_idx is not valid
            print "Input " + str(percentages_dict) + " is not valid."
            return -1

        # If signs is a single char
        s = self.alph.find(sign)
        if s is None:
            # Correct XML file and valid sign?!
            return None

        size = int(s.find("rowsN").text)
        if pose_idx < 0 or pose_idx >= size:
            # Row index out of bounds
            print "For sign " + str(sign) + " there is no row " + str(pose_idx)
            return None

        # Search for the desired row
        rows_list = []
        for row_child in s:
            if row_child.tag == "row":
                rows_list.append(row_child)
        # When not found, cannot edit the row
        found = False
        row = ""
        for rr in rows_list:
            row = rr
            if int(row.attrib["row_id"]) == pose_idx:
                # Desired row found
                found = True
                break
        if found == False:
            # Desired row not found. Exit with error?!
            print "For sign " + str(sign) + " the row_id " + str(r) + " is missing!"
            return -1

        # Search for the desired joint(s)
        for joint in percentages_dict.keys():
            j = row.find(joint)

            tmp_j = joint in self.all_joints_list

            if j is None or tmp_j is False:
                print "For sign " + str(sign) + " and row_id " + str(pose_idx) + " the joint " + str(joint) + " does not exist."
                continue

            if joint not in self.all_joints_dict.keys():
                print "WARNING: Coherence error!"
                print "GUI asks for editing " + str(joint) + " which is not implemented."
                continue

            # If new value is coherent with joint limits, accept it and overwrite the old value
            if percentages_dict[joint] <= 1 and percentages_dict[joint] >= float(self.all_joints_dict[joint]):
                j.text = str(percentages_dict[joint])
                # TODO modify here single row without rewreiting the whole file
                #row.append(j)
            else:
                print "For sign " + str(sign) + " and row_id " + str(pose_idx) + " and joint " + str(joint) + "\
                     the value " + str(percentages_dict[joint]) + " is not within valid bounds."
                continue
        # If everything was OK, write the new xml and succeed
        # TODO rewriting all the XML, inner comments are lost!!!
        out_file = open(self.XML_SIGNS,"w")
        out_file.write(self.XML_HEADER)
        out_file.write("\n")
        out_file.write(ET.tostring(self.root_signs))
        out_file.close()

        return 0

    # Parse signs (that may be a LIST of signs or a single sign),
    # returning a dictionary of dictionaries of dictionaries with pairs {sign, {pose_idx, {motor_code as int/string, motor_pose}}}
    # or a dictionaries of dictionaries {pose_idx, {motor_code as int/string, motor_pose} respectively
    def parse(self, signs):
        if self.tree_robot is None or self.tree_signs is None:
            return {}

        if isinstance(signs, list):
            # If signs is a list
            all_signs_dict = {}
            for sign in signs:
                s = self.alph.find(sign)
                if s is None:
                    # Correct XML file and valid sign?!
                    continue
                all_signs_dict[sign] = self.parse_sign(s)
            return all_signs_dict

        elif isinstance(signs, str):
            # If signs is a single char
            s = self.alph.find(signs)
            if s is None:
                # Correct XML file and valid sign?!
                return None
            return self.parse_sign(s)
        else:
            # Parse all the signs
            all_signs_dict = {}
            for sign in self.ALPHABET:
                s = self.alph.find(sign)
                if s is None:
                    # Correct XML file and valid sign?!
                    print "Sign " + str(sign) + " not found."
                    print "Is it a valid sign?"
                    continue
                all_signs_dict[sign] = self.parse_sign(s)
            return all_signs_dict


    # Invoking (more than once, if needed) parsing for a single sign
    def parse_sign(self, sign):
        child = ""
        all_cmds_dict = {}
        # Is the sign dynamic or not?
        dyn = sign.attrib["dynamic"]

        # size is the number of rows in the matrix mat for the sign s
        # Please refer to the xml file for more detailed comments
        size = int(sign.find("rowsN").text)
        mat = np.zeros((size, len(self.all_joints_list)), dtype=np.float)
        # Try to explore the rows with crescent ID -> a missing row_id should be a mistake?!

        rows_list = []
        for row_child in sign:
            if row_child.tag == "row":
                rows_list.append(row_child)

        for r in range(size):
            # When not found, the row is an empty node
            found = False
            row = ""
            for rr in rows_list:
                row = rr
                if int(row.attrib["row_id"]) == r:
                    # Desired row found
                    found = True
                    break
            if found == False:
                # Desired row not found. Exit with error?!
                print "For sign " + str(sign) + " the row_id " + str(r) + " is missing!"
                continue

            # Checking row consistency and saving the desired wor (if valid)
            if len(row) != len(self.all_joints_list):
                print "ERROR: For sign " + str(sign) + " the row_id " + str(r) + " has incorrect length " + str(len(row))
                continue
            for child in row:
                try:
                    mat[r, self.all_joints_list.index(child.tag)] = float(child.text)
                except Exception as e:
                    print "ERROR: For sign " + str(sign) + " the row_id " + str(r) + " encountered error: " + str(e)
                    continue

        child = ""

        # Now the sign has been completely parsed
        # Check for which limb has been implemented in the robot
        try:
            # Here add roots for any possible future limb
            hands = self.root_robot.find("hands")
            arms = self.root_robot.find("arms")
        except Exception as e:
            # Valid XML files?!
            print e
            return -1

        if hands is not None:
            left_hand = hands.find("left")
            right_hand = hands.find("right")
            tmp_joints = hands.find("joints")
            if tmp_joints is not None:
                for joint_child in tmp_joints:
                    if joint_child.text not in self.all_joints_list:
                        print "WARNING: Hands are implementing joint " + str(joint_child.text) +\
                              " which is not in valid joints list from " + str(XML_SIGNS)


        if arms is not None:
            left_arm = arms.find("left")
            right_arm = arms.find("right")
            tmp_joints = arms.find("joints")
            if tmp_joints is not None:
                for joint_child in tmp_joints:
                    if joint_child.text not in self.all_joints_list:
                        print "WARNING: Arms are implementing joint " + str(joint_child.text) +\
                              " which is not in valid joints list from " + str(XML_SIGNS)

        # Let's look for implemented joints in the valid limbs
        for limb in [left_hand, right_hand, left_arm, right_arm]:
            if limb is None or "kinematic" not in limb.attrib:
                # Non implemented limb
                continue
            kin = limb.attrib["kinematic"]
            if kin == "True" and dyn == "False":
                # Considering only the final shape for a static sign when fingers anti-entanglement is implemented by the robot
                mat = mat[-1]

            # For any row in mat
            for cmd_row in range(mat.shape[0]):
                # cmd is the set of commands for the robot for any row of any sign, repored to the operating range of the robot
                cmd = {}

                # For any valid joint in that limb
                for child in limb:
                    if child.tag in self.all_joints_list and child.find("implemented").text == "True":
                        # Converting pose in working range for the joint:
                        # minrange - maxrange when there is no rest position
                        # otherwise, rest position - maxrange when val pose is in 0 - 1
                        # otherwise, minrange - rest position

                        val = mat[cmd_row, self.all_joints_list.index(child.tag)]
                        rp = float(child.find("restposition").text)

                        if rp == -1.:
                            b = float(child.find("minrange").text)
                            c = float(child.find("maxrange").text)
                            if val >= 0.:
                                a = val
                            else:
                                a = val + 1
                        else:
                            if val >= 0.:
                                a = val
                                b = float(child.find("maxrange").text)
                                c = rp
                            else:
                                a = val + 1
                                b = rp
                                c = float(child.find("minrange").text)

                        cmd_num = a * (b - c) + c

                        # Map int(round(cmd_num)) to cmd[child.tag] to have pairs
                        # (motor_name_as_string, motor_pose) in the dictionaries
                        # cmd[child.tag] = int(round(cmd_num))

                        # Map int(round(cmd_num)) to cmd[int(child.find("code").text)]
                        # to have pairs (motor_code_as_int, motor_pose) in the dictionaries
                        cmd[int(child.find("code").text)] = int(round(cmd_num))

                #all_cmds_list.append(cmd)
                all_cmds_dict[cmd_row] = cmd

        return all_cmds_dict
