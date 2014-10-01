
import controlP5.*;
import processing.serial.*;  

Serial serial;

ControlP5 cp5;

int myColorBackground = color(0,0,0);
int knobValue = 100;

int serialPortNumber = 0;

Knob indice;
Knob medio;
Knob anulare;
Knob mignolo;
Knob pollice;
Knob polso;
Knob adindice;
Knob admedio;
Knob adpollice;

//Ordine di posizione all'interno del comando alla porta seriale
//1. indice
//2. medio
//3. anulare
//4. mignolo
//5. pollice
//6. polso
//7. adindice
//8. admedio
//9. adpollice

//Lista di comandi per fare le lettere secondo l'ordine naturale (NB diverso da serial)
// che è pollice indice medio anulare mignolo polso adpollice adindice admedio
//A 180 0 0 180 0 90 180 90 70
//B 0 180 180 0 180 100 90 90 90
//C 110 130 110 70 180 90 30 90 90
//D 35 180 0 180 0 90 30 90 90
//E 40 0 45 160 90 90 145 90 90
//F 90 40 180 0 180 90 150 90 90
//I 20 0 0 180 180 90 20 90 90
//L 180 180 0 180 0 90 0 90 90
//P 0 70 0 180 0 90 0 90 90
//R soloindice a 50 -> 90 130 100 90 90 90 90 40 120
//S 180 180 0 180 0 90 0 90 90
//U 0 180 180 180 0 90 0 90 90
//V 0 180 180 180 0 90 0 120 60
//W 0 180 0 180 0 90 0 90 90
//X 40 70 45 160 90 90 160 90 90
//Y 180 0 0 180 180 90 0 90 90

//int[][] signs = {{180,0,0,180,0,90,180,90,70},{0,180,180,0,180,100,90,90,90},{110,130,110,70,180,90,30,90,90},{35,180,0,180,0,90,30,90,90},{40,0,45,160,90,90,145,90,90},{90,40,180,0,180,90,150,90,90},{20,0,0,180,180,90,20,90,90},{180,180,0,180,0,90,0,90,90},{0,70,0,180,0,90,0,90,90},{180,180,0,180,0,90,0,90,90},{0,180,180,180,0,90,0,90,90},{0,180,180,180,0,90,0,120,60},{0,180,0,180,0,90,0,90,90},{40,70,45,160,90,90,160,90,90},{180,0,0,180,180,90,0,90,90}};

void setup() {
  println("Setup...");
  println(Serial.list());
  String port = Serial.list()[serialPortNumber];
  serial = new Serial(this, port, 9600);
  serial.clear();
  delay(2000);
  serial.clear();
  println("Setup 1 done!");
  
  size(700,400);
  smooth();
  noStroke();
  
  cp5 = new ControlP5(this);
  
  indice = cp5.addKnob("indice")
               .setRange(0,180)
               .setValue(90)
               .setPosition(200,70)
               .setRadius(50)
               .setDragDirection(Knob.VERTICAL)
               ;
               
               
   medio = cp5.addKnob("medio")
               .setRange(0,180)
               .setValue(90)
               .setPosition(300,70)
               .setRadius(50)
               .setDragDirection(Knob.VERTICAL)
               ;
               
   anulare = cp5.addKnob("anulare")
               .setRange(0,180)
               .setValue(90)
               .setPosition(400,70)
               .setRadius(50)
               .setDragDirection(Knob.VERTICAL)
               ;
                
   mignolo = cp5.addKnob("mignolo")
               .setRange(0,180)
               .setValue(90)
               .setPosition(500,70)
               .setRadius(50)
               .setDragDirection(Knob.VERTICAL)
               ;   
             
   pollice = cp5.addKnob("pollice")
               .setRange(0,180)
               .setValue(90)
               .setPosition(100,70)
               .setRadius(50)
               .setDragDirection(Knob.VERTICAL)
               ;  
               
   polso = cp5.addKnob("polso")
               .setRange(0,180)
               .setValue(90)
               .setPosition(400,250)
               .setRadius(50)
               .setDragDirection(Knob.VERTICAL)
               ;
   adindice = cp5.addKnob("adindice")
               .setRange(0,180)
               .setValue(90)
               .setPosition(200,250)
               .setRadius(50)
               .setDragDirection(Knob.VERTICAL)
               ;
    admedio = cp5.addKnob("admedio")
               .setRange(0,180)
               .setValue(90)
               .setPosition(300,250)
               .setRadius(50)
               .setDragDirection(Knob.VERTICAL)
               ;             
   adpollice = cp5.addKnob("adpollice")
               .setRange(0,180)
               .setValue(90)
               .setPosition(100,250)
               .setRadius(50)
               .setDragDirection(Knob.VERTICAL)
               ;   
  //Setto le pose di partenza per mano aperta          
 /* indice(160);
  anulare(10);
  pollice(170);
  adindice(90);
  adpollice(10);
  medio(170);
  mignolo(170);
  polso(90);
  admedio(70);*/
  
  
  
//  serial.write(241);
//  serial.write(160);
//  serial.write(10);
//  serial.write(170);
//  serial.write(90);
//  serial.write(10);
//  serial.write(170);
//  serial.write(170);
//  serial.write(90);
//  serial.write(80);
  
  println("Setup 2 done!");
}

void draw() {
  background(myColorBackground);
  fill(knobValue);
  rect(0,height/2,width,height/2);
  fill(0,100);
  //rect(80,40,140,320);
}

void setposefromnaturalorder(int[] values) {
  /*indice(values[1]);
  anulare(values[3]);
  pollice(values[0]);
  adindice(values[7]);
  adpollice(values[6]);
  medio(values[2]);
  mignolo(values[4]);
  polso(values[5]);
  admedio(values[8*/
}

void indice(int indiceValue) {
  myColorBackground = color(indiceValue);
    serial.write(242);
    serial.write(1);
    serial.write(indiceValue);
  println("indice a: "+indiceValue +"gradi");
}

void medio(int medioValue) {
  myColorBackground = color(medioValue);
    serial.write(242);
    serial.write(2);
    serial.write(medioValue);
  println("medio a: "+medioValue +"gradi");
}

void anulare(int anulareValue) {
  myColorBackground = color(anulareValue);
    serial.write(242);
    serial.write(3);
    serial.write(anulareValue);
  println("anulare a: "+anulareValue +"gradi");
}

void mignolo(int mignoloValue) {
  myColorBackground = color(mignoloValue);
    serial.write(242);
    serial.write(4);
    serial.write(mignoloValue);
  println("mignolo a: "+mignoloValue +"gradi");
}

void pollice(int polliceValue) {
  myColorBackground = color(polliceValue);
    serial.write(242);
    serial.write(0);
    serial.write(polliceValue);
  println("pollice a: "+polliceValue +"gradi");
}

void polso(int polsoValue) {
  myColorBackground = color(polsoValue);
    serial.write(242);
    serial.write(8);
    serial.write(polsoValue);
  println("polso a: "+polsoValue +"gradi");
}

void adindice(int adindiceValue) {
  myColorBackground = color(adindiceValue);
    serial.write(242);
    serial.write(6);
    serial.write(adindiceValue);
  println("adindice a: "+adindiceValue +"gradi");
}

void admedio(int admedioValue) {
  myColorBackground = color(admedioValue);
    serial.write(242);
    serial.write(7);
    serial.write(admedioValue);
  println("admedio a: "+admedioValue +"gradi");
}

void adpollice(int adpolliceValue) {
  myColorBackground = color(adpolliceValue);
    serial.write(242);
    serial.write(5);
    serial.write(adpolliceValue); 
  println("adpollice a: "+adpolliceValue +"gradi");
}

void performRest(){
 /* indice(160);
  anulare(10);
  pollice(170);
  adindice(90);
  adpollice(10);
  medio(170);
  mignolo(170);
  polso(90);
  admedio(70);*/
}

void perform_a(){
  /*
  mignolo(180); 
  delay(500);
  anulare(180);
  delay(500);
  
    indice(160);

  pollice(170);
  delay(500);
  adindice(90);
  delay(500);
  adpollice(10);
    delay(500);
  medio(170);
    delay(500);

    delay(500);
  polso(90);
    delay(500);
  admedio(70);
  */
}


void keyPressed() {
  switch(key) {
    case('1'):serial.write(245);break;
    case('2'):serial.write(247);break;
    case('c'):serial.write(246);break;
    case('a'):perform_a();break;
  } 
}
