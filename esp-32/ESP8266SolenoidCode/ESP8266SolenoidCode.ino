/*
    ESP8266 Solenoid Valve Code 
    Lauren Frye 
*/

#define RELAY_PIN D8 // If ESP8266 pin connected to the IN pin of relay

// The setup function runs once on reset or power-up
void setup() {

  // initialize the digital pin A5 as an output.
  pinMode(RELAY_PIN, OUTPUT);

}

void loop() {

  digitalWrite(RELAY_PIN, HIGH); // open valve 5 seconds, for example
  delay(5000);
  digitalWrite(RELAY_PIN, LOW);  // close valve 5 seconds, for example
  delay(5000);

}
