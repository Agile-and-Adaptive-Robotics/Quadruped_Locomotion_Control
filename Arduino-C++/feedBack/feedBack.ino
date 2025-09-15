/*
 *  CD74HC4067 "Loop" example used for the basic MUX structure.
 *  https://www.instructables.com/Arduino-Interfacing-With-CD74HC4067-16-channel-MUX/
 */

#include <CD74HC4067.h> // multiplexer library.

const int num_potentiometer = 12;       // how many potentiometers are there?
const int num_press_sensor = 12;        // and how many pressure sensors?
const int data_length = num_potentiometer + num_press_sensor * 2;
uint8_t sensor_data[data_length];       // storage array for all sensor data.

// --- Logical-to-physical mapping for potentiometers (joint angles) ---
// Order: ['L_hip_joint', 'L_knee_joint', 'L_ankle_joint', 
//         'R_hip_joint', 'R_knee_joint', 'R_ankle_joint', 
//         'L_scapula_joint', 'L_shoulder_joint', 'L_wrist_joint', 
//         'R_scapula_joint', 'R_shoulder_joint', 'R_wrist_joint']

const int L_scapula_joint   = 0;
const int L_shoulder_joint  = 1;
const int L_wrist_joint     = 2;
const int R_scapula_joint   = 3;
const int R_shoulder_joint  = 4;
const int R_wrist_joint     = 5;
const int L_hip_joint       = 6;
const int L_knee_joint      = 7;
const int L_ankle_joint     = 8;
const int R_hip_joint       = 9;
const int R_knee_joint      = 10;
const int R_ankle_joint     = 11;


const int R_hip_joint_ext_muscle      = 2;
const int R_hip_joint_flx_muscle      = 3;
const int R_knee_joint_ext_muscle     = 4;
const int R_knee_joint_flx_muscle     = 5;
const int R_ankle_joint_ext_muscle    = 6;
const int R_ankle_joint_flx_muscle    = 7;

const int L_hip_joint_ext_muscle      = 8;
const int L_hip_joint_flx_muscle      = 9;
const int L_knee_joint_ext_muscle     = 10;
const int L_knee_joint_flx_muscle     = 11;
const int L_ankle_joint_ext_muscle    = 12;
const int L_ankle_joint_flx_muscle    = 13;

const int R_scapula_joint_ext_muscle  = 2;
const int R_scapula_joint_flx_muscle  = 3;
const int R_shoulder_joint_ext_muscle = 4;
const int R_shoulder_joint_flx_muscle = 5;
const int R_wrist_joint_ext_muscle    = 6;
const int R_wrist_joint_flx_muscle    = 7;

const int L_scapula_joint_ext_muscle  = 8;
const int L_scapula_joint_flx_muscle  = 9;
const int L_shoulder_joint_ext_muscle = 10;
const int L_shoulder_joint_flx_muscle = 11;
const int L_wrist_joint_ext_muscle    = 12;
const int L_wrist_joint_flx_muscle    = 13;


// --- Arrays for polling order (logical order) ---

const uint8_t mux_channels[num_potentiometer] = {
  L_scapula_joint, L_shoulder_joint, L_wrist_joint, 
  R_scapula_joint, R_shoulder_joint, R_wrist_joint,
  L_hip_joint, L_knee_joint, L_ankle_joint, 
  R_hip_joint, R_knee_joint, R_ankle_joint
};

const uint8_t press_mux_channel_fore[num_press_sensor] = {  
  L_scapula_joint_ext_muscle, L_scapula_joint_flx_muscle, 
  L_shoulder_joint_ext_muscle, L_shoulder_joint_flx_muscle, 
  L_wrist_joint_ext_muscle, L_wrist_joint_flx_muscle,

  R_scapula_joint_ext_muscle, R_scapula_joint_flx_muscle, 
  R_shoulder_joint_ext_muscle, R_shoulder_joint_flx_muscle, 
  R_wrist_joint_ext_muscle, R_wrist_joint_flx_muscle
};

const uint8_t press_mux_channel_hind[num_press_sensor] = {
  L_hip_joint_ext_muscle, L_hip_joint_flx_muscle, 
  L_knee_joint_ext_muscle, L_knee_joint_flx_muscle, 
  L_ankle_joint_ext_muscle, L_ankle_joint_flx_muscle,

  R_hip_joint_ext_muscle, R_hip_joint_flx_muscle, 
  R_knee_joint_ext_muscle, R_knee_joint_flx_muscle, 
  R_ankle_joint_ext_muscle, R_ankle_joint_flx_muscle
};


               // s0  s1  s2  s3
CD74HC4067  mux(18, 17, 16, 15);  // create a new CD74HC4067 object with its four control pins
const int pot_pin = A0;          // will be A17 on Muscle Mutt

CD74HC4067 pressure_mux_fore(23, 22, 21, 20);  // create a new CD74HC4067 object 
const int pressure_pin_fore = A5;              // read pin for the CD74HC4067

CD74HC4067 pressure_mux_hind(31, 30, 29, 28);  // create a new CD74HC4067 object 
const int pressure_pin_hind = A13;             // read pin for the CD74HC4067



int raw_data; // raw data from serial.

void setup() {
    Serial.begin(115200); // Initialize serial
    Serial.setTimeout(1); // Serial timeout

    pinMode(pot_pin, INPUT); // set the initial mode of the common pin.
    pinMode(pressure_pin_fore, INPUT); // set the initial mode of the common pin.
}

// Select through all multiplexor pins and update sensor data array
void read_all_joints() {
  // Poll potentiometers in logical order
  for (int i = 0; i < num_potentiometer; i++) {
    mux.channel(mux_channels[i]);
    analogRead(pot_pin); // Dummy read! Allows the Teensy ADC pin capacitor to charge
    sensor_data[i] = analogRead(pot_pin)/4; // read potentiometer data, byte-sized
    // Serial.print(sensor_data[i]);
    // Serial.print("  ");
  }
  // Poll pressure sensors in logical order
  for (int i = 0; i < num_press_sensor; i++) {
    pressure_mux_fore.channel(press_mux_channel_fore[i]);
    analogRead(pressure_pin_fore); // Dummy read! Allows the Teensy ADC pin capacitor to charge
    sensor_data[num_press_sensor + i] = analogRead(pressure_pin_fore)/4; // read byte-sized data
    Serial.print(sensor_data[num_press_sensor + i]);
    Serial.print("  ");
  }
  // Poll pressure sensors in logical order
  for (int i = 0; i < num_press_sensor; i++) {
    pressure_mux_hind.channel(press_mux_channel_hind[i]);
    analogRead(pressure_pin_hind); // Dummy read! Allows the Teensy ADC pin capacitor to charge
    sensor_data[num_press_sensor + i] = analogRead(pressure_pin_hind)/4; // read byte-sized data
    Serial.print(sensor_data[num_press_sensor + i]);
    Serial.print("  ");
  }
  Serial.println();
}

// When requested over serial, read and send sensor data
void loop() {
  // if (Serial.available()) {
    // raw_data = Serial.read(); 
    // if (raw_data == 255) {
      read_all_joints();
      // Serial.write(sensor_data, data_length);
    // }
  // }
  delay(200);
}