//Timer_Interrupt.c

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>

#define F_CPU 16000000UL  // 16 MHz CPU Clock Frequency
#include <util/delay.h>

#define sbi(var, mask)   ((var) |= (uint8_t)(1 << mask))
#define cbi(var, mask)   ((var) &= (uint8_t)~(1 << mask))

// encoder position recording (available globally, but editable within the interrupt via the "volatile" declaration)
volatile uint8_t enc_val = 0;
volatile unsigned int enc_count;

static int lookup_table[] = {0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0};


// SPI write read function
char SPI_write(char spi_data)
{
	SPDR=spi_data;
	while ((SPSR & (1<<SPIF))==0);	// Wait until the data transfer is complete
	return SPDR;
}


char SPI_read(void) {
	while ((SPSR & (1<<SPIF))==0);	// Wait until the data transfer is complete
	return SPDR;
}


ISR(INT0_vect) {
	enc_val = enc_val << 2;
	enc_val = enc_val | ((PIND & 0b1100) >> 3);
	
	enc_count = enc_count + lookup_table[enc_val & 0b1111];
}

int main (void) {
	
	// SPI initialization
	DDRB |= (1 << DDB4);							//Set MISO as an output
	DDRB &= ~((1 << DDB3)|(1 << DDB5)|(1 << DDB2)); // Set MOSI, SCK, and SS pins as inputs (this step is redundant, but makes the code more readable).

	SPCR = (1 << SPE); // ATmega configured as peripheral
	
	// Encoder initialization
	EIMSK |= (1 << INT0); // Activity on INT0 triggers an interrupt
	EICRA |= (1<<ISC10);  // Any logical change on INT0 generates an interrupt request
	
	sei();
	
	while (1) {
		if (!(PINB & (1 << PB2))) { // Triggered when PB2 CS pin is LOW (pulled by Teensy) 
			char teensy_request = SPI_read();
			if (teensy_request == 0xB0) { // MSB byte request
				SPI_write(enc_count >> 8);
			}
			if (teensy_request == 0x0B) { // LSB byte request
				SPI_write(enc_count & 0xFF);
			}
		}
	}
}