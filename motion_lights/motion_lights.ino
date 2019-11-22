#include <Stepper.h>

#define LEDPIN 13             // choose the pin for the LED
#define PIRPIN 2              // choose the input pin (for PIR sensor)


#define STEPS 200             //Number of steps

Stepper stepper(STEPS, 8, 10, 9, 11); //Setting up stepper


int pirState = LOW;             // we start, assuming no motion detected
int val = 0;                    // variable for reading the pin status
int blindsActive = 1;           // activates controls for blinds
int lightsActive = 1;
int timer = 0;
String command;
void setup() {
  pinMode(LEDPIN, OUTPUT);      // declare LED as output
  pinMode(PIRPIN, INPUT);     // declare sensor as input
  stepper.setSpeed(60);         // set speed of stepper
 // dht.begin();
  Serial.begin(9600);           // start serial
}
 
void loop(){
  val = digitalRead(PIRPIN);  // read input value
  
  if (Serial.available() > 0) {
    command = Serial.readString();
    }
  if (command == "Lights off") {
    lightsActive = 0;
    Serial.println(command);
  }
  if (val == HIGH){
    lightsOn();
  }
  else {
    lightsOff();
  }
}


void lightsOn() {
            // check if the input is HIGH
    if (lightsActive == 1) {
      digitalWrite(LEDPIN, HIGH); // turn LED ON
    }
    if (pirState == LOW && blindsActive == HIGH) {      
      stepper.step(2048);       // turns the stepper once fully assuming it takes one turn to roll up blinds
      pirState = HIGH;
      Serial.println(pirState);   // for use by controller
      
    }
  }
  
void lightsOff() {
  digitalWrite(LEDPIN, LOW);  // turn LED OFF
    if (pirState == HIGH && blindsActive == 1 && val == LOW){
      stepper.step(-2048);    
      pirState = LOW;
      Serial.println(pirState);// for use by the controller
    }
  }
