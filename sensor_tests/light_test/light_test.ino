/*
 * Author:  Daniel Mallia
 * Date:    4/15/2020
 * Purpose: This script is used for testing and calibrating the Gowoops
 *          "Digital Light Intensity Detection Photosensitive Sensor 
 *          Module for Arduino UNO". The board has an analog and digital
 *          output. The former yields a conventional analog signal which
 *          can be interpreted to determine the light intensity, with low 
 *          signal/voltage indicating greater brightness, and high signal/
 *          voltage indicating less intensity. The latter consists of output 
 *          of a 0 for "high" light or a 1 for "low" light. The board also
 *          has a potentiometer which can be used to modify the threshold for
 *          the digital output. Turning the potentiometer left will increase 
 *          the threshold, requiring very direct application of light in the 
 *          direction of the sensor for the an output of "high" light. This  
 *          inversion of low voltage for high brightness, and high 
 *          directionality with the module is due to its usage of a photodiode
 *          rather than a photoresistor. 
 *          
 *          Maximum observed voltage value: 4.80V
 *          Minimum observed voltage value: 0.01V
 *          
 *          ***Requires some finer tuning to get the percentages into desirable
 *          range.****
 */

const int analog_pin = A0;
const int digital_pin = 7;
const float max = 4.80;
const float min = 0.01;

void setup() {
  Serial.begin(9600);
  pinMode(7, INPUT);
}

void loop() {
  int raw = analogRead(analog_pin);
  delay(500);
  int digital = digitalRead(digital_pin);
  float voltage = (raw/1024.0) * 5.0;
  float light = 100 * (1 - ((voltage - min) / (max - min)));

  Serial.print("Sensor Value: ");
  Serial.print(raw);
  Serial.print(" Voltage: ");
  Serial.print(voltage);
  Serial.print(" Light level %: ");
  Serial.print(light);
  Serial.print(" Digital: ");
  Serial.print(digital);

  if(digital == 0){
    Serial.println(" Light: ON");
  } else {
    Serial.println(" Light: OFF");
  }

}
