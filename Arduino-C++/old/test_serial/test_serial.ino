// Help from ChatoGPT here

const uint8_t packet_size = 4;

uint8_t buffer[packet_size];
uint8_t buffer_index = 0;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
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

      Serial.write(buffer, packet_size);
      digitalWrite(LED_BUILTIN, HIGH);
      delay(10);
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
  delay(1);
}