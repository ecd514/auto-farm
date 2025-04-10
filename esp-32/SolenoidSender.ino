// HOST Code
// Sensor Data Reciever (hosting web server)
// Solenoid Data Sender (getting data from Pi)

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <espnow.h>

ESP8266WebServer server(80);

// Network name and password
const char* ssid = "ESP8266";
const char* password = "laurenfrye";

uint8_t broadcastAddress[] = { 0x2C, 0x3A, 0xE8, 0x39, 0x4C, 0xCD }; // Solenoid receiver MAC address
// 2C:3A:E8:39:4C:CD

// Variable controlling solenoid on/off
int open;  

// Structure to receive data, same format as sender 
float tem1, hum1, ph1;
typedef struct struct_message {
    int id;
    float tem;
    float hum;
    float ph;
} struct_message;

// Create a struct_message called myData
struct_message myData;

// Create a structure to hold the data recieved from each board
struct_message board1;
struct_message board2;

// Create an array with the three structures
struct_message boardsStruct[2] = {board1, board2};

void handleSolenoidOn() {
  digitalWrite(LED_BUILTIN, LOW);  // Turn ON (ESP's LED is active-low)
  open = 1;
  server.send(200, "text/plain", "Solenoid ON");
}

void handleSolenoidOff() {
  digitalWrite(LED_BUILTIN, HIGH); // Turn OFF
  open = 0;
  server.send(200, "text/plain", "Solenoid OFF");
}

// Callback function that will be executed when data is received
void OnDataRecv(uint8_t * mac_addr, uint8_t *incomingData, uint8_t len) {
  char macStr[18];
  Serial.print("Packet received from: ");
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.println(macStr);
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.printf("Board ID #%u: %u bytes\n", myData.id, len);
  // Update the structures with the new incoming data
  boardsStruct[myData.id-1].tem = myData.tem;
  boardsStruct[myData.id-1].hum = myData.hum;
  boardsStruct[myData.id-1].ph = myData.ph;
  Serial.printf("Sensor # %u ", myData.id);
  Serial.println();
  Serial.printf("Temperature value: %.2f \n", boardsStruct[myData.id-1].tem);
  Serial.printf("Humidity value: %.2f \n", boardsStruct[myData.id-1].hum);
  Serial.printf("pH value: %.2f \n", boardsStruct[myData.id-1].ph);
  Serial.println();
}

void handleRoot() {
  String htmlContent = "<!DOCTYPE html><html><head>";
  htmlContent += "<script>";
  htmlContent += "setTimeout(function(){ location.reload(); }, 5000);";  // Refresh every 5 seconds
  htmlContent += "</script>";
  htmlContent += "</head><body>";
  if (open == 0)
  {
    htmlContent += "<p>*Solenoid Valve Closed*</p>";
  }
  if (open == 1)
  {
    htmlContent += "<p>*Solenoid Valve Open*</p>";
  }
  htmlContent += "<h1>Sensor 1 Data</h1>";
  htmlContent += "<p>Temperature: " + String(boardsStruct[0].tem, 2) + " &degC</p>";
  htmlContent += "<p>Humidity: " + String(boardsStruct[0].hum, 2) + " %</p>";
  htmlContent += "<p>pH: " + String(boardsStruct[0].ph, 2) + " </p>";
  htmlContent += "<h1>Sensor 2 Data</h1>";
  htmlContent += "<p>Temperature: " + String(boardsStruct[1].tem, 2) + " &degC</p>";
  htmlContent += "<p>Humidity: " + String(boardsStruct[1].hum, 2) + " %</p>";
  htmlContent += "<p>pH: " + String(boardsStruct[1].ph, 2) + " </p>";
  
  
  // Send the response
  server.send(200, "text/html", htmlContent);
}

// Callback when data is sent
void OnDataSent(uint8_t *mac_addr, uint8_t sendStatus) {
  Serial.print("\r\nLast Packet Send Status: ");
  if (sendStatus == 0){
    Serial.println("Delivery success");
  }
  else{
    Serial.println("Delivery fail");
  }
}

void setup() {
  delay(1000);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);  // Set the ESP8266 to station mode
  WiFi.disconnect();

  // Server for Aidan to connect to 
  Serial.println();
  Serial.println("Configuring access point...");
  WiFi.softAP(ssid, password);
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");

  // Initialize ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("ESP-NOW initialization failed!");
    return;
  }

  // Set ESP-NOW role
  esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);

  // Once ESPNow is successfully init, we will register for Send CB to
  // get the status of Transmitted packet
  esp_now_register_send_cb(OnDataSent);
  // Register peer
  esp_now_add_peer(broadcastAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);
  // Register for a callback function that will be called when data is received
  esp_now_register_recv_cb(esp_now_recv_cb_t(OnDataRecv));
}

void loop() {

  server.handleClient();
  delay(2000);

  // Send message via ESP-NOW
  esp_now_send(0, (uint8_t *) &open, sizeof(open));
}
