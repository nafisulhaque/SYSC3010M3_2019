#include <Stepper.h>
#include "DHT.h"

#define LEDPIN 12             // choose the pin for the LED
#define PIRPIN 2              // choose the input pin (for PIR sensor)
#define DHTPIN 7

#define STEPS 200             //Number of steps
#define DHTTYPE DHT11

Stepper stepper(STEPS, 8, 10, 9, 11); //Setting up stepper
DHT dht(DHTPIN, DHTTYPE);       //Setting up DHT

int pirActive = HIGH;              // activates PIR motion sensor
int blindsActive = HIGH;          // activates controls for blinds
int lightsActive = HIGH;          // activates control for lights


int pirState = LOW;               // we start, assuming no motion detected
int val = LOW;                    // variable for reading the pin status

int lightsOn = LOW;
int blindsOn = LOW;

int temp = 0;
int hum = 0;

int opCode;
int commCode;

unsigned long previousMillis  = 0;
unsigned long currentMillis   = 0;
unsigned long interval = 4000;

int i = 0;
void setup() {
  pinMode(LEDPIN, OUTPUT);      // declare LED as output
  pinMode(PIRPIN, INPUT);       // declare sensor as input
  stepper.setSpeed(60);         // set speed of stepper
  dht.begin();
  currentMillis = millis();
  Serial.begin(9600);           // start serial
}


void loop() {
  if (Serial.available() > 0) {
    parse_command();
    use_command();
  }

  if (pirActive == HIGH) {
    use_PIR(digitalRead(PIRPIN));
  }

  if ((currentMillis - previousMillis) >= interval) {
    humTempMonitor();
    opCodeGen(1);
    Serial.flush();
    previousMillis = currentMillis;
  }
  else {
    opCodeGen(0);
    Serial.flush();
    currentMillis = millis();
  }
}


void activateLB() {
  if (lightsActive == HIGH) {
    digitalWrite(LEDPIN, HIGH); // turn LED ON
    lightsOn = HIGH;
  }

  if (pirState == LOW && blindsActive == HIGH) {
    stepper.step(2048);       // turns the stepper once fully assuming it takes one turn to roll up blinds
    blindsOn = HIGH;
    pirState = HIGH;
  }
}

void deactivateLB() {
  if (lightsActive == HIGH) {
    digitalWrite(LEDPIN, LOW);  // turn LED OFF
    lightsOn = LOW;
  }
  if (pirState == HIGH && blindsActive == HIGH) {
    stepper.step(-2048);
    blindsOn = LOW;
    pirState = LOW;
  }
}

void use_PIR(int value) {
  if (value == HIGH) {
    activateLB();
  }
  else {
    deactivateLB();
  }
}


void humTempMonitor() {
  temp = int(dht.readTemperature());
  hum = int(dht.readHumidity());
}

void opCodeGen(int humTempRead) {
  String tempS;
  String humS;
  if (String(hum).length() < 2) {
    humS = "0" + String(hum);
  }
  else {
    humS = String(hum);
  }
  if (String(temp).length() < 2) {
    tempS = "0" + String(temp);
  }
  else {
    tempS = String(temp);
  }
  String opCodeS = String(pirActive) + String(lightsActive) + String(blindsActive) + String(lightsOn) + String(blindsOn) + tempS + humS + String(humTempRead);
  Serial.println(opCodeS);
}



void parse_command() {
  commCode = Serial.readString().toInt();
}

void use_command() {
  blindsOn = commCode % 10;
  lightsOn = (commCode / 10) % 10;
  blindsActive = (commCode / 100) % 10;
  lightsActive = (commCode / 1000) % 10;
  pirActive = (commCode / 10000) % 10;
}
