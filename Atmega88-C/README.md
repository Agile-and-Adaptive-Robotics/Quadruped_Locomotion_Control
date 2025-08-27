# Teensy/ATmega88 SPI bus protocol

## ATmega88 Data Sending

Resources from Dr. Turcic's class on microcontrollers were used. In addition, a tutorial on setting up two ATmega devices in control and peripheral mode's with SPI was used to help understand initializing the ATmega88 as a peripheral device https://www.electronicwings.com/avr-atmega/atmega1632-spi.

### ATmega88 Encoder Reading

Reference: http://makeatronics.blogspot.com/2013/02/efficiently-reading-quadrature-with.html#:~:text=Incremental%20is%20rather%20useless%20for,be%20seen%20in%20the%20diagram.

The most lightweight model makes use of a lookup table, which captures new and old states driven by interrupts in the ATmega88. 
Interrupts are driven by Channel A (white wire) on the encoder via the INT0 PD2 pin. 
Channel B is connected to INT1 PD3.

<img width="400" alt="pinout_ATmega88A" src="https://github.com/user-attachments/assets/3362d00e-f0fe-462f-a3a9-997535e18fd8" />


