const int analogInputPin1 = A1;  // Analog input pin
const int analogInputPin2 = A2;  // Analog input pin
const int analogInputPin3 = A3;  // Analog input pin
const int analogInputPin4 = A4;  // Analog input pin
const int outputPin1 = 7;        // Digital output pin
const int outputPin2 = 6;        // Digital output pin
const int outputPin3 = 5;        // Digital output pin
const int outputPin4 = 4;        // Digital output pin

void setup() {
  pinMode(analogInputPin1, INPUT);
  pinMode(outputPin1, OUTPUT);
  digitalWrite(outputPin1, LOW); // Set initial state to LOW
  pinMode(analogInputPin2, INPUT);
  pinMode(outputPin2, OUTPUT);
  digitalWrite(outputPin2, LOW); // Set initial state to LOW
  pinMode(analogInputPin3, INPUT);
  pinMode(outputPin3, OUTPUT);
  digitalWrite(outputPin3, LOW); // Set initial state to LOW
  pinMode(analogInputPin4, INPUT);
  pinMode(outputPin4, OUTPUT);
  digitalWrite(outputPin4, LOW); // Set initial state to LOW
  Serial.begin(9600);           // Initialize serial communication for debugging
}

void loop() {
  int sensorValue1 = analogRead(analogInputPin1);  // Read analog input
  int sensorValue2 = analogRead(analogInputPin2);
  int sensorValue3 = analogRead(analogInputPin3);
  int sensorValue4 = analogRead(analogInputPin4);
  float voltage1 = sensorValue1 * (5.0 / 1023.0);  // Convert analog reading to voltage (assuming 5V system)
  float voltage2 = sensorValue2 * (5.0 / 1023.0); 
  float voltage3 = sensorValue3 * (5.0 / 1023.0); 
  float voltage4 = sensorValue4 * (5.0 / 1023.0); 
  
  Serial.print("Measured Voltage #1: ");
  Serial.println(voltage1);
  Serial.print("Measured Voltage #2: ");
  Serial.println(voltage2);
  Serial.print("Measured Voltage #3: ");
  Serial.println(voltage3);
  Serial.print("Measured Voltage #4: ");
  Serial.println(voltage4);
  
  // Check if voltage is over 0.3V
  if (voltage1 >= 0.3 ) {
    digitalWrite(outputPin1, HIGH); 
    Serial.println("Voltage 1 is higher then 0.3");
  } if (voltage1 < 0.3){
    digitalWrite(outputPin1, LOW);  // Output 0V signal
    Serial.println("Voltage 1 is lower then 0.3");
  }if (voltage2 >= 0.3 ) {
    digitalWrite(outputPin2, HIGH); 
    Serial.println("Voltage 2 is higher then 0.3V");
  } if (voltage2 < 0.3) {
    digitalWrite(outputPin2, LOW);  // Output 0V signal
    Serial.println("Voltage 2 is lower then 0.3");
  }if (voltage3 >= 0.3 ) {
    digitalWrite(outputPin3, HIGH); 
    Serial.println("Voltage 3 is higher then 0.3V");
  } if (voltage3 < 0.3){
    digitalWrite(outputPin3, LOW);  // Output 0V signal
    Serial.println("Voltage 3 is lower then 0.3");
  }if (voltage4 >= 0.3 ) {
    digitalWrite(outputPin4, HIGH); 
    Serial.println("Voltage 4 is higher then 0.3");
  } if (voltage4 < 0.3){
    digitalWrite(outputPin4, LOW);  // Output 0V signal
    Serial.println("Voltage 4 is lower then 0.3");
  }



  delay(100); // Delay for stability
}
