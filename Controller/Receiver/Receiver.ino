#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "ESP32-Access-Point";
const char* password = "password";

WebServer server(80);

struct PacketData
{
  byte yAxisValue;
};


//Right motor
int enableRightMotor=22; 
int rightMotorPin1=16;
int rightMotorPin2=17;
//Left motor
int enableLeftMotor=23;
int leftMotorPin1=18;
int leftMotorPin2=19;

const int PWMFreq = 1000; /* 1 KHz */
const int PWMResolution = 8;
const int rightMotorPWMSpeedChannel = 4;
const int leftMotorPWMSpeedChannel = 5;

#define MAX_MOTOR_SPEED 200
#define MED_MOTOR_SPEED 150
#define LOW_MOTOR_SPEED 100

void setUpPinModes()
{
  pinMode(enableRightMotor,OUTPUT);
  pinMode(rightMotorPin1,OUTPUT);
  pinMode(rightMotorPin2,OUTPUT);
  
  pinMode(enableLeftMotor,OUTPUT);
  pinMode(leftMotorPin1,OUTPUT);
  pinMode(leftMotorPin2,OUTPUT);

  // Set the initial state of the motors (stopped)
  digitalWrite(rightMotorPin1, LOW);
  digitalWrite(rightMotorPin2, LOW);
  digitalWrite(leftMotorPin1, LOW);
  digitalWrite(leftMotorPin2, LOW);

  //Set up PWM for motor speed
  ledcSetup(rightMotorPWMSpeedChannel, PWMFreq, PWMResolution);
  ledcSetup(leftMotorPWMSpeedChannel, PWMFreq, PWMResolution);  
  ledcAttachPin(enableRightMotor, rightMotorPWMSpeedChannel);
  ledcAttachPin(enableLeftMotor, leftMotorPWMSpeedChannel); 
  
  rotateMotor(0, 0);
}

void setup()
{
  setUpPinModes();
  Serial.begin(115200);

  // Set up SoftAP
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("SoftAP IP address: ");
  Serial.println(IP);

  // Start the HTTP server
  server.on("/", HTTP_GET, handleData); // Change to handle GET requests
  server.begin();
  Serial.println("HTTP server started");
}

void loop()
{
  server.handleClient();
}

void handleData()
{
  // Extract the query parameter "yAxisValue" from the URL
  String yAxisValueStr = server.arg("yAxisValue");
  
  // Convert the string to an integer
  int yAxisValue = yAxisValueStr.toInt(); 
  // Process received data
  //int throttle = map(yAxisValue, 0, 254, -255, 255);
  //int motorSpeed = constrain(throttle, -255, 255);

  // Control the car based on the received data
  // Your code to control the car goes here
  controlCar(yAxisValue);
  server.send(200, "text/plain", "Data received");
}

void rotateMotor(int rightMotorSpeed, int leftMotorSpeed)
{
  // Control the right motor
  if (rightMotorSpeed > 0)
  {
    digitalWrite(rightMotorPin1, HIGH);
    digitalWrite(rightMotorPin2, LOW);
  }
  // else if (rightMotorSpeed < 0)
  // {
  //   digitalWrite(rightMotorPin1, LOW);
  //   digitalWrite(rightMotorPin2, HIGH);
  // }
  else
  {
    digitalWrite(rightMotorPin1, LOW);
    digitalWrite(rightMotorPin2, LOW);
  }

  // Control the left motor
  if (leftMotorSpeed > 0)
  {
    digitalWrite(leftMotorPin1, HIGH);
    digitalWrite(leftMotorPin2, LOW);
  }
  // else if (leftMotorSpeed < 0)
  // {
  //   digitalWrite(leftMotorPin1, LOW);
  //   digitalWrite(leftMotorPin2, HIGH);
  // }
  else
  {
    digitalWrite(leftMotorPin1, LOW);
    digitalWrite(leftMotorPin2, LOW);
  }

  ledcWrite(rightMotorPWMSpeedChannel, abs(rightMotorSpeed));
  ledcWrite(leftMotorPWMSpeedChannel, abs(leftMotorSpeed));
}


void controlCar(int yAxisValue) {
  // Check if the yAxisValue indicates forward movement
  if (yAxisValue <= 4095 && yAxisValue >= 3000)
 {
    // Code to move the car forward
    rotateMotor(MAX_MOTOR_SPEED, MAX_MOTOR_SPEED);
    server.send(200, "text/plain","Car moving forward at MAX speed");
  } 
   else if (yAxisValue < 3000 && yAxisValue >= 2000)
 {
//     // Code to move the car forward
     rotateMotor(MED_MOTOR_SPEED, MED_MOTOR_SPEED);
     server.send(200, "text/plain","Car moving forward at MEDIUM speed");
  //}
//   else if (yAxisValue < 2000 && yAxisValue >= 1000)
//  {
//     // Code to move the car forward
//     rotateMotor(LOW_MOTOR_SPEED, LOW_MOTOR_SPEED);
//     server.send(200, "text/plain","Car moving forward at LOW speed");
  }else {
    // Stop the car if not moving forward
    rotateMotor(0, 0);
  }
}
