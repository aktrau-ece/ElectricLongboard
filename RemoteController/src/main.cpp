// This was written for an ESP32 using the Arduino framework on Platform IO.
// The ESP32 acts as a bluetooth-slave and streams sensor (a joystick)
// data to the bluetooth-master it's paired with.

#include <Arduino.h>
#include <BluetoothSerial.h>
// #include <WiFi.h>

#define JOYSTICK_NOINPUT_VALUE 1947
#define JOYSTICK_FULLTHROTTLE_VALUE 0
#define JOYSTICK_DEADZONE 5 // as a percentage

BluetoothSerial SerialBT;

const int yAxisPin = 33;
int yAxisValue;

int getThrottlePercentage(int sensor_output);

void setup() {

	Serial.begin(115200);
	Serial.println("Running setup..");

	// WiFi.mode(WIFI_MODE_STA);
	// Serial.println("MAC Address: " + WiFi.macAddress()); // 48:E7:29:A1:85:84

	SerialBT.begin("ESP32-Joystick");

	pinMode(yAxisPin, INPUT);

	Serial.println("Finished setup");
}

void loop() {

	yAxisValue = analogRead(yAxisPin);
	Serial.print("Raw sensor data: ");
	Serial.println(yAxisValue);

	int throttle = getThrottlePercentage(yAxisValue);
	Serial.print("Calculated throttle: ");
	Serial.println(throttle);

	String dataPacket = String(throttle) + "\n";
	if (SerialBT.available()) {
		SerialBT.print(dataPacket);
	}

	delay(2000);
	Serial.println("End of loop");
}

int getThrottlePercentage(int sensor_output) {

	int range = JOYSTICK_FULLTHROTTLE_VALUE - JOYSTICK_NOINPUT_VALUE;
	float throttle = float(sensor_output - JOYSTICK_NOINPUT_VALUE) / float(range) * 100;

	if ( abs(throttle) < JOYSTICK_DEADZONE ) {
		throttle = 0;
	}

	return int(throttle);
}