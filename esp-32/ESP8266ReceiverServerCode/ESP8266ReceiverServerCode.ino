/*
  ECD 514 
  Lauren Frye 
  ESP8266 Receiver/Server Code
*/

#include <ESP8266WiFi.h>
#include <espnow.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

// Structure to receive data, same format as sender 
typedef struct struct_message {
    int id;
    int temp;
    int humidity;
    int pH;
} struct_message;

// Create a struct_message called myData
struct_message myData;

// Create a structure to hold the data recieved from each board
struct_message board1;
struct_message board2;
struct_message board3;

// Create an array with the three structures
struct_message boardsStruct[3] = {board1, board2, board3};

// Process data when recieved 
void OnDataRecv(uint8_t * mac_addr, uint8_t *incomingData, uint8_t len) {
  char macStr[18];
  Serial.print("Packet received from: ");
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.println(macStr);
  memcpy(&myData, incomingData, sizeof(myData));
  Serial.printf("Board ID %u: %u bytes\n", myData.id, len);
  // Update the structures with the new incoming data
  boardsStruct[myData.id-1].temp = myData.temp;
  boardsStruct[myData.id-1].humidity = myData.humidity;
  boardsStruct[myData.id-1].pH = myData.pH;
  Serial.printf("Temperature value: %d \n", boardsStruct[myData.id-1].temp);
  Serial.printf("Humidity value: %d \n", boardsStruct[myData.id-1].humidity);
  Serial.printf("pH value: %d \n", boardsStruct[myData.id-1].pH);
  Serial.println();
}
 
void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);
  
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  // Initialize ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Setting ESP-NOW role 
  esp_now_set_self_role(ESP_NOW_ROLE_SLAVE);
  esp_now_register_recv_cb(OnDataRecv);

  // Access point setup 
  delay(1000);
  Serial.print("Configuring access point...");
  WiFi.softAP(ssid, password);
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");
}

// Text to be sent to web server
void handleRoot() {
  String htmlContent = "<h1>Sensor 1 Data</h1>";
  htmlContent += "<p>Temperature: " + String(ESP1t) + " °F</p>";
  htmlContent += "<p>Humidity: " + String(ESP1h) + " %</p>";
  htmlContent += "<p>pH: " + String(ESP1p) + " %</p>";
  
  htmlContent += "<h1>Sensor 2 Data</h1>";
  htmlContent += "<p>Temperature: " + String(ESP2t) + " °F</p>";
  htmlContent += "<p>Humidity: " + String(ESP2h) + " %</p>";
  htmlContent += "<p>pH: " + String(ESP2p) + " %</p>";

  htmlContent += "<h1>Sensor 3 Data</h1>";
  htmlContent += "<p>Temperature: " + String(ESP3t) + " °F</p>";
  htmlContent += "<p>Humidity: " + String(ESP3h) + " %</p>";
  htmlContent += "<p>pH: " + String(ESP3p) + " %</p>";

  tmlContent += "<h1>Sensor 4 Data</h1>";
  htmlContent += "<p>Temperature: " + String(ESP4t) + " °F</p>";
  htmlContent += "<p>Humidity: " + String(ESP4h) + " %</p>";
  htmlContent += "<p>pH: " + String(ESP4p) + " %</p>";

  // Send the response
  server.send(200, "text/html", htmlContent);
}

// Setting up the server 
void setup() {
  
  delay(1000);
  Serial.begin(115200);
  Serial.println();
  Serial.print("Configuring access point...");

  WiFi.softAP(ssid, password);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");
}

void loop(){
  // Access the variables for each board
  int ESP1t = boardsStruct[0].temp;
  int ESP1h = boardsStruct[0].humidity;
  int ESP1p = boardsStruct[0].pH;

  int ESP2t = boardsStruct[1].temp;
  int ESP2h = boardsStruct[1].humidity;
  int ESP2p = boardsStruct[1].pH;

  int ESP3t = boardsStruct[2].temp;
  int ESP3h = boardsStruct[2].humidity;
  int ESP3p = boardsStruct[2].pH;

// This ESP
  int ESP4t = //*sensor data*
  int ESP4h = //*sensor data*
  int ESP4p = //*sensor data*

  server.handleClient();  
}





