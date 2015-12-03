#include "ros/ros.h"
#include "std_msgs/String.h"

#include <iostream>

using namespace std;

class KeyboardInput {

private:
	string outputTopic;
	ros::Publisher pub;

public:

	KeyboardInput(int argc, char **argv) {

		ros::init(argc, argv, "keyboard_node",
				ros::init_options::AnonymousName);
		ros::NodeHandle nh("~");

		bool otParam = nh.getParam("output_topic", this->outputTopic);
		if (!otParam)
			this->outputTopic = "/sign_topic";

		pub = nh.advertise<std_msgs::String>(this->outputTopic, 1000);
		ROS_INFO("Data will be published on topic %s",
				this->outputTopic.c_str());

		ros::Rate loop_rate(10);

		std_msgs::String msg;

		while (ros::ok()) {
			cout<<"Insert a word or letter: ";
			cin>>msg.data;
			pub.publish(msg);
			ROS_INFO("Data %s published on topic %s", msg.data.c_str(),this->outputTopic.c_str());

			loop_rate.sleep();

		}

	}
};

int main(int argc, char **argv) {

	KeyboardInput ki(argc,argv);
}

