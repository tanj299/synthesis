/*
 * Author: Daniel Mallia
 * Date: 4/12/2020
 * Purpose: This script is intended to be a simplified 
 *          test sketch demonstrating how to work with
 *          the Adafruit Si7021 sensor, which employs 
 *          the I2C serial protocol. 
 *          
 *          This script depends on the below libraries.
 *          The Si7021 library is a requirement; the 
 *          Adafruit tutorial indicates that the Unified 
 *          Sensor Version library should also be 
 *          installed (and this depends on the Adafruit 
 *          ADXL343) library, but it is unclear if the 
 *          latter two are really necessary. 
 *          
 *          Adafruit Si7021 Version 1.2.4
 *          Adafruit Unified Sensor Version 1.1.2 
 *          Adafruit ADXL343 Version 1.2.0
 *          
 *          Refer to:
 *          https://learn.adafruit.com/adafruit-si7021-temperature-plus-humidity-sensor/arduino-code
 *          https://github.com/adafruit/Adafruit_Si7021
 * 
 */

#include "Adafruit_Si7021.h"

Adafruit_Si7021 sensor = Adafruit_Si7021();

void setup() {
  // Need to investigate appropriate serial transmission
  // rate - I suspect this high of a rate is only 
  // necessary for near continuous transmission.
  Serial.begin(115200);

  // Borrowed from Adafruit Si7021 example code
  if (!sensor.begin()) {
    Serial.println("Did not find Si7021 sensor!");
    while (true)
      ; // Loop forever if cannot establish communication
  }

}

void loop() {
  // Borrowed from Adafruit Si7021 example code and modified
  Serial.print("Humidity:    ");
  // Print relative humidity with 2 decimal place precision
  Serial.print(sensor.readHumidity(), 2);
  // Print temperature converted to Fahrenheit, same precision
  Serial.print("\tTemperature F: ");
  Serial.println(((1.8 * sensor.readTemperature()) + 32), 2);
  delay(1000);

}
