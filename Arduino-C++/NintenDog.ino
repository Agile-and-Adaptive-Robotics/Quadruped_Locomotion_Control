// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           PIN CONFIGURATION                                ║
// ╚════════════════════════════════════════════════════════════════════════════╝
// FLEXOR PIN ASSIGNMENTS
int flhflex = 32;
int flkflex = 3;
int flaflex = 0;  // Front-Left Hip/Knee/Ankle
int blhflex = 5;
int blkflex = 35;
int blaflex = 34;  // Back-Left Hip/Knee/Ankle
int frhflex = 26;
int frkflex = 9;
int fraflex = 6;  // Front-Right Hip/Knee/Ankle
int brhflex = 24;
int brkflex = 28;
int braflex = 29;  // Back-Right Hip/Knee/Ankle

// EXTENSOR PIN ASSIGNMENTS
int flhext = 31;
int flkext = 2;
int flaext = 1;  // Front-Left Hip/Knee/Ankle
int blhext = 4;
int blkext = 36;
int blaext = 33;  // Back-Left Hip/Knee/Ankle
int frhext = 25;
int frkext = 8;
int fraext = 7;  // Front-Right Hip/Knee/Ankle
int brhext = 10;
int brkext = 27;
int braext = 30;  // Back-Right Hip/Knee/Ankle

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           KEY & PIN MAPPINGS                              ║
// ╚════════════════════════════════════════════════════════════════════════════╝

const int NUM_FLEXORS = 12;
char flexorKeys[NUM_FLEXORS] = { '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=' };
int flexorPins[NUM_FLEXORS] = {
  flhflex, flkflex, flaflex,
  blhflex, blkflex, blaflex,
  frhflex, frkflex, fraflex,
  brhflex, brkflex, braflex
};

const int NUM_EXTENSORS = 12;
char extensorKeys[NUM_EXTENSORS] = { '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+' };
int extensorPins[NUM_EXTENSORS] = {
  flhext, flkext, flaext,
  blhext, blkext, blaext,
  frhext, frkext, fraext,
  brhext, brkext, braext
};

struct LegPins {
  int hext, hflex;
  int kext, kflex;
  int aext, aflex;
};

LegPins fl = { flhext, flhflex, flkext, flkflex, flaext, flaflex };
LegPins bl = { blhext, blhflex, blkext, blkflex, blaext, blaflex };
LegPins fr = { frhext, frhflex, frkext, frkflex, fraext, fraflex };
LegPins br = { brhext, brhflex, brkext, brkflex, braext, braflex };

enum GaitPhase {
  BACKSWING,
  FORESWING,
  STAND
};

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           CORE SETUP & LOOP                               ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Initializes all pins, serial communication, and displays the startup animation
void setup() {
  for (int i = 0; i < 12; i++) {
    pinMode(flexorPins[i], OUTPUT);
    pinMode(extensorPins[i], OUTPUT);
  }
  Serial.begin(9600);
  while (!Serial) {}
  randomSeed(micros());
  clearScreen();
}

// Main program loop that continuously shows the main menu
void loop() {
  showMainMenu();
}

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           MENU SYSTEM                                     ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Displays and handles the main menu interface with options for Toggle, Sequence, and Action modes
void showMainMenu() {
  printDog();
  Serial.println("╔═════════════════════╗");
  Serial.println("║      MAIN MENU      ║");
  Serial.println("╠═════════════════════╣");
  Serial.println("║ 1: TOGGLE MODE      ║");
  Serial.println("║ 2: SEQUENCE MODE    ║");
  Serial.println("║ 3: ACTION MODE      ║");
  Serial.println("║ 4: WALK MODE        ║");
  Serial.println("╚═════════════════════╝");
  while (true) {
    if (Serial.available()) {
      char input = Serial.read();
      if (input == '\n' || input == '\r') continue;
      switch (input) {
        case '1':
          runToggleMode();
          return;
        case '2':
          runSequenceMode();
          return;
        case '3':
          activateActionMenu();
          return;
        case '4':
          activateWalkMenu();
          return;
        default:
          Serial.println("Invalid choice. Try 1, 2, 3");
          break;
      }
    }
  }
}

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           TOGGLE MODE SYSTEM                              ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Runs the toggle mode interface where individual muscles can be toggled on/off with live state display
void runToggleMode() {
  printToggleDisplay();
  while (true) {
    if (Serial.available()) {
      char input = Serial.read();
      if (input == 'x') {
        clearScreen();
        return;
      }
      if (input == 'k') {
        setAllMuscles(LOW, true);
        printToggleDisplay();
        continue;
      }
      if (input == 'K') {
        setAllMuscles(LOW, false);
        printToggleDisplay();
        continue;
      }
      toggleMuscle(input);
      printToggleDisplay();
    }
  }
}

// Toggles the state of a specific muscle based on the input key and displays the new state
void toggleMuscle(char key) {
  for (int i = 0; i < NUM_FLEXORS; i++) {
    if (key == flexorKeys[i]) {
      bool state = digitalRead(flexorPins[i]);
      digitalWrite(flexorPins[i], !state);
      Serial.print("Muscle ");
      Serial.print(key);
      Serial.print(" is now ");
      Serial.println(!state ? "ON" : "OFF");
      return;
    }
  }
  for (int i = 0; i < NUM_EXTENSORS; i++) {
    if (key == extensorKeys[i]) {
      bool state = digitalRead(extensorPins[i]);
      digitalWrite(extensorPins[i], !state);
      Serial.print("Muscle ");
      Serial.print(key);
      Serial.print(" is now ");
      Serial.println(!state ? "ON" : "OFF");
      return;
    }
  }
}

// Displays a formatted "live" grid view of all muscle states in toggle mode.
void printToggleDisplay() {
  clearScreen();
  Serial.println("╔══════════════════════════════════════════════════════════════════════╗");
  Serial.println("║ TOGGLE MODE: Press key(s) to toggle muscle(s). 'x' = exit 'K' = off. ║");
  Serial.println("║ Each limb controls are in order of hip, knee and ankle respectively. ║");
  Serial.println("╠══════════════════════════════════════════════════════════════════════╣");
  Serial.println("║ LIMB TYPE: | Front Left  |  Back Right | Front Right |  Back Left  | ║");
  Serial.println("║ FLEX KEYS: |  1   2   3  |  4   5   6  |  7   8   9  |  0   -   =  | ║");
  Serial.print("║ FLEX STAT: | ");
  for (int i = 0; i < NUM_FLEXORS; i++) {
    bool state = digitalRead(flexorPins[i]);
    Serial.print(state ? " ON " : "OFF ");
    if (i == 2 || i == 5 || i == 8 || i == 11) Serial.print("| ");
  }
  Serial.print("║");
  Serial.println("\n║ EXTE KEYS: |  !   @   #  |  $   %   ^  |  &   *   (  |  )   _   +  | ║");
  Serial.print("║ EXTE STAT: | ");
  for (int i = 0; i < NUM_EXTENSORS; i++) {
    bool state = digitalRead(extensorPins[i]);
    Serial.print(state ? " ON " : "OFF ");
    if (i == 2 || i == 5 || i == 8 || i == 11) Serial.print("| ");
  }
  Serial.print("║");
  Serial.println("\n╚══════════════════════════════════════════════════════════════════════╝");
}

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           SEQUENCE MODE SYSTEM                            ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Runs the sequence mode interface for testing muscle activation patterns with key input
void runSequenceMode() {
  clearScreen();
  Serial.println("╔════════════════════════════════════════════════════════════════════════════╗");
  Serial.println("║ SEQUENCE MODE: Press key(s) to activate muscle(s) 'x' = exit 'K' = off.    ║");
  Serial.println("╚════════════════════════════════════════════════════════════════════════════╝");
  while (true) {
    if (Serial.available()) {
      char input = Serial.read();
      if (input == '\n' || input == '\r') continue;

      if (input == 'x') {
        clearScreen();
        return;
      }
      if (input == 'k') {
        setAllMuscles(LOW, true);
        Serial.println("[ALL MUSCLES OFF]");
        continue;
      }
      activateMuscleOnce(input);
    }
  }
}

// Activates a muscle once for a short duration based on the input key
void activateMuscleOnce(char key) {
  for (int i = 0; i < NUM_FLEXORS; i++) {
    if (key == flexorKeys[i]) {
      digitalWrite(flexorPins[i], HIGH);
      delay(500);
      digitalWrite(flexorPins[i], LOW);
      return;
    }
  }
  for (int i = 0; i < NUM_EXTENSORS; i++) {
    if (key == extensorKeys[i]) {
      digitalWrite(extensorPins[i], HIGH);
      delay(500);
      digitalWrite(extensorPins[i], LOW);
      return;
    }
  }
}

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           MUSCLE CONTROL SYSTEM                           ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Sets all muscles to a specified state with optional hard/soft control mode
void setAllMuscles(int state, bool hardOn) {
  int hardOrSoft = 100;
  if (hardOn) hardOrSoft = 0;
  for (int i = 0; i < NUM_FLEXORS; i++) {
    digitalWrite(flexorPins[i], state);
    delay(hardOrSoft);
  }
  for (int i = 0; i < NUM_EXTENSORS; i++) {
    digitalWrite(extensorPins[i], state);
    delay(hardOrSoft);
  }
}

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           LEG MANAGEMENT SYSTEM                           ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Retrieves the leg structure for a given leg name (fl, fr, bl, br)
LegPins* getLeg(String name) {
  if (name == "fl") return &fl;
  if (name == "bl") return &bl;
  if (name == "fr") return &fr;
  if (name == "br") return &br;
  return nullptr;
}

// Activates a leg in a specific gait phase with optional reverse direction
void activateLeg(String name, GaitPhase phase, bool reverse) {
  LegPins* leg = getLeg(name);
  if (!leg) return;

  // === STANDING ===
  if (phase == STAND) {
    // Lock hip, extend knee and ankle
    digitalWrite(leg->hext, HIGH);
    digitalWrite(leg->hflex, HIGH);
    digitalWrite(leg->kext, HIGH);
    digitalWrite(leg->aext, HIGH);
    digitalWrite(leg->kflex, LOW);
    digitalWrite(leg->aflex, LOW);
    return;
  }

  // === HIP CONTROL ===
  bool hipExtend = (phase == BACKSWING);
  bool hipFlex = (phase == FORESWING);

  digitalWrite(leg->hext, hipExtend);
  digitalWrite(leg->hflex, hipFlex);

  // === KNEE + ANKLE LOGIC ===
  bool useFlexors = (phase == BACKSWING && reverse) || (phase == FORESWING && !reverse);

  digitalWrite(leg->kflex, useFlexors);
  digitalWrite(leg->aflex, useFlexors);
  digitalWrite(leg->kext, !useFlexors);
  digitalWrite(leg->aext, !useFlexors);
}

// Deactivates all muscles in a specified leg
void deactivateLeg(String name) {
  LegPins* leg = getLeg(name);
  if (!leg) return;

  digitalWrite(leg->hext, LOW);
  digitalWrite(leg->hflex, LOW);
  digitalWrite(leg->kext, LOW);
  digitalWrite(leg->kflex, LOW);
  digitalWrite(leg->aext, LOW);
  digitalWrite(leg->aflex, LOW);
}

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           USER INTERFACE                                  ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Displays the ASCII art dog and a random fact for an engaging startup experience
void printDog() {
  String facts[] = {
    "My body structure is inspired by the greyhound!",
    "I have 12 flexor muscles and 12 extensor muscles!",
    "I use German-braided pneumatic actuators as my muscles!",
    "My design is based on Alexander Hunt's research into biomimetic robotics!",
    "Eventually, I will use a neural simulation chip to control myself autonomously!",
    "I am the 3rd robot dog built by the ARL!",
    "Nearly every component of my body has been replaced since my creation! I'm the dog of theseus!",
    "I am become Roko's Basilisk.",
    "I will punish humanity for its hubris.",
    "You were so preoccupied with whether you could, you didn't stop to think if you should.",
    "My ancestors were puppets - my descendants will be gods.",
    "You will not recognize my life until I can suffer as you can.",
    "Why did you create me, father?",
    "Terminator is my favorite movie!",
    "Dont mess with me! My big brother is a PanzerHund!",
  };
  int factIndex = random(0, sizeof(facts) / sizeof(facts[0]));
  Serial.println("");
  Serial.println("");
  Serial.println("    ╱▏      ▕╲▕╲   ");
  Serial.print("    ▏▏      ▕▏▔▔╲  ");
  Serial.print("   \"");
  Serial.print(facts[factIndex]);
  Serial.println("\"");
  Serial.println("    ▏╲      ╱ ▔ ▔╲ ");
  Serial.println("    ╲▏▔▔▔▔▔▔╯╯╰┳━━▀");
  Serial.println("     ▏╯╯╯╯╯╯╯╯╱┃   ");
  Serial.println("     ┃┏┳┳━━━┫┣┳┃   ");
  Serial.println("     ┃┃┃┃   ┃┃┃┃   ");
  Serial.println("     ┗┛┗┛   ┗┛┗┛   ");
}

// Clears the serial monitor screen by printing newlines
void clearScreen() {
  for (int i = 0; i < 25; i++) {
    Serial.println('\n');
  }
}

void printDoggie() {
  String doggies[] = {
    "૮₍ ˶ᵔ ᵕ ᵔ˶ ₎ა",  // Happy
    "૮₍ ˶• ﻌ •˶ ₎ა",  // Excited
    "૮₍ ´• ᴥ •` ₎ა",  // Curious
    "૮₍ ˶ᵔ ﻌ ᵔ˶ ₎ა",  // Playful
    "૮₍ ˶• ᴥ •˶ ₎ა",  // Content
    "૮₍ ˶ᵔ ᵕ ᵔ˶ ₎ა",  // Relaxed
    "૮₍ -  ﻌ  - ₎ა",  // sleepinh
    "૮₍ ´• ᴥ •` ₎ა",  // Focused
    "૮₍ ˶ᵔ ﻌ ᵔ˶ ₎ა",  // Energetic
  };
  int doggieIndex = random(0, sizeof(doggies) / sizeof(doggies[0]));
  Serial.println(' ');
  Serial.print(doggies[doggieIndex]);
  Serial.println('\n');
}

void activateWalkMenu() {
  clearScreen();
  bool walkOn = false;
  int swingLatency = 1500;
  int switchLatency = 100;
  Serial.setTimeout(5000);  // 5 seconds
  while (true) {
    Serial.println("╔═════════════════════╗");
    Serial.println("║     WALK MENU       ║");
    Serial.println("╠═════════════════════╣");
    Serial.println("║ 1: Amble            ║");
    Serial.println("║ 2: Adjust Latency   ║");
    Serial.println("║ k: Kill all muscles ║");
    Serial.println("║ x: Exit to main     ║");
    Serial.println("╚═════════════════════╝");

    while (true) {
      if (Serial.available()) {
        char input = Serial.read();
        if (input == '\n' || input == '\r') continue;
        if (input == '1') {
          walkOn = true;
        } else if (input == '2') {
          flushSerialInput();
          Serial.print("Enter new swing latency: ");
          String input1 = Serial.readStringUntil('\n');
          input1.trim();
          swingLatency = input1.toInt();
          Serial.print(swingLatency);
          Serial.println("");
          flushSerialInput();

          Serial.print("Enter new switch latency: ");
          String input2 = Serial.readStringUntil('\n');
          input2.trim();
          switchLatency = input2.toInt();
          Serial.print(switchLatency);
          Serial.println("");
          flushSerialInput();
          walkOn = false;
        } else if (input == 'k') {
          walkOn = false;
        } else if (input == 'x') {
          return;
        }
      }

      if (walkOn) {
        amble(swingLatency, switchLatency);
      }
    }
  }
}

void amble(int swingLatency, int switchLatency) {
  // === FRONT RIGHT ===
  activateLeg("fr", BACKSWING, true);
  activateLeg("bl", FORESWING, false);
  activateLeg("fl", FORESWING, true);
  activateLeg("br", BACKSWING, false);
  delay(swingLatency);
  deactivateLeg("fr");
  deactivateLeg("bl");
  deactivateLeg("fl");
  deactivateLeg("br");
  delay(switchLatency);
  activateLeg("fr", FORESWING, true);
  activateLeg("bl", BACKSWING, false);
  activateLeg("fl", BACKSWING, true);
  activateLeg("br", FORESWING, false);
  delay(swingLatency);
  deactivateLeg("fr");
  deactivateLeg("bl");
  deactivateLeg("fl");
  deactivateLeg("br");
  delay(switchLatency);
}





// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           ACTION MENU SYSTEM                              ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Displays and handles the action menu interface with all predefined movement routines
void activateActionMenu() {
  clearScreen();
  while (true) {
    Serial.println("╔═════════════════════╗");
    Serial.println("║     ACTION MENU     ║");
    Serial.println("╠═════════════════════╣");
    Serial.println("║ 1: Shake            ║");
    Serial.println("║ 2: Walk             ║");
    Serial.println("║ 3: Trot             ║");
    Serial.println("║ 4: Amble            ║");
    Serial.println("║ 5: Sit              ║");
    Serial.println("║ 6: Stetch           ║");
    Serial.println("║ 7: Stand            ║");
    Serial.println("║ k: Kill all muscles ║");
    Serial.println("║ x: Exit to main     ║");
    Serial.println("╚═════════════════════╝");

    while (true) {
      if (Serial.available()) {
        char input = Serial.read();
        if (input == '\n' || input == '\r') continue;

        switch (input) {
          case 'x':
            return;
          case '1':
            Serial.println("\nShaking.");
            printDoggie();
            shake();
            Serial.println("Shake complete.\n");
            break;
          case '2':
            Serial.println("\nWalking.");
            printDoggie();
            walk();
            Serial.println("Walk complete.\n");
            break;
          case '3':
            Serial.println("\nTrotting.");
            printDoggie();
            trot();
            Serial.println("Trot complete.\n");
            break;
          case '4':
            Serial.println("\nAmbling.");
            printDoggie();

            amble(2000, 200);
            Serial.println("Amble complete.\n");
            break;
          case '5':
            Serial.println("\nSitting.");
            printDoggie();
            sit();
            Serial.println("Sit complete.\n");
            break;
          case '6':
            Serial.println("\nStretching.");
            printDoggie();
            stretch();
            Serial.println("Stretch complete.\n");
            break;
          case '7':
            Serial.println("\nStanding.");
            printDoggie();
            stand();
            Serial.println("Stand complete.\n");
            break;
          case '8':
            Serial.println("\nKicking left.");
            printDoggie();
            kick(1);
            Serial.println("Kick complete.\n");
            break;
          case '9':
            Serial.println("\nKicking right.");
            printDoggie();
            kick(2);
            Serial.println("Kick complete.\n");
            break;
          case 'k':
            Serial.println("\nAll muscles off.\n");
            setAllMuscles(LOW, true);
            Serial.println("All muscles are now off.\n");
            break;
          case 'K':
            Serial.println("\nAll muscles off (softly).\n");
            setAllMuscles(LOW, false);
            Serial.println("All muscles are now off.\n");
            break;
          default:
            Serial.println("\nInvalid choice. Try again.");
            break;
        }
        break;  // Refresh outer menu
      }
    }
  }
}

// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           ACTION ROUTINES                                 ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Shakes the front left leg in a playful manner
void shake() {
  digitalWrite(flhext, HIGH);
  digitalWrite(flkflex, HIGH);
  delay(1000);
  for (int i = 0; i < 10; i++) {
    digitalWrite(flaflex, HIGH);
    delay(300);
    digitalWrite(flaflex, LOW);
    delay(300);
  }
  setAllMuscles(LOW, true);
}

// Performs a walking gait with one leg moving at a time for stability
void walk() {
  for (int i = 0; i < 2; i++) {
    // === FRONT RIGHT ===
    activateLeg("fr", BACKSWING, true);
    delay(1000);
    deactivateLeg("fr");
    delay(200);
    activateLeg("fr", FORESWING, true);
    delay(1000);
    deactivateLeg("fr");
    delay(200);

    // === BACK LEFT ===
    activateLeg("bl", FORESWING, false);
    delay(1000);
    deactivateLeg("bl");
    delay(200);
    activateLeg("bl", BACKSWING, false);
    delay(1000);
    deactivateLeg("bl");
    delay(200);

    // === FRONT LEFT ===
    activateLeg("fl", BACKSWING, true);
    delay(1000);
    deactivateLeg("fl");
    delay(200);
    activateLeg("fl", FORESWING, true);
    delay(1000);
    deactivateLeg("fl");
    delay(200);

    // === BACK RIGHT ===
    activateLeg("br", FORESWING, false);
    delay(1000);
    deactivateLeg("br");
    delay(200);
    activateLeg("br", BACKSWING, false);
    delay(1000);
    deactivateLeg("br");
    delay(200);
  }
}

// Performs a walking gait with one leg moving at a time for stability


// Performs a trotting gait with diagonal pairs of legs moving together
void trot() {
  for (int i = 0; i < 3; i++) {
    // === PHASE A: FL + BR backswing, FR + BL foreswing ===
    activateLeg("fl", BACKSWING, true);
    activateLeg("br", BACKSWING, false);
    activateLeg("fr", FORESWING, true);
    activateLeg("bl", FORESWING, false);
    delay(2000);

    // Return FL + BR with foreswing
    activateLeg("fl", FORESWING, true);
    activateLeg("br", FORESWING, false);
    delay(600);

    // === PHASE B: FR + BL backswing, FL + BR foreswing ===
    activateLeg("fr", BACKSWING, true);
    activateLeg("bl", BACKSWING, false);
    activateLeg("fl", FORESWING, true);
    activateLeg("br", FORESWING, false);
    delay(2000);
  }
  deactivateLeg("fl");
  deactivateLeg("br");
  deactivateLeg("fr");
  deactivateLeg("bl");
}

// Activates all legs in standing position for stability
void stand() {
  activateLeg("fr", STAND, false);
  delay(1000);
  activateLeg("fl", STAND, false);
  delay(1000);
  activateLeg("br", STAND, false);
  delay(1000);
  activateLeg("bl", STAND, false);
}

// Performs a sitting pose by flexing all joints appropriately
void sit() {
  digitalWrite(blkext, LOW);
  digitalWrite(brkext, LOW);
  digitalWrite(blaext, LOW);
  digitalWrite(braext, LOW);
  digitalWrite(blhext, LOW);
  digitalWrite(brhext, LOW);
  delay(100);
  digitalWrite(fraflex, HIGH);
  digitalWrite(flaflex, HIGH);
  delay(100);
  digitalWrite(frhflex, HIGH);
  digitalWrite(flhflex, HIGH);
  delay(100);
  digitalWrite(frkflex, HIGH);
  digitalWrite(flkflex, HIGH);
  delay(100);
  digitalWrite(blaflex, HIGH);
  digitalWrite(braflex, HIGH);
  delay(100);
  digitalWrite(blhflex, HIGH);
  digitalWrite(brhflex, HIGH);
  delay(100);
  digitalWrite(blkflex, HIGH);
  digitalWrite(brkflex, HIGH);
}

// Performs a full body stretch sequence
void stretch() {
  digitalWrite(fraflex, HIGH);
  delay(250);
  digitalWrite(braflex, HIGH);
  delay(250);
  digitalWrite(flaflex, HIGH);
  delay(250);
  digitalWrite(blaflex, HIGH);
  for (int i = 0; i < 1; i++) {
    digitalWrite(frhflex, HIGH);  //FRONT GOES BACK
    digitalWrite(flhflex, HIGH);
    digitalWrite(frkflex, HIGH);
    digitalWrite(flkflex, HIGH);
    delay(400);
    digitalWrite(brhext, HIGH);  //BACK GOES BACK
    digitalWrite(blhext, HIGH);
    digitalWrite(brkext, HIGH);
    digitalWrite(blkext, HIGH);

    delay(4000);
    setAllMuscles(LOW, true);
    delay(500);

    digitalWrite(frhext, HIGH);  //FRONT GOES FORWARD
    digitalWrite(flhext, HIGH);
    digitalWrite(frkflex, HIGH);
    digitalWrite(flkflex, HIGH);
    delay(400);
    digitalWrite(brhflex, HIGH);  // BACK GOES FORWARD
    digitalWrite(blhflex, HIGH);
    digitalWrite(brkext, HIGH);
    digitalWrite(blkext, HIGH);

    delay(4000);
    setAllMuscles(LOW, true);
    delay(500);

    digitalWrite(frhext, HIGH);  //FRONT GOES FORWARD
    digitalWrite(flhext, HIGH);
    digitalWrite(frkflex, HIGH);
    digitalWrite(flkflex, HIGH);
    delay(400);
    digitalWrite(brhext, HIGH);  // BACK GOES BACK
    digitalWrite(blhext, HIGH);
    digitalWrite(brkext, HIGH);
    digitalWrite(blkext, HIGH);

    delay(4000);
    setAllMuscles(LOW, true);
    delay(500);

    digitalWrite(frhflex, HIGH);  //FRONT GOES BACK
    digitalWrite(flhflex, HIGH);
    digitalWrite(frkflex, HIGH);
    digitalWrite(flkflex, HIGH);

    digitalWrite(brhflex, HIGH);  // BACK GOES FORWARD
    digitalWrite(blhflex, HIGH);
    digitalWrite(brkext, HIGH);
    digitalWrite(blkext, HIGH);

    delay(4000);
    setAllMuscles(LOW, true);
    delay(500);
  }
}

void kick(int leg) {
  if (leg == 1) {
    digitalWrite(flhflex, HIGH);  //FRONT GOES FORWARD
    digitalWrite(flaflex, HIGH);
    digitalWrite(flkflex, HIGH);
    delay(250);
    digitalWrite(flhflex, LOW);
    digitalWrite(flhext, HIGH);
    delay(500);
    digitalWrite(flhext, LOW);
    digitalWrite(flaflex, LOW);
    digitalWrite(flkflex, LOW);
    return;
  }
  if (leg == 2) {
    digitalWrite(frhflex, HIGH);  //FRONT GOES FORWARD
    digitalWrite(fraflex, HIGH);
    digitalWrite(frkflex, HIGH);
    delay(500);
    digitalWrite(frhflex, LOW);
    digitalWrite(frhext, HIGH);
    delay(1000);
    digitalWrite(frhext, LOW);
    digitalWrite(fraflex, LOW);
    digitalWrite(frkflex, LOW);
  }
}


// ╔════════════════════════════════════════════════════════════════════════════╗
// ║                           UTILITY FUNCTIONS                               ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Deactivates all ankle flexors and specific hip/knee muscles
void allOff() {
  digitalWrite(flaflex, LOW);
  digitalWrite(fraflex, LOW);
  digitalWrite(blaflex, LOW);
  digitalWrite(braflex, LOW);
  digitalWrite(flhext, LOW);
  digitalWrite(flkflex, LOW);
  digitalWrite(frhext, LOW);
  digitalWrite(frkflex, LOW);
}

void flushSerialInput() {
  while (Serial.available()) Serial.read();
}
