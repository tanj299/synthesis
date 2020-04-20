/*
 * Author:  Daniel Mallia
 * Date:    4/20/2020
 * Purpose: This is the main Arduino sketch for maintaining
 *          two plants in a synthesis garden.
 * 
 */

#include "Adafruit_Si7021.h"

Adafruit_Si7021 th_sensor = Adafruit_Si7021();
int plant1_pins[] = {A0, A2, 2, 6};
int plant2_pins[] = {A1, A3, 3, 7};

void plant_report(int pins[]) {
  Serial.println(((1.8 * th_sensor.readTemperature()) + 32), 2);
  delay(2000);
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
