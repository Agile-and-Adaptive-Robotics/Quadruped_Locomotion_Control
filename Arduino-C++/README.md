# Teensy Side


## Teensy Data Receiving

Reference: https://docs.arduino.cc/learn/communication/spi/

Teensy 4.1 Parameters:
~ Max device speed should be around 60 MHz. However, I think we will probably need to round down here.
~ We will use MSH first data order.
~ Data clock will be idle when LOW, and samples will be on the leading edge of clock pulses.
~ This corresponds to MODE0 on the Teensy.

## Running through each CS pin

Reference: https://docs.arduino.cc/built-in-examples/control-structures/Arrays/