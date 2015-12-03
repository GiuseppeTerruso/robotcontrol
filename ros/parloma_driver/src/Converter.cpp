/*
 * stringConverter.cpp

 *
 *  Created on: 22/mar/2015
 *      Author: bruna
 */

#ifndef   CONVERTER
#define   CONVERTER

#include <sstream>
#include <string>
#include <iostream>
#include <SerialStream.h>

using namespace std;

class Converter{

public:

static bool StringToFloat(string s, float& val)
{
  istringstream stream(s);
 return !(stream>>val).fail();
}

};



#endif

