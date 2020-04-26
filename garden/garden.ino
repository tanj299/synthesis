/*
 * Author:  Daniel Mallia
 * Date:    4/20/2020
 * Purpose: This is the main Arduino sketch for maintaining
 *          two plants in a synthesis garden.
 * 
 */

#include "Adafruit_Si7021.h"
#include <OneWire.h>
#include <DallasTemperature.h>

// Define sensors
// Single Temperature and Humidity Sensor
Adafruit_Si7021 th_sensor = Adafruit_Si7021();

// Single Water Level Sensor
const int water_lvl_sensor = 6;

// Set up OneWire objects
const int plant1_soil_temp_pin = 4;
const int plant2_soil_temp_pin = 5;
OneWire oneWire1(plant1_soil_temp_pin);
DallasTemperature plant1_soil_temp(&oneWire1);
DeviceAddress plant1_arr;
OneWire oneWire2(plant2_soil_temp_pin);
DallasTemperature plant2_soil_temp(&oneWire2);
DeviceAddress plant2_arr;

// Sensor arrays 
// Light (Analog) / Soil Moisture (Analog) 
int plant1_pins[] = {A0, A2};
int plant2_pins[] = {A1, A3};

// Define sensor constants
const float max_light = 4.80;
const float min_light = 0.01;
const float max_moisture = 1.71;
const float min_moisture = 0.90;

// Define relay control pins
const int light_ctrl = 8;
const int pump_ctrl = 10;

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
void plant_report(int pins[], DallasTemperature& sensor, DeviceAddress arr) {
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

  // Fetch soil temperature
  sensor.requestTemperaturesByAddress(arr);
  int soil_temp = round(sensor.getTempF(arr));

  // Transmit over Serial as a comma-delimited sequence
  Serial.print(temp); Serial.print(","); Serial.print(humid);
  Serial.print(","); Serial.print(light); Serial.print(",");
  Serial.print(moisture); Serial.print(","); Serial.println(soil_temp);
}

int setup_soil_temp(DallasTemperature& sensor, DeviceAddress arr) {
  sensor.begin();
  if(!sensor.getAddress(arr, 0)) {
    return 1;
  } else {
    sensor.setResolution(arr, 10);
    return 0;
  }
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

  // Set outputs and keep light and pump off unless requested
  pinMode(light_ctrl, OUTPUT);
  pinMode(pump_ctrl, OUTPUT);
  digitalWrite(light_ctrl, HIGH);
  digitalWrite(pump_ctrl, HIGH);
}

void loop() {
  // While there are commands to process
  while(Serial.available()) {
    char rec = Serial.read(); // Read command
    switch(rec) {
      case '1': // Report on plant 1
        plant_report(plant1_pins, plant1_soil_temp, plant1_arr); 
        break;
      case '2': // Report on plant 2
        plant_report(plant2_pins, plant2_soil_temp, plant2_arr); 
        break;
      case '3': // Check water level - return 0 if OK, else 1
        Serial.println(digitalRead(water_lvl_sensor));
        delay(100);
        break;
      case '4': // Set up plant 1 soil temperature sensor
        Serial.println(setup_soil_temp(plant1_soil_temp, plant1_arr));
        break;
      case '5': // Set up plant 2 soil temperature sensor
        Serial.println(setup_soil_temp(plant2_soil_temp, plant2_arr));
        break;
      case '6': // Turn on light
        digitalWrite(light_ctrl, LOW);
        break;
      case '7': // Turn off light
        digitalWrite(light_ctrl, HIGH);
        break;
      case '8': // Turn on pump
        digitalWrite(pump_ctrl, LOW);
        delay(100);
        break;
      case '9': // Turn off pump
        digitalWrite(pump_ctrl, HIGH);
        delay(100);
        break;
    }
  }

  delay(5000); // Rest for 5 seconds
}
