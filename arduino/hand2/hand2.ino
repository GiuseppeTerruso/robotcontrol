/*
    Copyright (C) 2014 Politecnico di Torino
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

    This software is developed within the PARLOMA project, which aims
    at developing a communication system for deablinf people (www.parloma.com)
    The PARLOMA project is developed with the Turin node of AsTech laboraroies
    network of Italian CINI (Consorzio Interuniversitario Nazionale di Informatica)

    Contributors:
        Ludovico O. Russo (ludovico.russo@polito.it)
        Andrea Bulgarelli
 */


#include <Servo.h>



enum motor_t {thumb_flex, index_flex, middle_flex, ring_flex, pinky_flex,
              thumb_abd, index_abd, middle_abd, wrist_1,  MOTOR_NUM
              };

class Motor{
  public:
    Motor(int pin, int pos = 0, int p_min = 0, int p_max = 180, bool direct = true);
    void reset();
    void move(int pos);
  private:
    Servo motor;
    int position;
    int p_max;
    int p_min;
    int pos_reset;
    bool direct;
};

Motor::Motor(int pin, int pos, int p_min, int p_max, bool direct):
    position(-1), p_max(p_max), p_min(p_min), direct(direct)
{
  if (pos >= 0 && pos <= 180) {
    pos_reset = pos;
  } else {
    pos_reset = 0;
  }
  this->motor.attach(pin);
  this->reset();
}

void Motor::reset() {
  this->move(pos_reset);
}

void Motor::move(int pos) {
   if (pos >= 0 && pos <= 180) {
   if (this->direct) pos = 180-pos;
    position = map(pos, 0, 180, p_min, p_max);
    motor.write(position);
  }
}

Motor *motors[MOTOR_NUM];


void allocate_motors() {
    motors[thumb_flex]  =   new Motor(  10,   0,  0,  180,  true);
    motors[index_flex]  =   new Motor(  12,   0,  0,  180,  true);
    motors[middle_flex] =   new Motor(  5,    0,  0,  180,  true);
    motors[ring_flex]   =   new Motor(  4,    0,  0,  180,  true);
    motors[pinky_flex]  =   new Motor(  3,    0,  0,  180,  true);
    motors[thumb_abd]   =   new Motor(  6,    0,  0,  180,  true);
    motors[index_abd]   =   new Motor(  11,   0,  0,  180,  true);
    motors[middle_abd]  =   new Motor(  2,    0,  0,  180,  true);
    motors[wrist_1]     =   new Motor(  8,    0,  0,  180,  true);
}

int Sbyte, indiceByte, medioByte, anulareByte, mignoloByte, polliceByte, polsoByte, adindiceByte, admedioByte, adpolliceByte;

char command; // 201 = control all fingers
              // 202 = control specific finger


int pos = 0, migntemp=0;

void setup()
{
  allocate_motors();
  Serial.begin(9600);
}


void loop()
{
  if (Serial.available() >= 10) {
    Sbyte = Serial.read();//byte inizio

    if (Sbyte == 245) {
      for (int i = 0; i < 9; i++) {
        motors[i]->move(Serial.read());
      }
    }
  }
}
