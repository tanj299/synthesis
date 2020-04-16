/*
 * Author:  Daniel Mallia
 * Date:    4/16/2020
 * Purpose: This script is used for testing the EPS Technology Liquid 
 *          Level Sensors. Per the sensor datasheet, the output voltage
 *          of the sensor is generally around 0.30V in water and around 
 *          4.83V in air. Thus while the sensor can be used with an 
 *          analog pin for more precise measurements, the below test 
 *          sketch demonstrated that it can also be used with a digital
 *          pin, recognizing the ~5V HIGH signal (1) as signifying the
 *          sensor is in air, and the ~0V LOW signal (0) as signifying
 *          the sensor is in water. 
 *          
 *          Note: The "recommended application circuit" suggests using 
 *          two capacitors to help filter the power signal noise. While 
 *          good practice, success with this sketch demonstrates that 
 *          they are not absolutely necessary.
 * 
 */

const int pin = 7;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int raw = digitalRead(pin);
  delay(500);
  if(raw == 0){
    Serial.println("Water Level: OK");
  } else {
    Serial.println("Add Water!");
  }

}
