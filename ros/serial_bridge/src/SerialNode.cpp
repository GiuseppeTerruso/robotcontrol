#include "ros/ros.h"
#include "serial_bridge/generic_serial.h"

#include <SerialStream.h>
#include <iostream>

using namespace LibSerial;
using namespace std;

class SerialNode {

private:
	string arduinoPort;
	SerialStream arduino;
	int baudRate;
	string inputTopic;
	SerialStreamBuf::BaudRateEnum baud;
	ros::Subscriber sub;

public:
	SerialNode(int argc, char ** argv) {

		//AnonymousName-> add a random number at the end of the node name
		//to make it unique
		ros::init(argc, argv, "serial_node", ros::init_options::AnonymousName);
		ros::NodeHandle nh("~");

		bool portParam = nh.getParam("port", this->arduinoPort);
		bool baudRateParam = nh.getParam("baudrate", this->baudRate);
		bool inputTopicParam = nh.getParam("serial_topic", this->inputTopic);

		if (!portParam)
			this->arduinoPort = "/dev/ttyACM0";

		if (!baudRateParam) {
			this->baudRate = 9600;
			this->baud = SerialStreamBuf::BAUD_9600;
		} else {
			switch (this->baudRate) {
			case 9600:
				this->baud = SerialStreamBuf::BAUD_9600;
				break;
			case 19200:
				this->baud = SerialStreamBuf::BAUD_19200;
				break;
			case 38400:
				this->baud = SerialStreamBuf::BAUD_38400;
				break;
			case 57600:
				this->baud = SerialStreamBuf::BAUD_57600;
				break;
			default:
				this->baud = SerialStreamBuf::BAUD_9600;
				break;
			}
		}

		if(!inputTopicParam)
			this->inputTopic="/serial_topic";

		ROS_INFO("Port set on: %s", this->arduinoPort.c_str());
		ROS_INFO("Baudrate set on: %d",this->baudRate);

		this->arduino.SetBaudRate(this->baud);
		this->arduino.SetCharSize( SerialStreamBuf::CHAR_SIZE_8 );
		this->arduino.SetParity( SerialStreamBuf::PARITY_NONE );
		this->arduino.SetFlowControl( SerialStreamBuf::FLOW_CONTROL_NONE );

		this->arduino.Open(this->arduinoPort, ios_base::out);

		if (this->arduino.IsOpen()) {
			ROS_INFO("Node connected to serial port %s ad baudrate %d",
					this->arduinoPort.c_str(),this->baudRate);
		}

		else {
			ROS_INFO("Port %s not available. This node will be shutdown", this->arduinoPort.c_str());
			ros::shutdown();
		}

		this->sub=sub=nh.subscribe(this->inputTopic,1000,&SerialNode::callbackFunction,this);

		ROS_INFO("Node subscribed on topic: %s",this->inputTopic.c_str());
		ROS_INFO("Node initialized");

		ros::spin();
	}

	void callbackFunction(const serial_bridge::generic_serial::ConstPtr&);

	~SerialNode(){
			this->arduino.Close();
		}
};

void SerialNode::callbackFunction(const serial_bridge::generic_serial::ConstPtr& msg)
{


	  ROS_INFO("Received data on topic: %s",this->inputTopic.c_str());
	  char* values2send;
	  cout<<"[";
      for(int i=0; i<msg->msg.size();i++)
      {
       cout<<msg->msg[i]<<", ";
       values2send[i]=msg->msg[i];
      }
      cout<<"]"<<endl;

      if(!this->arduino.good())
      {
    	  this->arduino.Close();
    	  this->arduino.Open(this->arduinoPort);
    	  if(!this->arduino.IsOpen())
    	  {
  			ROS_INFO("Lost connection on Port %s. This node will be shutdown", this->arduinoPort.c_str());
            ros::shutdown();
    	  }
      }

      this->arduino.write(values2send,msg->msg.size());
      ROS_INFO("Data correctly sent to serial port");

}

int main(int argc, char ** argv) {
	SerialNode(argc, argv);
}
