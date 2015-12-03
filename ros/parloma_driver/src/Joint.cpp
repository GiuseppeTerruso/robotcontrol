/*
 * Joint.cpp
 *
 *      Author: Bruna Galante
 */

#ifndef   JOINT
#define   JOINT

#include <list>
#include <map>
#include <iostream>

using namespace std;

class Joint{

public:
	map<string,string>* _informations;
	string _jointName;


public:

	Joint(string jointName,map<string,string> mapInfo)
	{
		this->_jointName=jointName;
		_informations=new map<string,string>(mapInfo);

	}

	~Joint()
	{
		delete this->_informations;
	}


	bool checkValidXMLFormat(list<string>* listKey)
	{
		if(this->_jointName=="")
			return false;

		if(listKey->size()!=this->_informations->size())
			return false;

		list<string>::iterator it;
		for(it=listKey->begin(); it!=listKey->end(); it++)
		{
			if(this->_informations->find(*it)==this->_informations->end())
				return false;
		}

		return true;
	}

	string getValue(string keyValue)
	{
		string value;
		if(this->_informations->find(keyValue)!=this->_informations->end())
			value=this->_informations->find(keyValue)->second;
		return value;
	}

	string getJointName()
	{
		return this->_jointName;
	}

};

#endif


