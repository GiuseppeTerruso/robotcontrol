#include <iostream>

#ifndef   SIGN
#define   SIGN

using namespace std;

class Sign {

private:
	string _signName;
	short _numRows;
	bool _dynamic;

public:
	Sign(string sN, short nR, bool dynamic) :
			_signName(sN), _numRows(nR), _dynamic(dynamic) {
	};

	string getSignName() {
		return this->_signName;
	}

	bool getDynamic() {
		return this->_dynamic;
	}

	short getNumRows(){
		return this->_numRows;
	}
};

#endif
