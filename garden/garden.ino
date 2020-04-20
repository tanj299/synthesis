/*
 * Author:  Daniel Mallia
 * Date:    4/20/2020
 * Purpose: This is the main Arduino sketch for maintaining
 *          two plants in a synthesis garden.
 * 
 */

#include "Adafruit_Si7021.h"

// Define sensors
// Single Temperature and Humidity Sensor
Adafruit_Si7021 th_sensor = Adafruit_Si7021();
// Single Water Level Sensor
const int water_lvl_sensor = 6;
// Sensor arrays 
// Light (Analog) / Soil Moisture (Analog) 
// Light (Digital) / Soil Temperature (Digital)
int plant1_pins[] = {A0, A2, 2, 4};
int plant2_pins[] = {A1, A3, 3, 5};

// Function to retrieve the moisture level as an integer
// percentage 0 - 100 %.
// Note: max and min are stored constants reflecting the 
// observed values with the sensor.
int get_moisture_level(int pin) {
  float max = 1.71;
  float min = 0.90;
  int sensorVal = analogRead(pin);
  float voltage = (sensorVal/1024.0) * 3.0;
  return round(100*( 1 - ((voltage - min) / (max - min))));
}

void plant_report(int pins[]) {
  int temp = round((1.8 * th_sensor.readTemperature()) + 32);
  delay(50);
  int humid = round(th_sensor.readHumidity());
  delay(50);
  int moisture = get_moisture_level(pins[1]);
  Serial.print(temp); Serial.print(","); Serial.print(humid);
  Serial.println(",");
}

void setup() {
  Serial.begin(9600);

  // Check for Si7021 sensor
  while (!th_sensor.begin()) {
    Serial.println("Did not find Si7021 sensor!");
    delay(5000);
    if(th_sensor.begin()) {
      break;
    }
  }
}

void loop() {
  // While there are commands to process
  while(Serial.available()) {
    char rec = Serial.read(); // Read command
    if(rec == '1') { // Report on plant 1
      plant_report(plant1_pins);
    } else if(rec == '2') { // Report on plant 2
      plant_report(plant2_pins);
    }
  }

  delay(5000); // Rest for 5 seconds
}
