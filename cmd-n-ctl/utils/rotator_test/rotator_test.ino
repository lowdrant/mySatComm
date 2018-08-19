/**
 * Rotator test script for mySatComm using
 * A4988 Stepper Motor Controller breakout board
 * and an optoisolator controlling a servo.
 * 
 * connect Pin12 to STEP
 * connect Pin13 to DIRECTION
 * connect Pin9 to SERVO
 * Author: Marion Anderson
 * Date: 2018-08-11
 */
#include <Servo.h>
const int dir_pin = 13;
const int step_pin = 12;
bool clockwise = true;
Servo testServo;
int pos = 0;
int posstep = 5;

void setup()
{
  pinMode(dir_pin, OUTPUT);
  pinMode(step_pin, OUTPUT);
  testServo.attach(9);
  Serial.begin(9600);
}

void loop()
{
  // Switch direction command
  if (Serial.available()) {
    int incoming = Serial.read();
    if (incoming == '-') {
      clockwise = !clockwise;
      Serial.print("Changing direction to ");
      if (clockwise) {
        Serial.println("clockwise!");
      } else {
        Serial.println("counter clockwise!");
      }
    }
  }

  // Direction control
  if (clockwise) {
    digitalWrite(dir_pin, LOW);
  } else {
    digitalWrite(dir_pin, HIGH);
  }
  delayMicroseconds(1);  // 200ns setup t
  
  // Step motor
  digitalWrite(step_pin, HIGH);
  delayMicroseconds(3);  // 1us setup time
  digitalWrite(step_pin, LOW);
  delayMicroseconds(3);
  Serial.println("Step!");

  testServo.write(pos);
  if (pos+posstep > 180 || pos+posstep < 0) {
    posstep *= -1;
  }
  pos += posstep;
  Serial.print("pos: ");
  Serial.println(pos);
  delay(30);  // wait between steps

  
}
