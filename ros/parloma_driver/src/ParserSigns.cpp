/*
 * ParserSigns.cpp
 *
 *      Author: Bruna Galante
 *
 * This class handles the parsing of the xml file 'sign2pose'.
 */

#ifndef   PARSER_SIGNS
#define   PARSER_SIGNS

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/foreach.hpp>
#include <iostream>
#include <list>
#include <map>

#include "Converter.cpp"

#include "Sign.cpp"

using namespace std;
using namespace boost::property_tree;

#define ROOT_TAG_SIGNS "signs"
#define JOINTS_TAG "joints"
#define ALPHABET_TAG "alphabet"
#define SIGN_TAG "sign"
#define ROWNUM_TAG "rowsN"
#define ROW_TAG "row"

#define errorCode -1

class ParserSigns {
private:
	ptree _ptree, _root, _joints, _alphabet;
	list<Sign>* _implementedSigns;
	string _fileName;
	short _loadSigns();
	short _fillXMLTree();

public:
	ParserSigns(string fileName) :
			_fileName(fileName) {
		this->_implementedSigns = new list<Sign>();
		this->_fillXMLTree();
		this->_loadSigns();
		cout << "Object ParserSigns rightly created!" << endl;
	}
	;

	~ParserSigns() {
		delete this->_implementedSigns;
	}

private:
	map<string, float> _parseRow(ptree);
	short _isInAlphabet(string);

public:
	list<map<string, float> > returnPosesForSign(string, bool);
	list<string>* getImplementedSigns();
	


};

short ParserSigns::_fillXMLTree() {
	try {
		read_xml(this->_fileName, this->_ptree, xml_parser::no_comments);
		this->_root = _ptree.get_child(ROOT_TAG_SIGNS);
		this->_alphabet = this->_root.get_child(ALPHABET_TAG);
		this->_joints = this->_root.get_child(JOINTS_TAG);
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

short ParserSigns::_loadSigns() {
	if (this->_alphabet.empty())
		return errorCode;

	bool value;

	BOOST_FOREACH(ptree::value_type& childNode,this->_alphabet) {
		boost::optional<string> signName =
				childNode.second.get_optional<string>("<xmlattr>.name_id");
		boost::optional<string> dynamic = childNode.second.get_optional<string>(
				"<xmlattr>.dynamic");
		if (dynamic.get() == "False")
			value = false;
		else
			value = true;
		ptree subtree = (ptree) childNode.second;
		BOOST_FOREACH(ptree::value_type& child,subtree) {
			if (child.first == "rowsN") {
				short numR = child.second.get<short>("");
				Sign s(signName.get(), numR, value);
				this->_implementedSigns->push_front(s);
			}
		}

	}

	return 0;
}


list<string>* ParserSigns::getImplementedSigns() {
	list<string>* implSigns = new list<string>();
	list<Sign>::iterator it;
	for (it = this->_implementedSigns->begin();
			it != this->_implementedSigns->end(); it++) {
		string sName = (*it).getSignName();
		implSigns->push_back(sName);
	}

	return implSigns;
}

map<string, float> ParserSigns::_parseRow(ptree node) {
	map<string, float> mapPose;
	BOOST_FOREACH(ptree::value_type& child,node) {
		string jointName = child.first;

		if (jointName == "<xmlattr>") //?
			continue;

		string valuePose = child.second.get<string>("");
		float value;
		Converter c;
		c.StringToFloat(valuePose, value);

		mapPose[jointName] = value;
	}

	return mapPose;
}

list<map<string, float> > ParserSigns::returnPosesForSign(string sign,
		bool kinematic) {
	list<map<string, float> > listPosesForSign;
	short numRows = this->_isInAlphabet(sign);

	BOOST_FOREACH(ptree::value_type& child,this->_alphabet) {
		boost::optional<string> signValue = child.second.get<string>(
				"<xmlattr>.name_id");
		if (signValue.get() == sign) {
			ptree childNode = (ptree) child.second;
			for (int count = 0; count < numRows; count++) {
				BOOST_FOREACH(ptree::value_type& ch,childNode) {
					if (ch.first == ROW_TAG) {
						boost::optional<short> rowNum = ch.second.get<short>(
								"<xmlattr>.row_id");
						if (rowNum.get() == count) {
							map<string, float> poseMap = this->_parseRow(
									(ptree) ch.second);
							listPosesForSign.push_back(poseMap);
						}
					}
				}
			}
		}

	}

	if (kinematic) {
		list<Sign>::iterator it;
		for (it = this->_implementedSigns->begin();
				it != this->_implementedSigns->end(); it++) {
			if (it->getSignName() == sign && !it->getDynamic()) {
				//only last pose
				map<string, float> last = listPosesForSign.back();
				listPosesForSign.clear();
				listPosesForSign.push_back(last);
			}
		}
	}

	return listPosesForSign;
}

short ParserSigns::_isInAlphabet(string sign){
list<Sign>::iterator it;
	for (it = this->_implementedSigns->begin();
			it != this->_implementedSigns->end(); it++) {
		string sName = (*it).getSignName();
		if (sName == sign)
			return (*it).getNumRows();
	}
	return errorCode;
}

#endif
