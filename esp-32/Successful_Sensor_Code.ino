#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <espnow.h>

// Set up pins and rs485
#define MAX485_DE_RE D1           // Digital pin D1 (GPIO5) used to control DE/RE
SoftwareSerial rs485(D5, D6);     // RX = D5 (GPIO14), TX = D6 (GPIO12)

// Original DFRobot sensor command and measurement variables
uint8_t Com[8] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x04, 0x44, 0x09};

// Receiver MAC Address
uint8_t broadcastAddress[] = {0x40, 0x91, 0x51, 0x58, 0x82, 0xB9};
// 40:91:51:58:82:B9

// Set your Board ID 
#define BOARD_ID 1

// Structure to send data, same format as receiver  
float tem, hum, ph;
typedef struct struct_message {
    int id;
    float tem;
    float hum;
    float ph;
} struct_message;

struct_message myData; 

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
  // Begin debug serial communication at 9600 baud
  Serial.begin(9600);

  // Start RS485 Software Serial
  rs485.begin(9600);

  // Initialize MAX485 control pin
  pinMode(MAX485_DE_RE, OUTPUT);
  digitalWrite(MAX485_DE_RE, LOW);  // Set to receive mode to start

  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  // Init ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  } 
  // Set ESP-NOW role
  esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);

  // Once ESPNow is successfully init, we will register for Send CB to
  // get the status of Trasnmitted packet
  esp_now_register_send_cb(OnDataSent);
  
  // Register peer
  esp_now_add_peer(broadcastAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);
}

void loop() {
  // Read sensor data from RS485 device 
  readHumiturePH();

  delay(1000);

  // Send sensor data
  myData.id = BOARD_ID;
  myData.tem = tem; 
  myData.hum = hum; 
  myData.ph = ph; 
  esp_now_send(0, (uint8_t *) &myData, sizeof(myData));

  // Output the sensor readings to the debug Serial Monitor
  Serial.print("TEM = ");
  Serial.print(tem, 1);
  Serial.print(" °C  HUM = ");
  Serial.print(hum, 1);
  Serial.print(" %RH  PH = ");
  Serial.println(ph, 1);
  delay(1000);
}

// Function to handle reading sensor data over RS485
void readHumiturePH() {
  uint8_t Data[13] = {0};
  uint8_t ch = 0;
  bool flag = true;

  while(flag) {

   delay(100);

   // Switch MAX485 to transmit mode to send the command
   digitalWrite(MAX485_DE_RE, HIGH);
   rs485.write(Com, 8);
   rs485.flush();

   // Return to receive mode so we can read sensor response
   digitalWrite(MAX485_DE_RE, LOW);

   // Allow sensor time to respond
   delay(10);  

   if (readN(&ch, 1) == 1) {
     if (ch == 0x01) {
       Data[0] = ch;
       if (readN(&ch, 1) == 1) {
         if (ch == 0x03) {
           Data[1] = ch;
           if (readN(&ch, 1) == 1) {
             if (ch == 0x08) {
               Data[2] = ch;
               if (readN(&Data[3], 10) == 10) {
                 // Validate the message using CRC16: if valid extract the sensor values.
                 if (CRC16_2(Data, 11) == (Data[11] * 256 + Data[12])) {
                   // Parse data to proper units (check your sensor datasheet for scaling)
                   hum = (Data[3] * 256 + Data[4]) / 10.0;
                   tem = (Data[5] * 256 + Data[6]) / 10.0;
                   ph  = (Data[9] * 256 + Data[10]) / 10.0;
                   flag = false; // Successfully read a valid data packet.
                 }
               }
             }
           }
         }
       }
     }
   }

   rs485.flush();  // Clear any remaining data from the RS485 buffer

  }
}

// Read N bytes from rs485 into a buffer with timeout support.
// Returns the number of bytes read.
uint8_t readN(uint8_t *buf, size_t len) {
  size_t offset = 0;
  long start = millis();

  while ((millis() - start < 500) && (offset < len)) {
   if (rs485.available()) {
     buf[offset++] = rs485.read();
     start = millis(); // Reset timeout after each received byte
   }
  }
  return offset;
}


// CRC16 calculation function (unchanged from original code)
unsigned int CRC16_2(unsigned char *buf, int len) {
  unsigned int crc = 0xFFFF;
  for (int pos = 0; pos < len; pos++) {
   crc ^= (unsigned int)buf[pos];
   for (int i = 8; i != 0; i--) {
     if ((crc & 0x0001) != 0) {
       crc >>= 1;
       crc ^= 0xA001;
     } else {
       crc >>= 1;
     }
   }
  }
  // Swap low/high byte as per original implementation
  return ((crc & 0x00FF) << 8) | ((crc & 0xFF00) >> 8);
 }