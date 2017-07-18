#include <EEPROM.h>

#define ANALOG_PINS 8
#define NO_MESSAGE -1
#define NOOP 0
#define DISABLE 1
#define ENABLE 2
#define READ_STATE 3
#define READ_SENSORS 4
#define ECHO 5
#define GET_SERIAL 32
#define SET_SERIAL 33

#define OUTPUT_PIN 12

#define SN_ADDR 0
#define STATE_ADDR 4

void setup()
{
  Serial.begin(9600);
  pinMode(OUTPUT_PIN, OUTPUT);
}

void readState() {
  Serial.write(EEPROM.read(STATE_ADDR));
}

void disable() {
  setAndRead(LOW);
}

void enable() {
  setAndRead(HIGH);
}

void setAndRead(int val) {
  EEPROM.write(STATE_ADDR, val);
  digitalWrite(OUTPUT_PIN, val);
  Serial.write(val);
}

void readSensors() {
  for (int i = 0; i < ANALOG_PINS; i++) {
    Serial.write(analogRead(i));
  }
}

void setSerialNumber() {
  int serialNumber = Serial.read();
  EEPROM.write(SN_ADDR, serialNumber);
  Serial.write(serialNumber);
}

void getSerialNumber() {
  Serial.write(EEPROM.read(SN_ADDR));
}

void checkSerial() {
  int serialValue = Serial.read();
  switch (serialValue) {
    case NO_MESSAGE:
      break;
    case DISABLE:
      disable();
      break;
    case ENABLE:
      enable();
      break;
    case READ_SENSORS:
      readSensors();
      break;
    case READ_STATE:
      readState();
      break;
    case GET_SERIAL:
      getSerialNumber();
      break;
    case SET_SERIAL:
      setSerialNumber();
      break;
    default:
      break;
  }
}

void loop()
{
  delay(100);
  checkSerial();
}
