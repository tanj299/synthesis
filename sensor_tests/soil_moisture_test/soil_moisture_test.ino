/*
 * Author:  Daniel Mallia
 * Date:    3/30/2020
 * Purpose: This script is used for testing and calibrating the SongHe 
 *          Capacitive Soil Moisture Sensor. 
 *          
 *          Reference: 
 *          Operating voltage: 3.3 ~ 5.5V
 *          Output Voltage: 0 ~ 3.0V
 *          
 *          Capacitance is a measure of the response of a dielectric material to
 *          an applied electrical field - how much charge can be stored on two
 *          parallel conductors due to the presence of a material in between 
 *          them that is not electrically conductive. 
 *          
 *          The voltage output of this sensor is a proxy for the amount of 
 *          capacitance. As capacitance increases (as in the presence of 
 *          water), the voltage drops given their inverse relationship, 
 *          described by:
 *          
 *          Q = CV
 *          
 *          Where V is voltage, C is capacitance, and Q is the potential
 *          difference.
 *          
 *          Maximum observed voltage value: 1.71V 
 *          Minimum observed voltage value: 0.90V
 */

const int sensorPin = A0;
const float max = 1.71;
const float min = 0.90;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // 
  int sensorVal = analogRead(sensorPin);

  float voltage = (sensorVal/1024.0) * 3.0;
  float moisture = 1 - ((voltage - min) / (max - min));
  
  Serial.print("Sensor Value: ");
  Serial.print(sensorVal);
  
  Serial.print(" Voltage: ");
  Serial.print(voltage);

  Serial.print(" Moisture %: ");
  Serial.println(100 * moisture);
  delay(1000);
  
  
}
