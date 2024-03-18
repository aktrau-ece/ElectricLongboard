#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

// Right motor
int enableRightMotor = 22;
int rightMotorPin1 = 16;
int rightMotorPin2 = 17;
// Left motor
int enableLeftMotor = 23;
int leftMotorPin1 = 18;
int leftMotorPin2 = 19;

#define MAX_MOTOR_SPEED 200
#define MED_MOTOR_SPEED 150
#define LOW_MOTOR_SPEED 100

void setUpPinModes() {
  pinMode(enableRightMotor, OUTPUT);
  pinMode(rightMotorPin1, OUTPUT);
  pinMode(rightMotorPin2, OUTPUT);

  pinMode(enableLeftMotor, OUTPUT);
  pinMode(leftMotorPin1, OUTPUT);
  pinMode(leftMotorPin2, OUTPUT);

  // Set the initial state of the motors (stopped)
  digitalWrite(rightMotorPin1, LOW);
  digitalWrite(rightMotorPin2, LOW);
  digitalWrite(leftMotorPin1, LOW);
  digitalWrite(leftMotorPin2, LOW);
}

void setup() {
  setUpPinModes();
  Serial.begin(115200);

  // Initialize Bluetooth serial communication
  SerialBT.begin("ESP32-Motors"); 

  Serial.println("Bluetooth device started");
}

void loop() {

  // Check if data is available to read from Bluetooth
  if (SerialBT.available()) {
    // Read the data received over Bluetooth
    String dataPacket = SerialBT.readStringUntil('\n');

    // Convert the received string to an integer
    int yAxisValue = dataPacket.toInt();

    // Process received data and control the car
    controlCar(yAxisValue);

    Serial.print("Received y-axis value: ");
    Serial.println(yAxisValue);
  }
}

void rotateMotor(int rightMotorSpeed, int leftMotorSpeed) {
  // Control the right motor
  if (rightMotorSpeed > 0) {
    digitalWrite(rightMotorPin1, HIGH);
    digitalWrite(rightMotorPin2, LOW);
  } else {
    digitalWrite(rightMotorPin1, LOW);
    digitalWrite(rightMotorPin2, LOW);
  }

  // Control the left motor
  if (leftMotorSpeed > 0) {
    digitalWrite(leftMotorPin1, HIGH);
    digitalWrite(leftMotorPin2, LOW);
  } else {
    digitalWrite(leftMotorPin1, LOW);
    digitalWrite(leftMotorPin2, LOW);
  }

  // Set motor speeds using PWM
  analogWrite(enableRightMotor, abs(rightMotorSpeed));
  analogWrite(enableLeftMotor, abs(leftMotorSpeed));
}

void controlCar(int yAxisValue) {
  // Check if the yAxisValue indicates forward movement
  if (yAxisValue <= 4095 && yAxisValue >= 3000) {
    // Move the car forward at MAX speed
    rotateMotor(MAX_MOTOR_SPEED, MAX_MOTOR_SPEED);
  } else if (yAxisValue < 3000 && yAxisValue >= 2000) {
    // Move the car forward at MEDIUM speed
    rotateMotor(MED_MOTOR_SPEED, MED_MOTOR_SPEED);
  } else {
    // Stop the car if not moving forward
    rotateMotor(0, 0);
  }
}


