#define ANALOG_PINS 8
#define NO_MESSAGE -1
#define DISABLE 0
#define ENABLE 1
#define READ_SENSORS 2
#define READ_STATE 3

#define OUTPUT_PIN 12

int state = LOW;

void setup()
{
  Serial.begin(9600);
  pinMode(OUTPUT_PIN, OUTPUT);
}

void readState() {
  Serial.write(state);
}

void disable() {
  state = LOW;
  digitalWrite(OUTPUT_PIN, state);
  readState();
}

void enable() {
  state = HIGH;
  digitalWrite(OUTPUT_PIN, state);
  readState();
}

void readSensors() {
  for (int i = 0; i < ANALOG_PINS; i++) {
    Serial.write(analogRead(i));
  }
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
    default:
      break;
  }
}

void loop()
{
  delay(100);
  checkSerial();
}
