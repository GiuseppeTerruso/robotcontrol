/*
 * ParserRobot.cpp
 * Author: Bruna Galante
 *
 * This class handles the parsing of the xml file 'robot_hand'.
 *      
 */

#ifndef   PARSER_ROBOT
#define   PARSER_ROBOT

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/foreach.hpp>
#include <iostream>
#include <list>
#include <map>

#include "Converter.cpp"
#include "Joint.cpp"

#define ROOT_TAG_ROBOT  "robot"
#define INFORMATIONS_TAG "information"
#define HAND_TAG "hands"
#define RIGHT_TAG "right"
#define LEFT_TAG "left"
#define JOINT_TAG "joint"

//values of these tags can change according to the hand implementation
#define IMPLEMENTED_TAG "implemented"
#define CODE_TAG "code"

using namespace std;
using namespace boost::property_tree;

const short errorCode = -2;

class ParserRobot {

private:
	ptree _ptree, _root;
	list<string>* _validKeys;
	list<Joint*> * _rightHand;
	list<Joint*> * _leftHand;
	string _fileName;

public:
	ParserRobot(string fileName) :
			_fileName(fileName) {
		this->_rightHand = NULL;
		this->_leftHand = NULL;
		this->_validKeys = new list<string>();

		if (!this->_fillXMLTree()) {
			if (!this->_retrieveValidInformation()) {
				if (!this->_searchHands())
					cout << "Object ParserRobot rightly created!" << endl;

			}
		}
	}

	~ParserRobot() {
		if (this->_rightHand != NULL)
			delete this->_rightHand;
		if (this->_leftHand != NULL)
			delete this->_leftHand;
		delete this->_validKeys;
	}

private:
	short _fillXMLTree();
	short _retrieveValidInformation();
	short _loadJoints(ptree, list<Joint*>*);
	short _searchHands();
	map<short, int>* _parsePose(map<string, float>, list<Joint*>*);

public:
	list<map<short, int>*>* parsePoses(list<map<string, float> >, bool);
};

short ParserRobot::_fillXMLTree() {
	try {
		read_xml(this->_fileName, this->_ptree, xml_parser::no_comments);
		this->_root = _ptree.get_child(ROOT_TAG_ROBOT);
	} catch (xml_parser::xml_parser_error& exception) {
		cerr << "Something bad happened during parsing. Check the file name!!!"
				<< std::endl;
		cerr << exception.what() << endl;
		return errorCode;
	} catch (ptree_bad_path& exception) {
		cerr << "Bad path. XML file not correct." << endl;
		cerr << exception.what();
		return errorCode;
	} catch (...) {
		cerr << "Something bad happened." << endl;
		return errorCode;
	}
	return 0;
}

short ParserRobot::_retrieveValidInformation() {
	if (this->_root.empty())
		return errorCode;

	try {
		ptree node = this->_root.get_child(INFORMATIONS_TAG);
		BOOST_FOREACH(ptree::value_type& childNode,node) {
			string value = childNode.second.get<string>("");
			this->_validKeys->push_front(value);

		}
	} catch (ptree_bad_path& exception) {
		cerr << "Bad path. XML file not correct." << endl;
		cerr << exception.what();
		this->_validKeys->clear();
		return errorCode;
	} catch (...) {
		cerr << "Something bad happened." << endl;
		this->_validKeys->clear();
		return errorCode;
	}

	return 0;
}

short ParserRobot::_loadJoints(ptree node, list<Joint*>* listJoint) {
	list<string>::iterator it;
	map<string, string> informations;
	Joint* j;

	BOOST_FOREACH(ptree::value_type& val,node) {
		if (val.first == "<xmlattr>") //?
			continue;

		boost::optional<string> jointName = val.second.get_optional<string>(
				"<xmlattr>.name_id");
		if (!jointName.is_initialized()) {
			cerr << "Failed to parse one joint. Check the robot_hand.xml file."
					<< endl;
			continue;
		}

		for (it = this->_validKeys->begin(); it != this->_validKeys->end();
				it++) {
			boost::optional<string> information =
					val.second.get_optional<string>(*it);
			if (information.is_initialized()) {

				informations[*it] = information.get();
			}
		}

		j = new Joint(jointName.get(), informations);

		if (!j->checkValidXMLFormat(this->_validKeys)) {
			cerr << "Failed to parse one joint. Check the robot_hand.xml file."
					<< endl;
			continue;
		} else {
			map<string, string>::iterator itG = j->_informations->find(
					IMPLEMENTED_TAG);
			if (itG->second == "True") {
				listJoint->push_back(j);
			}

		}

		informations.clear();

	}
	return 0;
}

short ParserRobot::_searchHands() {
	try {
		ptree node = this->_root.get_child(HAND_TAG);

		try {
			ptree rightHand = node.get_child(RIGHT_TAG);
			this->_rightHand = new list<Joint*>();
			this->_loadJoints(rightHand, this->_rightHand);
		} catch (ptree_bad_path& exception) {
			this->_rightHand = NULL;
		}

		try {
			ptree leftHand = node.get_child(LEFT_TAG);
			this->_leftHand = new list<Joint*>();
			this->_loadJoints(leftHand, this->_leftHand);
		} catch (ptree_bad_path& exception) {
			this->_leftHand = NULL;
		}

	} catch (ptree_bad_path& exception) {
		cerr << "Bad path. XML file not correct." << endl;
		cerr << exception.what();
		return errorCode;
	}

	return 0;
}

map<short, int>* ParserRobot::_parsePose(map<string, float> pose,
		list<Joint*>* hand) {
	map<short, int>* tmpPose = NULL;
	Converter c;

	if (this->_ptree.empty())
		return tmpPose;

	list<Joint*>::iterator it;

	for (it = hand->begin(); it != hand->end(); it++) {
		Joint *j = *it;
		if (pose.find(j->getJointName()) != pose.end()) {
			float val = pose[j->getJointName()];
			string minRange = j->getValue("minrange");
			string maxRange = j->getValue("maxrange");
			string restPosition = j->getValue("restposition");
			string code = j->getValue(CODE_TAG);

			if (minRange.empty() || maxRange.empty() || restPosition.empty()
					|| code.empty()) {
				cerr << "XML file is not correct for joint: "
						<< j->getJointName();
				continue;
			}

			float minRangeN, maxRangeN, restPositionN;

			bool minR = c.StringToFloat(minRange, minRangeN);
			bool maxR = c.StringToFloat(maxRange, maxRangeN);
			bool rP = c.StringToFloat(restPosition, restPositionN);
			short codeN = (short) atoi(code.c_str());

			if (!minR || !maxR || !rP) {
				cerr
						<< "Something went wrong during conversion from string to float for joint: "
						<< j->getJointName() << endl;
				cerr << "Check XML file." << endl;
				continue;
			}

			float a, b, c;
			if (restPositionN == -1.0) {
				b = minRangeN;
				c = maxRangeN;
				if (val >= 0.0)
					a = val;
				else
					a = val + 1;
			} else {
				if (val >= 0.0) {
					a = val;
					b = maxRangeN;
					c = restPositionN;
				} else {
					a = val + 1;
					b = restPositionN;
					c = minRangeN;
				}
			}

			int cmdNum = (a * (b - c) + c) + 0.5; //for round float value

			if (tmpPose == NULL)
				tmpPose = new map<short, int>();

			tmpPose->insert(pair<short, int>(codeN, cmdNum));
		}
	}

	return tmpPose;
}

list<map<short, int>*>* ParserRobot::parsePoses(
		list<map<string, float> > posesList, bool isRight) {
	list<Joint*>* listJoint = NULL;

	if (this->_ptree.empty())
		return NULL;

	list<map<short, int>*>* poses = NULL;

	if (isRight && this->_rightHand == NULL) {
		cerr
				<< "Cannot perform the operation, because there is no implementation for right hand."
				<< endl;
		return NULL;
	} else if (isRight) {
		listJoint = this->_rightHand;
	}

	if (!isRight && this->_leftHand == NULL) {
		cerr
				<< "Cannot perform the operation, because there is no implementation for left hand."
				<< endl;
		return NULL;
	} else if (!isRight) {
		listJoint = this->_leftHand;
	}

	list<map<string, float> >::iterator it;
	for (it = posesList.begin(); it != posesList.end(); it++) {
		map<short, int>* pose = this->_parsePose(*it, listJoint);
		if (poses == NULL)
			poses = new list<map<short, int>*>();
		poses->push_back(pose);

	}

	return poses;
}

#endif











