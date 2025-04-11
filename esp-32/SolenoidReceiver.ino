//Solenoid Receiver Code 

#include <ESP8266WiFi.h>
#include <espnow.h>
#define RELAY_PIN D8 // If ESP8266 pin connected to the IN pin of relay

int open = 0;

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);  // Set the ESP8266 to station mode

  pinMode(RELAY_PIN, OUTPUT);

  // Initialize ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("ESP-NOW initialization failed!");
    return;
  }

  // Register the callback to receive data
  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {
  // The receiver will handle the incoming data via the callback function
  delay(1000);

  if (open == 1)
  {
    digitalWrite(RELAY_PIN, HIGH); // open solenoid valve 
  }
  else 
  {
    digitalWrite(RELAY_PIN, LOW); // close solenoid valve
  }
}

void OnDataRecv(uint8_t * mac, uint8_t *data, uint8_t len) {
  memcpy(&open, data, sizeof(open));  // Copy the received data into the variable
  Serial.print("Received data: ");
  Serial.println(open);  // Print the received data
}
