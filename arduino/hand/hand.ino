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
 */

#include <Servo.h> 

Servo indice;  
Servo medio;
Servo anulare;
Servo mignolo;
Servo pollice;
Servo polso;

int Sbyte, indiceByte, medioByte, anulareByte, mignoloByte, polliceByte, polsoByte;                

int pos = 0, migntemp=0;

void setup()
{
    indice.attach(13);
    medio.attach(12);
    anulare.attach(11);
    mignolo.attach(3);
    pollice.attach(2);
    polso.attach(4);

    Serial.begin(9600);
}


void loop()
{
    if (Serial.available() >= 7) {
        Sbyte = Serial.read();//byte inizio

        if (Sbyte == 255){
            indiceByte = Serial.read(); //pacchetto dati
            medioByte = Serial.read();
            anulareByte = Serial.read();
            mignoloByte = Serial.read();
            polliceByte =Serial.read();
            polsoByte = Serial.read();

            //pilotiamo i servo
            if(indiceByte>=0 && indiceByte<=180){
                indice.write(indiceByte);    
            }
            if(medioByte>=0 && medioByte<=180){
                medio.write(medioByte);    
            }
            if(anulareByte>=0 && anulareByte<=180){
                anulare.write(anulareByte);    
            }
            if(mignoloByte>=0 && mignoloByte<=180){
                migntemp=abs(mignoloByte-180);
                if(migntemp>160)
                    migntemp=160;
                if(migntemp<50)
                    migntemp=50;
                mignolo.write(migntemp);    
            }
            if(polliceByte>=0 && polliceByte<=180){
                pollice.write(polliceByte);    
            }
            if(polsoByte>=0 && polsoByte<=180){
                polso.write(polsoByte);    
            }
        }
    }
} 
