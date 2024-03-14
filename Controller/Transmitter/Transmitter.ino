#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "ESP32-Access-Point";
const char* password = "password";
const char* serverIP = "192.168.4.1"; // IP address of the server (receiver)

const int yAxisPin = 33;

void setup()
{
  Serial.begin(115200);
  pinMode(yAxisPin, INPUT);

  // Connect to Wi-Fi
  Serial.println();
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}

void loop()
{
  // Read joystick data
  int yAxisValue = analogRead(yAxisPin); // Map 0-4095  

  // Send data to the server
  sendData(yAxisValue);

  //delay(100); // Adjust delay as needed
}

void sendData(int yAxisValue)
{
  WiFiClient client;

  // Construct the URL with the query parameter as plain text
  String url = "http://" + String(serverIP) + "/?yAxisValue=" + String(yAxisValue);

  // Send GET request to the server
  HTTPClient http;
  http.begin(client, url);
  int httpResponseCode = http.GET();

  if (httpResponseCode > 0)
  {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    String response = http.getString();
    Serial.println(response);
    Serial.print("y-axis value: ");
    Serial.println(yAxisValue);
  }
  else
  {
    Serial.print("HTTP Error: ");
    Serial.println(http.errorToString(httpResponseCode).c_str());
  }

  http.end();
}
