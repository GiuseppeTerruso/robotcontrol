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

# Usage: python script_name 
# This script parses the XML file that lists all the command, with the relative codes,
# to control a given robotic actuator.

import xml.etree.ElementTree as ET
import sys

# Code for non valid commands
NON_VALID = -1

class parser_command():

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

    # Parse cmds (that is a LIST of commands), returning a dictionary with pairs (command, code as int)
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
        return cmds_dict.values()


# main
def main():
    p = parser_command(XML_COMMAND)
    print p.parse(['set_all_motors','set_one_motor', 'lol'])

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print "Usage: python script_name "
    else:
        main()
