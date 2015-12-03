#include "ros/ros.h"
#include "ros/package.h"
#include "serial_bridge/generic_serial.h"
#include "std_msgs/String.h"

#include <iostream>
#include <map>
#include <list>

#include "ParserRobot.cpp"
#include "ParserCommands.cpp"
#include "ParserSigns.cpp"

using namespace std;

#define SET_ALL "set_all_motors"

class HandDriver {

private:

	string xml_commands_list;
	string xml_sign_to_pose;
	string xml_hand;

	string input_topic;
	string output_topic;

	ParserSigns *ps = NULL;
	ParserCommands *pc = NULL;
	ParserRobot *pr = NULL;

	ros::Publisher pub;
	ros::Subscriber sub;
	

public:

	HandDriver(int argc, char ** argv) {

		string path = ros::package::getPath("parloma_driver");
		cout << "Path: " << path << endl;
		this->xml_commands_list = path + "/xml/commands_list.xml";
		this->xml_sign_to_pose = path + "/xml/signs2pose.xml";
		this->xml_hand = path + "/xml/robot_hand.xml";

		this->ps = new ParserSigns(xml_sign_to_pose);
		this->pc = new ParserCommands(xml_commands_list);
		this->pr = new ParserRobot(xml_hand);

		ros::init(argc, argv, "hand_driver", ros::init_options::AnonymousName);
		ros::NodeHandle nh("~");

		bool itParam = nh.getParam("input_topic", this->input_topic);
		bool otParam = nh.getParam("output_topic", this->output_topic);

		if (!itParam)
			input_topic = "/sign_topic";
		if (!otParam)
			output_topic = "/serial_topic";

		pub = nh.advertise<serial_bridge::generic_serial>(output_topic, 10);
		sub = nh.subscribe(this->input_topic, 10,
				&HandDriver::callbackFunction, this);
		ROS_INFO("Node is listening on topic: %s", this->input_topic.c_str());
		ROS_INFO("Node initialized.");

		ros::spin();

	}

	void callbackFunction(const std_msgs::String::ConstPtr& msg) {

		ros::Rate pausePose(1);
		string message = msg->data;

		ROS_INFO("Received message %s.", message.c_str());

		list<string> cmd;
		cmd.push_back(SET_ALL);
		map<string, int> code = this->pc->getCodeForCmds(cmd);

		for (int i = 0; i < message.length(); i++) {

			serial_bridge::generic_serial msg;
			msg.msg.push_back((uint8_t) code[SET_ALL]);
			string string2send(1, message[i]);

			if (string2send == " ")
				continue;

			list<map<string, float> > listOfPercentage = this->ps->returnPosesForSign(
					string2send, false);


			if( listOfPercentage.size() == 0 ){
				ROS_INFO("Sign %c will not be sent, error in retrieving percentages.", message[i]);
				continue;
			}

			list<map<short, int>* >* listOfPoses = this->pr->parsePoses(
								listOfPercentage, true);

			if( listOfPoses == NULL ){
				ROS_INFO("Sign %c will not be sent, error in computing poses.", message[i]);
				continue;
			}

			ROS_INFO("Poses for sign: %c", message[i]);
			cout<<"[";
			list<map<short, int>*>::iterator itN;
			for (itN = listOfPoses->begin(); itN != listOfPoses->end(); itN++) {
				cout << "{ ";
				map<short, int>::iterator itM;
				for (itM = (*itN)->begin(); itM != (*itN)->end(); itM++)
				{
						msg.msg.push_back((uint8_t) (*itM).second);
						cout << (*itM).first<< " : " << (*itM).second<<", ";
				}
				cout << " }; ";
				pub.publish(msg);

			}
			cout << "]"<<endl;
			pausePose.sleep();
		}
	}

};

int main(int argc, char **argv) {

	HandDriver hd(argc, argv);
}

