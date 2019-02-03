#include <SimpleDHT.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// for DHT22, 
//      VCC: 5V or 3V
//      GND: GND
//      DATA: 2
int pinDHT22 = 4;
SimpleDHT22 dht22(pinDHT22);

const char* ssid = "***";
const char* password = "***";

void setup_wifi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(1000);
    Serial.println("Connecting...");
  }
}

void setup() {
  pinMode(2, OUTPUT);
  Serial.begin(115200);
  setup_wifi();
}

void loop() {
  digitalWrite(2, LOW);    
  
  float temperature = 0;
  float humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht22.read2(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT22 failed, err="); 
    Serial.println(err);
    delay(2500);
    return;
  }
  
  Serial.print("Sample OK: ");
  Serial.print((float)temperature); Serial.print(" *C, ");
  Serial.print((float)humidity); Serial.println(" RH%");

  if (WiFi.status() != WL_CONNECTED) {
    setup_wifi();
  } 
  else {
    HTTPClient http;
 
    http.begin("http://192.168.0.35:5000/therm/push");
    http.addHeader("Content-Type", "text/plain");

    Serial.println("works");
    int httpCode = http.POST(String(temperature));
    Serial.println(httpCode);
    http.end();
  }

  digitalWrite(2, HIGH); 
  delay(2500);
}