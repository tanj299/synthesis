/*
 * Author:  Daniel Mallia
 * Date:    4/1/2020
 * Purpose: This script is used for testing the Gikfun waterproof
 *          DS18B20 temperature probe sensor. A saint of a 
 *          reviewer on Amazon described the proper wiring and 
 *          referred to the required libaries; a commenter on the
 *          review suggested the hackatronics tutorial. (See the 
 *          below links.)
 *          
 *          Please note that in the course of looking up the 
 *          needed OneWire and DallasTempetature libraries, I 
 *          found that Adafruit had expanded on the original 
 *          libraries, and so I opted to use their versions 
 *          instead. Thus the below uses the following Adafruit 
 *          libraries:
 *          
 *          Adafruit MAX31850 DallasTemp Version 1.0.1
 *          Adafruit MAX31850 OneWire Version 1.0.2
 *          
 *          Both were installed via the Arduino IDE library 
 *          manager. 
 *           
 *          Two sensor notes:
 *          1. This particular DS18B20 sensor does not use 
 *             "parasitic power" as it has a dedicated VCC 
 *             (Voltage Common Collector) line. This   
 *             behavior can be checked via the 
 *             DallasTemperature isParasitePowerMode() 
 *             method.
 *          2. Multiple DS18B20 sensors can be connected to
 *             the same data pin: hence the need to find the
 *             individual device addresses.
 *             
 * Refer to:         
 * https://www.amazon.com/gp/customer-reviews/R3MCZMSAU1CUER/ref=cm_cr_dp_d_rvw_ttl?ie=UTF8&ASIN=B012C597T0
 * https://www.hacktronics.com/Tutorials/arduino-1-wire-tutorial.html
 * https://github.com/adafruit/MAX31850_DallasTemp/blob/master/examples/Single/Single.pde
 * https://github.com/adafruit/MAX31850_DallasTemp/blob/master/DallasTemperature.h
 * 
 */

#include <OneWire.h>
#include <DallasTemperature.h>

const int sensorsPin = 7;
OneWire oneWire(sensorsPin);
DallasTemperature sensors(&oneWire);
DeviceAddress arr;

void setup() {
  Serial.begin(9600);
  sensors.begin();
  Serial.print(sensors.getDeviceCount(), DEC);
  if(sensors.isParasitePowerMode()) Serial.println("ON");
  if(!sensors.getAddress(arr, 0)) Serial.println("Unable to find address for Device 0");  
  Serial.print("Device 0 Address: ");
  printAddress(arr);
  Serial.println();
  sensors.setResolution(arr, 10);

}


void loop() {
  sensors.requestTemperaturesByAddress(arr);
  float temperature = sensors.getTempF(arr);
  Serial.print("Temperature in F: ");
  Serial.println(temperature);

  delay(1000);
  

}

void printAddress(DeviceAddress addr) {
  for(uint8_t i = 0; i < 8; i++) {
    if(addr[i] < 16) Serial.print("0");
    Serial.print(addr[i], HEX);
  }
}
