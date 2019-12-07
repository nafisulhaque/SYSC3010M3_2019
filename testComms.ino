String opCode;
int test = 1;
void setup() {
  Serial.begin(9600);
}

void loop() {
  switch (test) {
    case 1:
      testPIRActive(0);
      break;
    case 2:
      testPIRActive(1);
      break;
    case 3:
      testLedActive(0);
      break;
    case 4:
      testLedActive(1);
      break;
    case 5:
      testLed(0);
      break;
    case 6:
      testLed(1);
      break;
    case 7:
      testBlindsActive(0);
      break;
    case 8:
      testBlindsActive(1);
      break;
    case 9:
      testBlinds(0);
      break;
    case 10:
      testBlinds(1);
      break;
    case 11:
      testTempHum("4563");
      break;
    case 12:
      testTempHum("2550");
      break;
    case 13:
      testTempHum("2718");
      test = 0;
      break;
  }
  
  test++;
  delay(500);
}

void testPIRActive(int isActive) {
  if (isActive) {
    opCode = "100000000";
  }
  else {
    opCode = "000000000";
  }
  Serial.println(opCode);
}

void testLedActive(int isActive) {
  if (isActive) {
    opCode = "010000000";
  }
  else {
    opCode = "000000000";
  }
  Serial.println(opCode);
}

void testLed(int isOn) {
  if (isOn) {
    opCode = "000100000";
  }
  else {
    opCode = "000000000";
  }
  Serial.println(opCode);
}

void testBlindsActive(int isActive) {
  if (isActive) {
    opCode = "001000000";
  }
  else {
    opCode = "000000000";
  }
  Serial.println(opCode);
}

void testBlinds(int isOn) {
  if (isOn) {
    opCode = "000010000";
  }
  else {
    opCode = "000000000";
  }
  Serial.println(opCode);
}

void testTempHum(String tempHum) {
  String a = "00000";
  String b = tempHum;
  Serial.println(a + b);
}
