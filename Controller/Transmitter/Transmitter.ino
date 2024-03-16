#include <BluetoothSerial.h>

const char* deviceName = "ESP32-Joystick"; // Bluetooth device name
BluetoothSerial SerialBT;

String receiverMACadd = "24:DC:C3:98:9E:F0";
uint8_t address[6]  = {0x24, 0xDC, 0xC3, 0x98, 0x9E, 0xF0};
String receiverName = "ESP32-Motors"; 
bool connected;

const int yAxisPin = 33;

void setup() {
  Serial.begin(115200);
  SerialBT.begin(deviceName, true);
  pinMode(yAxisPin, INPUT);
  Serial.println("Bluetooth device started");
  connected = SerialBT.connect(receiverName);
  if(connected) {
    Serial.println("Connected Succesfully!");
  } else {
    while(!SerialBT.connected(10000)) {
      Serial.println("Failed to connect."); 
    }
  }
  if (SerialBT.disconnect()) {
    Serial.println("Disconnected Succesfully!");
  }

  SerialBT.connect();
}

void loop() {
  // Read joystick data
  int yAxisValue = analogRead(yAxisPin); // Map 0-4095  

  // Send data over Bluetooth
  sendData(yAxisValue);

  delay(100); // Adjust delay as needed
}

void sendData(int yAxisValue) {
  // Construct the data packet to send over Bluetooth
  String dataPacket = String(yAxisValue) + "\n";

  // Send data packet over Bluetooth
  SerialBT.print(dataPacket);

  Serial.print("y-axis value sent: ");
  Serial.println(yAxisValue);
}


