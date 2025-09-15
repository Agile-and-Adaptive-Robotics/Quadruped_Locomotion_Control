#include <Arduino.h>

// Pin assignments for valves controlling BPA muscles
int pins[] = {
  10, 24, 27, 28, 29, 30,   // Right leg
  4, 5, 36, 35, 33, 34,     // Left leg
  25, 26, 8, 9, 1, 0,       // Right arm
  31, 32, 2, 3, 7, 6        // Left arm
};

const int numPins = sizeof(pins) / sizeof(pins[0]);
int currentIndex = -1;  // no pin active at start

void setup() {
  Serial.begin(9600);
  Serial.println("Press ENTER to activate next muscle pin...");

  // Initialize all pins as outputs, LOW at start
  for (int i = 0; i < numPins; i++) {
    pinMode(pins[i], OUTPUT);
    digitalWrite(pins[i], LOW);
  }
}

void loop() {
  // Check if user pressed ENTER (carriage return/newline arrives in Serial)
  if (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      // Turn off previous pin
      if (currentIndex >= 0) {
        digitalWrite(pins[currentIndex], LOW);
      }

      // Advance to next pin
      currentIndex++;
      if (currentIndex >= numPins) {
        currentIndex = 0;  // wrap around to first
      }

      // Activate new pin
      digitalWrite(pins[currentIndex], HIGH);
      Serial.print("Activated pin: ");
      Serial.println(pins[currentIndex]);
    }
  }
}
