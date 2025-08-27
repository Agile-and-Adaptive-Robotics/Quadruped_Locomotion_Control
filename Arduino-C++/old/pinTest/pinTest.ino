/*
  For Loop Iteration/Users/jacklutz/Desktop/1_Academic/1_MJL_Research/1_Code/1_Modeling_and_Simulation/1_Quadruped/pinTest/pinTest.ino

  Demonstrates the use of a for() loop.
  Lights multiple LEDs in sequence, then in reverse.

  The circuit:
  - LEDs from pins 2 through 7 to ground

  created 2006
  by David A. Mellis
  modified 30 Aug 2011
  by Tom Igoe

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/ForLoopIteration
*/



int timer = 100;  // The higher the number, the slower the timing.

void setup() {
  Serial.begin(9600);
  // use a for loop to initialize each pin as an output:
  for (int thisPin = 0; thisPin <= 36; thisPin++) {
    pinMode(thisPin, OUTPUT);
  }

  Serial.print("Ready to rock'n'roll.");
  while (!Serial.available()) {
      // do nothing
    }
  Serial.read();
}

void loop() {
  // loop from the lowest pin to the highest:
  for (int thisPin = 0; thisPin <= 36; thisPin++) {
    // turn the pin on:
    digitalWrite(thisPin, HIGH);
    Serial.print("Current pin HIGH");
    Serial.println(thisPin);

    while (!Serial.available()) {
      // do nothing
    }
    Serial.read();

    // turn the pin off:
    digitalWrite(thisPin, LOW);
  }

}
