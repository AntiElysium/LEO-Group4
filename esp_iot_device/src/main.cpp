#include <Arduino.h>
#include <WiFi_Config.h>
#include <MQTT.h>

int lowThreshold = 700;
int mediumThreshold = 1500;
int highThreshold = 3000;

uint8_t PIN = 32;
int loops = 0;

void blink() {
  for (int i = 1; i <= loops; i++) {
    digitalWrite(PIN, HIGH);
    delay(500);
    digitalWrite(PIN, 0);
    delay(500);
  }
  delay(2000);
}

void lowBlinkCallback(byte* message, unsigned int length) {
  char payload[length];
  memcpy(payload, message, length);
  payload[sizeof message] = 0; //Null termination
  lowThreshold = atoi(payload);
}

void mediumBlinkCallback(byte* message, unsigned int length) {
  char payload[length];
  memcpy(payload, message, length);
  payload[sizeof message] = 0; //Null termination
  mediumThreshold = atoi(payload);
}

void highBlinkCallback(byte* message, unsigned int length) {
  char payload[length];
  memcpy(payload, message, length);
  payload[sizeof message] = 0; //Null termination
  highThreshold = atoi(payload);
}

void checkThresholds(byte* message, unsigned int length) {
  char* payload = (char*) (message);

  char* ptr = strtok(payload, ",");
  
  int co2Level = atoi(ptr);

  if (highThreshold < co2Level) {
    loops = 3;
  } else if (mediumThreshold < co2Level) {
    loops = 2;
  } else if (lowThreshold < co2Level) {
    loops = 1;
  } else {
    loops = 0;
  }

}

void setup() {
  pinMode(PIN, OUTPUT);

  // put your setup code here, to run once:
  Serial.begin(115200);
  initWifi();
  initMQTT();

  subscribeToTopic("leo1-04/project/threshold/low", lowBlinkCallback);
  subscribeToTopic("leo1-04/project/threshold/middle", mediumBlinkCallback);
  subscribeToTopic("leo1-04/project/threshold/high", highBlinkCallback);

  subscribeToTopic("big_bouncing_inflatable_green_ball", checkThresholds);
}

void loop() {
  // put your main code here, to run repeatedly:
  loopMQTT();
  if (loops != 0) {
    blink();
  }
}