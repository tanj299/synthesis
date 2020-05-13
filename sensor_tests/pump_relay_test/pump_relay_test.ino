/*
 * Author: Daniel Mallia
 * Date: 4/9/2020
 * Purpose: This script is used for testing the control of 
 *          the 12V water pumps by the Arduino via a relay
 *          board. The script is very simple, as there is 
 *          little difficulty past the setup.
 *          
 *          In terms of configuration, the pump is hooked 
 *          up to the Normally Open (NO) jack on the relay.
 *          This is so that by default, when the Arduino is 
 *          off (or should power fail), the pump is part of
 *          a "normally open" circuit and will not turn on.
 *          Once the Arduino is on and the pinMode has been 
 *          set to OUTPUT, a signal of HIGH (5 volts) must 
 *          be "written" to the pin so as to keep the pump
 *          OFF. (This has to do with the voltage 
 *          referencing, as we essentially want the relay to
 *          NOT see a difference of 5 volts, until we want 
 *          to close the normally open circuit.) Thus, to
 *          turn ON the water pump, we write a signal of LOW
 *          (0 volts) which will cause the relay to switch 
 *          power to the pump. 
 *          
 */

// Pin connected to input pin #1 on the relay
const int pin = 10;

void setup() {
  pinMode(pin, OUTPUT);
}

void loop() {
  // Run the pump for 2000 milliseconds (2 seconds) and then
  // switch it off for 10 seconds.
  digitalWrite(pin, LOW); // LOW = PUMP ON
  delay(2000);
  digitalWrite(pin, HIGH); // HIGH = PUMP OFF
  delay(10000);
}
