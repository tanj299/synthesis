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

// Define sensor constants
const float max_light = 4.80;
const float min_light = 0.01;
const float max_moisture = 1.71;
const float min_moisture = 0.90;

// Function to retrieve the light level as an integer
// percentage 0 - 100%
// Note: max and min are stored constants reflecting the 
// observed values with the sensor.
int get_light_level(int pin) {
  int raw = analogRead(pin);
  float voltage = (raw/1024.0) * 5.0;
  return round(100 * (1 - ((voltage - min_light) / (max_light - min_light))));
}

// Function to retrieve the moisture level as an integer
// percentage 0 - 100 %.
// Note: max and min are stored constants reflecting the 
// observed values with the sensor.
int get_moisture_level(int pin) {
  int sensorVal = analogRead(pin);
  float voltage = (sensorVal/1024.0) * 3.0;
  return round(100*( 1 - ((voltage - min_moisture) / (max_moisture - min_moisture))));
}

// Function for returning a "plant status report" over Serial.
// @param pins An array containing the pins for the plant of
//             interest, in the sensor ordering described above.
void plant_report(int pins[]) {
  // Fetch temperature and humidity from the single Si7021 sensor
  int temp = round((1.8 * th_sensor.readTemperature()) + 32);
  delay(100);
  int humid = round(th_sensor.readHumidity());
  delay(100);

  // Fetch light reading
  int light = get_light_level(pins[0]);
  delay(100);

  // Fetch soil moisture
  int moisture = get_moisture_level(pins[1]);
  delay(100);

  // Transmit over Serial as a comma-delimited sequence
  Serial.print(temp); Serial.print(","); Serial.print(humid);
  Serial.print(","); Serial.print(light); Serial.print(",");
  Serial.print(moisture); Serial.println(",");
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
    switch(rec) {
      case '1': // Report on plant 1
        plant_report(plant1_pins); 
        break;
      case '2': // Report on plant 2
        plant_report(plant2_pins); 
        break;
      case '3': // Check water level - return 0 if OK, else 1
        Serial.println(digitalRead(water_lvl_sensor));
        delay(100);
        break;
    }
  }

  delay(5000); // Rest for 5 seconds
}
