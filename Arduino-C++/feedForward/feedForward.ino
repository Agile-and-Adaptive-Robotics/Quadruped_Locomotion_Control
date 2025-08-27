#include <Arduino.h>
#include <Muscle.h>
/*
 * Py_Ard_Pipeline_Mult_Muscles
 *  
 *  This code implements a data pipeline in conjunction with RTSpikingCPG.py, 
 *   actuating two braided pneumatic actuator (BPA) muscles on robots in the
 *   Agile & Adaptive Robotics Laboratory (AARL) at Portland State University.
 *
 * Dependencies:
 *  - Muscle.h library, a library for implementing pulse-based control of AARL
 *      BPA muscles.
 * 
 *  - Arduino.h library, a library for encoding Teensy microcontrollers.
 *
 * Date: 8/9/2024
 * By: Stu McNeal
 */

const uint8_t packet_size = 4;

uint8_t buffer[packet_size];
uint8_t buffer_index = 0;


// Define the control pins for the valves that control the BPA muscles. Specific to the AARL QTB.

int pin_valve_hipREX      = 10;
int pin_valve_hipRFL      = 24;
int pin_valve_kneeREX     = 27;
int pin_valve_kneeRFL     = 28;
int pin_valve_ankleREX    = 29;
int pin_valve_ankleRFL    = 30;

int pin_valve_hipLEX      = 4;
int pin_valve_hipLFL      = 5;
int pin_valve_kneeLEX     = 36;
int pin_valve_kneeLFL     = 35;
int pin_valve_ankleLEX    = 33;
int pin_valve_ankleLFL    = 34;

int pin_valve_scapulaREX  = 25;
int pin_valve_scapulaRFL  = 26;
int pin_valve_shoulderREX = 8;
int pin_valve_shoulderRFL = 9;
int pin_valve_wristREX    = 1;
int pin_valve_wristRFL    = 0;

int pin_valve_scapulaLEX  = 31;
int pin_valve_scapulaLFL  = 32;
int pin_valve_shoulderLEX = 2;
int pin_valve_shoulderLFL = 3;
int pin_valve_wristLEX    = 7;
int pin_valve_wristLFL    = 6;


// // Define the force sensor pins for each muscle object. Specific to the AARL QTB.
// int pin_force_sensor_hipREX = 17;
// int pin_force_sensor_hipRFL = 18;

// uint32_t force_hipREX;
// uint32_t force_hipRFL;

// MJL: Define variable to count minimum interval by which to send x (uint32_t is the format for millis();)
uint32_t t_s;
uint32_t t_n;

// Create the Muscle objects. The format for creating a Muscle class object is:
// Muscle <name>(String Name, int pin_valve, int pin_force_sensor) 
// I AM NOT USING FORCE SENSORS!!! MIGHT NEED TO GO BACK AND EDIT THE CLASS 
Muscle hipREX("hipREX", pin_valve_hipREX, 0);
Muscle hipRFL("hipRFL", pin_valve_hipRFL, 0);
Muscle hipLEX("hipLEX", pin_valve_hipLEX, 0); 
Muscle hipLFL("hipLFL", pin_valve_hipLFL, 0);
Muscle kneeREX("kneeREX", pin_valve_kneeREX, 0);
Muscle kneeRFL("kneeRFL", pin_valve_kneeRFL, 0);
Muscle kneeLEX("kneeLEX", pin_valve_kneeLEX, 0); 
Muscle kneeLFL("kneeLFL", pin_valve_kneeLFL, 0);
Muscle ankleREX("ankleREX", pin_valve_ankleREX, 0);
Muscle ankleRFL("ankleRFL", pin_valve_ankleRFL, 0);
Muscle ankleLEX("ankleLEX", pin_valve_ankleLEX, 0); 
Muscle ankleLFL("ankleLFL", pin_valve_ankleLFL, 0);
Muscle scapulaREX("scapulaREX", pin_valve_scapulaREX, 0); 
Muscle scapulaRFL("scapulaRFL", pin_valve_scapulaRFL, 0);
Muscle scapulaLEX("scapulaLEX", pin_valve_scapulaLEX, 0);
Muscle scapulaLFL("scapulaLFL", pin_valve_scapulaLFL, 0);
Muscle shoulderREX("shoulderREX", pin_valve_shoulderREX, 0);
Muscle shoulderRFL("shoulderRFL", pin_valve_shoulderRFL, 0);
Muscle shoulderLEX("shoulderLEX", pin_valve_shoulderLEX, 0);
Muscle shoulderLFL("shoulderLFL", pin_valve_shoulderLFL, 0);
Muscle wristREX("wristREX", pin_valve_wristREX, 0);
Muscle wristRFL("wristRFL", pin_valve_wristRFL, 0);
Muscle wristLEX("wristLEX", pin_valve_wristLEX, 0);
Muscle wristLFL("wristLFL", pin_valve_wristLFL, 0);

int x;

void setup() {
  Serial.begin(115200);

  //initialize Muscle object pins and set initial values (see Muscle.cpp) (Might be redundant...?)
  hipREX.begin();
  hipRFL.begin();
  hipLEX.begin();
  hipLFL.begin();
  kneeREX.begin();
  kneeRFL.begin();
  kneeLEX.begin();
  kneeLFL.begin();
  ankleREX.begin();
  ankleRFL.begin();
  ankleLEX.begin();
  ankleLFL.begin();
  scapulaREX.begin();
  scapulaRFL.begin();
  scapulaLEX.begin();
  scapulaLFL.begin();
  shoulderREX.begin();
  shoulderRFL.begin();
  shoulderLEX.begin();
  shoulderLFL.begin();
  wristREX.begin();
  wristRFL.begin();
  wristLEX.begin();
  wristLFL.begin();

  //Set maximum pulse frequency for the hipREX muscle
  hipREX.SetPulseFrequency(100);
  hipRFL.SetPulseFrequency(100);
  hipLEX.SetPulseFrequency(100);
  hipLFL.SetPulseFrequency(100);
  kneeREX.SetPulseFrequency(100);
  kneeRFL.SetPulseFrequency(100);
  kneeLEX.SetPulseFrequency(100);
  kneeLFL.SetPulseFrequency(100);
  ankleREX.SetPulseFrequency(100);
  ankleRFL.SetPulseFrequency(100);
  ankleLEX.SetPulseFrequency(100);
  ankleLFL.SetPulseFrequency(100);
  scapulaREX.SetPulseFrequency(100);
  scapulaRFL.SetPulseFrequency(100);
  scapulaLEX.SetPulseFrequency(100);
  scapulaLFL.SetPulseFrequency(100);
  shoulderREX.SetPulseFrequency(100);
  shoulderRFL.SetPulseFrequency(100);
  shoulderLEX.SetPulseFrequency(100);
  shoulderLFL.SetPulseFrequency(100);
  wristREX.SetPulseFrequency(100);
  wristRFL.SetPulseFrequency(100);
  wristLEX.SetPulseFrequency(100);
  wristLFL.SetPulseFrequency(100);
  
}

void loop() {

  if (Serial.available()) {
    uint8_t raw_data = Serial.read();

    if (buffer_index == 0 && raw_data == 255) {
        buffer[buffer_index] = raw_data;
        buffer_index++;
    } 

    else if (buffer_index != 0) {
        buffer[buffer_index] = raw_data;
        buffer_index++;
    }

    if (buffer_index == packet_size) {
      buffer_index = 0;

      if ((buffer[1] >> 7) & 0x01) hipREX.ShouldPulseStart();
      if ((buffer[1] >> 6) & 0x01) hipRFL.ShouldPulseStart();
      if ((buffer[1] >> 5) & 0x01) kneeREX.ShouldPulseStart();
      if ((buffer[1] >> 4) & 0x01) kneeRFL.ShouldPulseStart();
      if ((buffer[1] >> 3) & 0x01) ankleREX.ShouldPulseStart();
      if ((buffer[1] >> 2) & 0x01) ankleRFL.ShouldPulseStart();
      if ((buffer[1] >> 1) & 0x01) hipLEX.ShouldPulseStart();
      if ((buffer[1] >> 0) & 0x01) hipLFL.ShouldPulseStart();
      if ((buffer[2] >> 7) & 0x01) kneeLEX.ShouldPulseStart();
      if ((buffer[2] >> 6) & 0x01) kneeLFL.ShouldPulseStart();
      if ((buffer[2] >> 5) & 0x01) ankleLEX.ShouldPulseStart();
      if ((buffer[2] >> 4) & 0x01) ankleLFL.ShouldPulseStart();
      if ((buffer[2] >> 3) & 0x01) scapulaREX.ShouldPulseStart();
      if ((buffer[2] >> 2) & 0x01) scapulaRFL.ShouldPulseStart();
      if ((buffer[2] >> 1) & 0x01) shoulderREX.ShouldPulseStart();
      if ((buffer[2] >> 0) & 0x01) shoulderRFL.ShouldPulseStart();
      if ((buffer[3] >> 7) & 0x01) wristREX.ShouldPulseStart();
      if ((buffer[3] >> 6) & 0x01) wristRFL.ShouldPulseStart();
      if ((buffer[3] >> 5) & 0x01) scapulaLEX.ShouldPulseStart();
      if ((buffer[3] >> 4) & 0x01) scapulaLFL.ShouldPulseStart();
      if ((buffer[3] >> 3) & 0x01) shoulderLEX.ShouldPulseStart();
      if ((buffer[3] >> 2) & 0x01) shoulderLFL.ShouldPulseStart();
      if ((buffer[3] >> 1) & 0x01) wristLEX.ShouldPulseStart();
      if ((buffer[3] >> 0) & 0x01) wristLFL.ShouldPulseStart();

      Serial.write(buffer, packet_size);
    }
  }

  // End pulses as needed
  hipREX.ShouldPulseEnd();
  hipRFL.ShouldPulseEnd();
  hipLEX.ShouldPulseEnd();
  hipLFL.ShouldPulseEnd();
  kneeREX.ShouldPulseEnd();
  kneeRFL.ShouldPulseEnd();
  kneeLEX.ShouldPulseEnd();
  kneeLFL.ShouldPulseEnd();
  ankleREX.ShouldPulseEnd();
  ankleRFL.ShouldPulseEnd();
  ankleLEX.ShouldPulseEnd();
  ankleLFL.ShouldPulseEnd();
  scapulaREX.ShouldPulseEnd();
  scapulaRFL.ShouldPulseEnd();
  scapulaLEX.ShouldPulseEnd();
  scapulaLFL.ShouldPulseEnd();
  shoulderREX.ShouldPulseEnd();
  shoulderRFL.ShouldPulseEnd();
  shoulderLEX.ShouldPulseEnd();
  shoulderLFL.ShouldPulseEnd();
  wristREX.ShouldPulseEnd();
  wristRFL.ShouldPulseEnd();
  wristLEX.ShouldPulseEnd();
  wristLFL.ShouldPulseEnd();

}