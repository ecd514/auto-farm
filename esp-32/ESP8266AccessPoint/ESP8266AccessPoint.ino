#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

// Simulate sensor data
float ESP1t = 70.3;  // Example temp
float ESP1h = 60.7;  // Example humidity
float ESP1p = 7.1;  // Example pH

void handleRoot() {
  String htmlContent = "<h1>Sensor 1 Data</h1>";
  htmlContent += "<p>Temperature: " + String(ESP1t) + " °F</p>";
  htmlContent += "<p>Humidity: " + String(ESP1h) + " %</p>";
  htmlContent += "<p>pH: " + String(ESP1p) + " %</p>";
  
  // Send the response
  server.send(200, "text/html", htmlContent);
}

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

void loop() {
  server.handleClient();

}
