/* Encoder Test for Robo-team 1
 *  Nicolas Fredrickson
 *  Steven Coronel
 *  October 26th, 2017
 */

// we can achieve a 90 degree turn via 450/1088 turns
 
//The sample code for driving one way motor encoder
const byte encoder0pinA = 2;//2;//A pin -> the interrupt pin 2
const byte encoder0pinB = 3;//3;//B pin -> the digital pin 3

const byte encoder1pinA = 18;//18;//A pin -> the interrupt pin 18
const byte encoder1pinB = 19;//19;//B pin -> the digital pin 19

byte encoder0PinALast;
int duration0;//the number of the pulses
boolean Direction0;//the rotation Direction0 

byte encoder1PinALast;
int duration1;//the number of the pulses
boolean Direction1;//the rotation Direction0 

int loops;

#include <Servo.h>

//#define ROTATION 663 // According to manual
//#define ROTATION 398  // According to tests?
#define ROTATION 1326 //1326?????
// .413603
#define ROTATIONS_PER_90_DEGREES  450/1088

#define NINETY_DEGREE_RIGHT 1000

#define NINETY_DEGREE_LEFT  1000

#define CIRC 136 * PI

// .322051
#define PIP_DIST (CIRC) / ROTATION



#define PRINT_EVERY 5000//25 

#define ENC_0_NEG_SLOW 90
#define ENC_0_NEG_FAST 180//180  

#define ENC_0_POS_SLOW 80
#define ENC_0_POS_FAST 0//0

Servo ST0, ST1;

int state = 0;

void setup()
{  
  Serial.begin(9600);//Initialize the serial port
  EncoderInit();//Initialize the module
  
  ST0.attach( 9, 1000, 2000);
  ST1.attach(10, 1000, 2000);

  loops = 0;

  ST0.write(60);
  ST1.write(60);
  delay(10);

  duration0 = 0;
  duration1 = 0;
}
  
void loop()
{
  if(state == 0)
  	Drive(1000);
  else if(state == 1)
	turn90_right();
  else if(state == 2)
	turn90_left();
}

void Drive(int distance){
  if( ((duration0 + duration1) / 2) * PIP_DIST >= distance){
    ST0.write(85);
    ST1.write(85);
    delay(10);

    Serial.print(duration0);
    Serial.print(" ");
    Serial.println(duration1);

    duration0 = 0;
    duration1 = 0;

    state++;
  }
}

// left FORWARD, right BACKWARD
void turn90_left()
{

  ST0.write(65);
  ST1.write(105);
  delay(10);
  
  while(duration0 < NINETY_DEGREE_RIGHT)
  {   
    Serial.println(duration0);
  }

  ST0.write(85);
  ST1.write(85);
  delay(10);

  duration0 = 0;
  duration1 = 0;
  
  state++;
}
  
void turn90_right()
{
  ST0.write(105);
  ST1.write(65);
  delay(10);
  
  while(duration1 < NINETY_DEGREE_LEFT)
  {   
  	Serial.println(duration1);
  }

  ST0.write(85);
  ST1.write(85);
  delay(10);
  
  duration0 = 0;
  duration1 = 0;
  
  state++;
}

void EncoderInit()
{
  Direction0 = true;//default -> Forward
  Direction1 = true;//default -> Forward   
  pinMode(encoder0pinB,INPUT);
  pinMode(encoder1pinB,INPUT);  
  attachInterrupt(digitalPinToInterrupt(encoder0pinA), wheelSpeed0, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoder1pinA), wheelSpeed1, CHANGE);
}
  
void wheelSpeed0()
{
  int Lstate0 = digitalRead(encoder0pinA);
  if((encoder0PinALast == LOW) && Lstate0==HIGH)
  {
    int val0 = digitalRead(encoder0pinB);
    if(val0 == LOW && Direction0)
      Direction0 = false; //Reverse
    else if(val0 == HIGH && !Direction0)
      Direction0 = true;  //Forward
  }
  encoder0PinALast = Lstate0;
  
  if(!Direction0)  duration0++;
  else  duration0--;
}

void wheelSpeed1()
{
  int Lstate1 = digitalRead(encoder1pinA);
  if((encoder1PinALast == LOW) && Lstate1==HIGH)
  {
    int val1 = digitalRead(encoder1pinB);
    if(val1 == LOW && Direction1)
      Direction1 = false; //Reverse
    else if(val1 == HIGH && !Direction1)
      Direction1 = true;  //Forward
  }
  encoder1PinALast = Lstate1;
  
  if(!Direction1)  duration1++;
  else  duration1--;
}

// left BACKWARD, right FORWARD
void turn90CounterClock()
{
}

