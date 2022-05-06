#include <WiFi.h>

const char* SSID = "LEO1_TEAM_04";
const char* password = "embeddedlinux";

void initWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, password);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi");
    delay(500);
  }
  Serial.println("Connected");
}