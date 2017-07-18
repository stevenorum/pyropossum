#define DISABLE 1
#define ENABLE 2

void setup() {Serial.begin(9600);}

void setPin(int val) {
  int pin = Serial.read();
  pinMode(pin, OUTPUT);
  digitalWrite(pin, val);
  Serial.write(pin);
}

void disable() {setPin(LOW);}

void enable() {setPin(HIGH);}

void loop() {
  delay(50);
  switch (Serial.read()) {
    case DISABLE:
      disable();
      break;
    case ENABLE:
      enable();
      break;
    default:
      break;
  }
}