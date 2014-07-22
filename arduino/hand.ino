/*
Copyright (c) 2014 CINI Consorzio Interuniversitario Nazionale di Informatica

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Contributors:
        Ludovico Russo
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
