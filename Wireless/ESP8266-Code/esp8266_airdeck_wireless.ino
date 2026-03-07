#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

// --- Configuration ---
const char* ssid = "ssid here";
const char* password = "passwd here";
const char* targetIP = "IP here"; // Enter your computers's local IP address here
const int targetPort = 4210;

// Pin definitions for ESP8266 (e.g., NodeMCU or Wemos D1 Mini)
// Connect the other side of the buttons to GND
const int btnU = D1;
const int btnL = D2;
const int btnD = D3;
const int btnR = D4;

WiFiUDP udp;

int stateU = HIGH, stateL = HIGH, stateD = HIGH, stateR = HIGH;
int lastStateU = HIGH, lastStateL = HIGH, lastStateD = HIGH, lastStateR = HIGH;

void setup() {
  Serial.begin(115200);
  
  pinMode(btnU, INPUT_PULLUP);
  pinMode(btnL, INPUT_PULLUP);
  pinMode(btnD, INPUT_PULLUP);
  pinMode(btnR, INPUT_PULLUP);

  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected. IP: ");
  Serial.println(WiFi.localIP());
}

void sendPacket(const char* message) {
  udp.beginPacket(targetIP, targetPort);
  udp.write(message);
  udp.endPacket();
}

void loop() {
  stateU = digitalRead(btnU);
  stateL = digitalRead(btnL);
  stateD = digitalRead(btnD);
  stateR = digitalRead(btnR);

  // Button U
  if (stateU != lastStateU) {
    if (stateU == LOW) sendPacket("U"); else sendPacket("u");
    delay(50); // Debounce
  }
  // Button L
  if (stateL != lastStateL) {
    if (stateL == LOW) sendPacket("L"); else sendPacket("l");
    delay(50);
  }
  // Button D
  if (stateD != lastStateD) {
    if (stateD == LOW) sendPacket("D"); else sendPacket("d");
    delay(50);
  }
  // Button R
  if (stateR != lastStateR) {
    if (stateR == LOW) sendPacket("R"); else sendPacket("r");
    delay(50);
  }

  lastStateU = stateU;
  lastStateL = stateL;
  lastStateD = stateD;
  lastStateR = stateR;
}
