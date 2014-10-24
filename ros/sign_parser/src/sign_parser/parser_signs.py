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
#	 (CINI, www.consorzio-cini.it, www.consorzio-cini.it/index.php/en/lab-astech)

#    Contributors:
#        Giuseppe Airò Farulla (giuseppe.airofarulla@polito.it)

# Usage: python script_name 
# This script parses the XML files that list all the joints implemented in the considered 
# robot, the alphabet and the poses to assume to reproduce all the signs.

import xml.etree.ElementTree as ET
import sys
import numpy as np

class parser_signs:

	def __init__(self, XML_ROBOT, XML_SIGNS):

		self.XML_ROBOT = XML_ROBOT
		self.XML_SIGNS = XML_SIGNS

		# Try to access the XML files
		try:
			self.tree_robot = ET.parse(self.XML_ROBOT)
			self.root_robot = self.tree_robot.getroot()

			self.tree_signs = ET.parse(self.XML_SIGNS)
			self.root_signs = self.tree_signs.getroot()
		except: 
			# Valid XML files?!
			self.tree_robot = None
			self.root_robot = None
			self.tree_signs = None
			self.root_signs = None
			print "Unexpected error:", sys.exc_info()[0]

		# If valid XML files, try to retrieve the joints list and the alphabet
		# all_joint_list is the list of all the valid joints
		self.all_joints_list = []
		try:
			tmp_joints = self.root_signs.find("joints")
			for child in tmp_joints:
				self.all_joints_list.append(child.text)
			self.alph = self.root_signs.find("alphabet")
		except Exception as e: 
			# Correct XML file?!
			print e

	# Parse signs (that is a LIST of signs), returning a list of dictionaries with pairs (motor_code as int/string, motor_pose)
	def parse(self, signs):

		child = ""
		all_cmds_list = []

		if self.tree_robot is None or self.tree_signs is None:
			return []

		for sign in signs:
			try:
				# Is the sign s dynamic or not?
				s = self.alph.find(sign)
				dyn = s.attrib["dynamic"]
			except Exception as e: 
				# Correct XML file and valid sign?!
				print "For sign " + str(sign) + " encountered error " + str(e)
				print "Is it a valid sign?"
				continue

			# size is the number of rows in the matrix mat for the sign s
			# Please refer to the xml file for more detailed comments
			size = int(s.find("rowsN").text)
			mat = np.zeros((size, len(self.all_joints_list)), dtype=np.float)
			# Try to explore the rows with crescent ID -> a missing row_id should be a mistake?!

			rows_list = []
			for row_child in s:
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
				left_hand = hands.find("left")
				right_hand = hands.find("right")
				arms = self.root_robot.find("arms")
				left_arm = arms.find("left")
				right_arm = arms.find("right")
			except Exception as e:
				# Valid XML files?!
				print e
				return -1

			tmp_joints = hands.find("joints")
			if tmp_joints is not None:
				for joint_child in tmp_joints:
					if joint_child.text not in self.all_joints_list:
						print "WARNING: Hands are implementing joint " + str(joint_child.text) +\
							  " which is not in valid joints list from " + str(XML_SIGNS)

			tmp_joints = arms.find("joints")
			if tmp_joints is not None:
				for joint_child in tmp_joints:
					if joint_child.text not in self.all_joints_list:
						print "WARNING: Arms are implementing joint " + str(joint_child.text) +\
							  " which is not in valid joints list from " + str(XML_SIGNS)

			# Let"s look for implemented joints in the valid limbs
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

							# Map int(round(cmd_num)) to cmd[child.tag] to have pairs (motor_name_as_string, motor_pose) in the dictionaries
							#cmd[child.tag] = int(round(cmd_num))
							# Map int(round(cmd_num)) to cmd[int(child.find("code").text)] to have pairs (motor_code_as_int, motor_pose) 								in the dictionaries
							cmd[int(child.find("code").text)] = int(round(cmd_num))

					all_cmds_list.append(cmd)

		return all_cmds_list

# main
def main():
	print p.parse(["A","R"])

if __name__ == "__main__":
	if len(sys.argv) != 1:
		print "Usage: python script_name "
	else:
		main()
