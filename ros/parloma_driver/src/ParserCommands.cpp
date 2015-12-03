/*
 * Author: Bruna Galante
 * The methods of this class do the parsing of the XML file that list
 * all the commands implemented in a given robotic actuator.
 */

#ifndef   PARSER_COMMANDS
#define   PARSER_COMMANDS

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/foreach.hpp>
#include <iostream>
#include <list>
#include <map>

using namespace std;
using namespace boost::property_tree;

#define ROOT_TAG_COMMANDS "commands"
#define COMMAND_LIST_TAG "list"
#define COMMAND_NAME_VALUE_TAG "value"
#define CODES_LIST_TAG "codes"

/*
 * If something wrong happened during the execution of a function
 * is returned an error code (-1 is not used, because in the XML file this value
 * represent a command that is not yet implemented in the robot).
 */


class ParserCommands{

private:

	const short errorCode=-2;

	/* The name of the XML file */
	string fileName=NULL;
	/* XML tree objects */
	ptree _ptree,_root;
	/*list of the command's name saved in the file*/
	list<string>* _cmdList;

public:
	/*
	 * Constructor for the ParserCommands class
	 */
	ParserCommands(string fileName):fileName(fileName){
		_cmdList=new list<string>();
		if(!this->_fillXMLTree()){
		 this->_retrieveCommandLists();
		 cout << "Object ParserCommands rightly created!" << endl;
		}
		else
		 cerr<<"Cannot load commands"<<endl;
	}

	~ParserCommands(){
		delete _cmdList;
	}

	map<string,int> getCodeForCmds(list<string>);

private:

	short _retrieveCommandLists();
	short _parseCommand(string);
	short _fillXMLTree();

};

/*@brief Documentation for function fillXMLTree
 *
 * This functions reads the XML file and fill the struct _ptree,
 * from which will be retrieved the information about the commands.
 */

short ParserCommands::_fillXMLTree()
{
	try{
		read_xml(this->fileName,this->_ptree,xml_parser::no_comments);
		this->_root=_ptree.get_child(ROOT_TAG_COMMANDS);
	}catch (xml_parser::xml_parser_error& exception) {
		cerr<<"Something bad happened during parsing. Check the file name!!!"<<std::endl;
		cerr<<exception.what()<<endl;
		return errorCode;
	}catch (ptree_bad_path& exception){
		cerr<<"Bad path. XML file not correct."<<endl;
		cerr<<exception.what();
		return errorCode;
	}catch(...)
	{
		cerr<<"Something bad happened."<<endl;
		return errorCode;
	}

	return 0;
}

/*
 * This function reads all the commands from the XML file and saved
 * them into the list _cmdList.
 * This function should not be invoked directly.
 */
short ParserCommands::_retrieveCommandLists()
{
	if(this->_root.empty())
		return errorCode;

	try{
		ptree node=this->_root.get_child(COMMAND_LIST_TAG);
		BOOST_FOREACH(ptree::value_type& childNode,node)
		{
			string value=childNode.second.get<string>("");
			this->_cmdList->push_front(value);

		}
	}catch (ptree_bad_path& exception){
		cerr<<"Bad path. XML file not correct."<<endl;
		cerr<<exception.what();
		this->_cmdList->clear();
		return errorCode;
	}catch(...)
	{
		cerr<<"Something bad happened."<<endl;
		this->_cmdList->clear();
		return errorCode;
	}

	return 0;
}

short ParserCommands::_parseCommand(string cmd)
{
	short code=errorCode;

	if(this->_root.empty())
		return errorCode;

	try{
		ptree codes=this->_root.get_child(CODES_LIST_TAG);
		BOOST_FOREACH(ptree::value_type& node,codes)
		{
			if(node.first==cmd)
				code=node.second.get<short>("");
		}
	}catch(ptree_bad_path& exception)
	{
		cerr<<"Bad path. XML file not correct."<<endl;
		cerr<<exception.what();
		return errorCode;
	}catch(...)
	{
		cerr<<"Something bad happened."<<endl;
		return errorCode;
	}

	return code;
}

map<string,int> ParserCommands::getCodeForCmds(list<string> lstCmd)
{
	map<string,int> cmdCode;
	list<string>::iterator it;
	for(it=lstCmd.begin(); it!=lstCmd.end(); it++)
	{
		short code=this->_parseCommand(*it);
		if(code==errorCode)
			cerr<<"Error: code not found for command: "<<*it<<endl;
		else
			cmdCode[*it]=code;
	}
	return cmdCode;
}

#endif


