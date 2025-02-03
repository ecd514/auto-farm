/*
  WiFiAccessPoint.ino creates a WiFi access point and provides a web server on it.
*/

#include <WiFi.h>
#include <NetworkClient.h>
#include <WiFiAP.h>

// Set these to your desired credentials.
const char *ssid = "espAP";
const char *password = "laurenfrye";

NetworkServer server(80);

void setup() {

  Serial.begin(115200);
  Serial.println();
  Serial.println("Configuring access point...");

  // You can remove the password parameter if you want the AP to be open.
  // a valid password must have more than 7 characters
  if (!WiFi.softAP(ssid, password)) {
    log_e("Soft AP creation failed.");
    while (1);
  }
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  server.begin();

  Serial.println("Server started");
}

void loop() {
  NetworkClient client = server.accept();  // listen for incoming clients

  if (client) {                     // if you get a client,
    Serial.println("New Client.");  // print a message out the serial port
    client.print("You have successfully connected to the ESP32's access point! Hooray!");
    client.stop();
    Serial.println("Client Disconnected.");
  }
}


// pinging command capability 
// library to ping? if needed 
// meshing esps together, creating network of nodes 
// esps scan for networks, one "blooms" and starts the network, the others will connect to it, count down and when hit 0, start network if doesn't already exist 

