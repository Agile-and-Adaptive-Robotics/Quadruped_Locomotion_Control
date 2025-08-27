/*
 *  CD74HC4067 "Loop" example used for the basic MUX structure.
 *  https://www.instructables.com/Arduino-Interfacing-With-CD74HC4067-16-channel-MUX/
 */

#include <CD74HC4067.h> // multiplexer library.

const int num_potentiometer = 12;       // how many potentiometers are there?
const int num_press_sensor = 24;        // and how many pressure sensors?
const int data_length = num_potentiometer + num_press_sensor;
uint8_t sensor_data[data_length];       // storage array for all sensor data.

// --- Logical-to-physical mapping for potentiometers (joint angles) ---
// Order: ['L_hip_joint', 'L_knee_joint', 'L_ankle_joint', 
//         'R_hip_joint', 'R_knee_joint', 'R_ankle_joint', 
//         'L_scapula_joint', 'L_shoulder_joint', 'L_wrist_joint', 
//         'R_scapula_joint', 'R_shoulder_joint', 'R_wrist_joint']

const int L_hip_joint       = A0;
const int L_knee_joint      = A1;
const int L_ankle_joint     = A2;
const int R_hip_joint       = A3;
const int R_knee_joint      = A4;
const int R_ankle_joint     = A5;
const int L_scapula_joint   = A6;
const int L_shoulder_joint  = A7;
const int L_wrist_joint     = A8;
const int R_scapula_joint   = A9;
const int R_shoulder_joint  = A10;
const int R_wrist_joint     = A11;


const int R_hip_joint_ext_muscle      = 2;
const int R_hip_joint_flx_muscle      = 2;
const int R_knee_joint_ext_muscle     = 2;
const int R_knee_joint_flx_muscle     = 2;
const int R_ankle_joint_ext_muscle    = 2;
const int R_ankle_joint_flx_muscle    = 2;

const int L_hip_joint_ext_muscle      = 2;
const int L_hip_joint_flx_muscle      = 2;
const int L_knee_joint_ext_muscle     = 2;
const int L_knee_joint_flx_muscle     = 2;
const int L_ankle_joint_ext_muscle    = 2;
const int L_ankle_joint_flx_muscle    = 2;

const int R_scapula_joint_ext_muscle  = 2;
const int R_scapula_joint_flx_muscle  = 2;
const int R_shoulder_joint_ext_muscle = 2;
const int R_shoulder_joint_flx_muscle = 2;
const int R_wrist_joint_ext_muscle    = 2;
const int R_wrist_joint_flx_muscle    = 2;

const int L_scapula_joint_ext_muscle  = 2;
const int L_scapula_joint_flx_muscle  = 2;
const int L_shoulder_joint_ext_muscle = 2;
const int L_shoulder_joint_flx_muscle = 2;
const int L_wrist_joint_ext_muscle    = 2;
const int L_wrist_joint_flx_muscle    = 2;


// --- Arrays for polling order (logical order) ---

const uint8_t pot_mux_channels[num_potentiometer] = {
  L_hip_joint, L_knee_joint, L_ankle_joint, 
  R_hip_joint, R_knee_joint, R_ankle_joint, 
  L_scapula_joint, L_shoulder_joint, L_wrist_joint, 
  R_scapula_joint, R_shoulder_joint, R_wrist_joint
};

const uint8_t pressure_mux_channels[num_press_sensor] = {
  R_hip_joint_ext_muscle, R_hip_joint_flx_muscle, 
  R_knee_joint_ext_muscle, R_knee_joint_flx_muscle, 
  R_ankle_joint_ext_muscle, R_ankle_joint_flx_muscle,
  
  L_hip_joint_ext_muscle, L_hip_joint_flx_muscle, 
  L_knee_joint_ext_muscle, L_knee_joint_flx_muscle, 
  L_ankle_joint_ext_muscle, L_ankle_joint_flx_muscle,
  
  R_scapula_joint_ext_muscle, R_scapula_joint_flx_muscle, 
  R_shoulder_joint_ext_muscle, R_shoulder_joint_flx_muscle, 
  R_wrist_joint_ext_muscle, R_wrist_joint_flx_muscle,
  
  L_scapula_joint_ext_muscle, L_scapula_joint_flx_muscle, 
  L_shoulder_joint_ext_muscle, L_shoulder_joint_flx_muscle, 
  L_wrist_joint_ext_muscle, L_wrist_joint_flx_muscle
};


               // s0  s1  s2  s3
// CD74HC4067 mux(15, 16, 17, 18);  // create a new CD74HC4067 object with its four control pins
// const int pot_pin = A5;          // will be A17 on Muscle Mutt

// CD74HC4067 pressure_mux(20, 21, 22, 23);  // create a new CD74HC4067 object 
// const int pressure_pin = A17;          // read pin for the CD74HC4067

int raw_data; // raw data from serial.

void setup() {
    Serial.begin(115200); // Initialize serial
    Serial.setTimeout(1); // Serial timeout

    for (int i = 0; i < num_potentiometer; i++) {
      pinMode(pot_mux_channels[i],INPUT);
    }
    for (int i = 0; i < num_press_sensor; i++) {
      pinMode(pressure_mux_channels[i],INPUT);
    }

}

// Select through all multiplexor pins and update sensor data array
void read_all_joints() {
  // Poll potentiometers in logical order
  for (int i = 0; i < num_potentiometer; i++) {
    sensor_data[i] = analogRead(pot_mux_channels[i])/4; // Dummy read! Allows the Teensy ADC pin capacitor to charge

  }
  // Poll pressure sensors in logical order
  for (int i = 0; i < num_press_sensor; i++) {
    sensor_data[num_potentiometer + i] = analogRead(pressure_mux_channels[i])/4; // read byte-sized data
  }
}

// When requested over serial, read and send sensor data
void loop() {
  if (Serial.available()) {
    raw_data = Serial.read(); 
    if (raw_data == 255) {
      read_all_joints();
      Serial.write(sensor_data, data_length);
    }
  }
}