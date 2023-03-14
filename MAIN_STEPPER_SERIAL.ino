#include <AccelStepper.h>


// Direction pin is connected to Digital 9 (CW)
// Pulse pin is connected to Digital 8 (CLK)

// Motor 1 Definition
const int stepPin = 8;
const int dirPin = 9;
AccelStepper stepper(1, 8, 9);
// Pulse pin is connected to Digital 8 (CLK)
// Direction pin is connected to Digital 9 (CW)

const int STEPS_PER_REVOLUTION = 3200;
const float DEGREES_PER_STEP = 360.0 / STEPS_PER_REVOLUTION;
const float ANGLE_RANGE = 180.0;
const int SPEED_FACTOR = 1000;
float currentAngle = 0.0; // initialize current angle to 0
const int MAXSPEED =40000;
const byte numChars = 32;
char receivedChars[numChars]; // an array to store the received data
boolean newData = false;

void setup() {
  // Set the maximum speed and acceleration of the stepper motor
  stepper.setMaxSpeed(MAXSPEED);
  stepper.setAcceleration(40000);

  Serial.begin(2000000); // initialize serial communication
  Serial.println("<Arduino is ready>");
}

void loop() {
  recvWithEndMarker(); // receive data
  if (newData == true) { // if new data is available
    String input(receivedChars); // convert receivedChars array to String
    input.trim(); // remove any whitespace
    int datain = input.toInt();

    if (datain < 91){
      digitalWrite(dirPin, HIGH);
      stepper.move(1);
    }
    else if (datain >91){
      digitalWrite(dirPin, LOW);
      stepper.move(1);
    }
    newData = false; // reset newData flag
  }
  
  stepper.run();
}


void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;
 
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    }
    else {
      receivedChars[ndx] = '\0'; // terminate the string
      ndx = 0;
      newData = true; // set newData flag
    }
  }
}
