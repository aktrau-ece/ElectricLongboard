const int analogInputPin = A1;  // Analog input pin
const int outputPin = 7;        // Digital output pin

void setup() {
  pinMode(analogInputPin, INPUT);
  pinMode(outputPin, OUTPUT);
  digitalWrite(outputPin, LOW); // Set initial state to LOW
  Serial.begin(9600);           // Initialize serial communication for debugging
}

void loop() {
  int sensorValue = analogRead(analogInputPin);  // Read analog input
  float voltage = sensorValue * (5.0 / 1023.0);  // Convert analog reading to voltage (assuming 5V system)

  Serial.print("Measured Voltage: ");
  Serial.println(voltage);

  // Check if voltage is over 0.3V
  if (voltage >= 0.3) {
    digitalWrite(outputPin, HIGH); 
    Serial.println("Voltage is higher then 0.5V");
  } else {
    digitalWrite(outputPin, LOW);  // Output 0V signal
    Serial.println("Voltage is lower then 0.5");
  }

  delay(100); // Delay for stability
}

