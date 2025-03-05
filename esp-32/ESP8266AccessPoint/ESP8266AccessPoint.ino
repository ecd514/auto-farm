#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

// Count value for testing purposes 
int count = 0; 

// Simulate sensor data
float ESP1t = 50.3;  // Example temp
float ESP1h = 45.7;  // Example humidity
float ESP1p = 3.1;  // Example pH

// Network name and password
const char* ssid = "ESP8266AP";
const char* password = "laurenfrye";

void handleRoot() {
  String htmlContent = "<!DOCTYPE html><html><head>";
  htmlContent += "<script>";
  htmlContent += "setTimeout(function(){ location.reload(); }, 5000);";  // Refresh every 5 seconds
  htmlContent += "</script>";
  htmlContent += "</head><body>";
  htmlContent += "<h1>Sensor 1 Data</h1>";
  htmlContent += "<p>Temperature: " + String(ESP1t) + " &degF</p>";
  htmlContent += "<p>Humidity: " + String(ESP1h) + " %</p>";
  htmlContent += "<p>pH: " + String(ESP1p) + " </p>";
  
  // Send the response
  server.send(200, "text/html", htmlContent);
}

void setup() {
  
  delay(1000);
  Serial.begin(115200);
  Serial.println();
  Serial.println("Configuring access point...");

  WiFi.softAP(ssid, password);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();

  delay(1000);

  // Testing logic for updating sensor values 
  // Changing every 5 seconds
  if ((count % 5) == 0)
  {
    ESP1t = ESP1t + 3;
    ESP1h = ESP1h + 2;  
    ESP1p = ESP1p + 1; 
    Serial.print("Temperature: ");
    Serial.println(ESP1t);
    Serial.print("Humidity: ");
    Serial.println(ESP1h);
    Serial.print("pH: ");
    Serial.println(ESP1p);
  }
  count++; 
}
