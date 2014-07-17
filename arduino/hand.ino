#include <Servo.h>

Servo indice;
Servo medio;
Servo anulare;
Servo mignolo;
Servo pollice;
Servo polso;

int Sbyte, indiceByte, medioByte, anulareByte, mignoloByte, polliceByte, polsoByte;
int pos = 0, migntemp=0;


int all_control() {
    indiceByte      =   Serial.read();
    medioByte       =   Serial.read();
    anulareByte     =   Serial.read();
    mignoloByte     =   Serial.read();
    polliceByte     =   Serial.read();
    polsoByte       =   Serial.read();


    //servo control
    if(indiceByte>=0 && indiceByte<=180){
        indice.write(indiceByte)
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
            all_control();
        }
    }
}
