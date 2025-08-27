//Timer_Interrupt.c

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>

#define F_CPU 8000000UL  // 8 MHz CPU Clock Frequency
#include <util/delay.h>

#define sbi(var, mask)   ((var) |= (uint8_t)(1 << mask))
#define cbi(var, mask)   ((var) &= (uint8_t)~(1 << mask))

// encoder position recording (available globally, but editable within the interrupt via the "volatile" declaration)
volatile uint8_t enc_val0 = 0;
volatile uint8_t enc_val1 = 0;
volatile unsigned int enc_count0;
volatile unsigned int enc_count1;

static int lookup_table[] = {0,0,0,-1,0,0,1,0,0,1,0,0,-1,0,0,0}; // map change in encoder values to motion. use only one interrupt

//ISR(INT0_vect) {
//enc_val0 = enc_val0 << 2;						// leave space for new encoder reading
//enc_val0 = enc_val0 | ((PIND & 0b1100) >> 2);	// drop new encoder values in the open space
//
//enc_count0 = enc_count0 + lookup_table[enc_val0 & 0b1111]; // map the change in encoder values using the lookup table
//}
//
//ISR(INT1_vect) {
//enc_val1 = enc_val1 << 2;						// leave space for new encoder reading
//enc_val1 = enc_val1 | ((PIND & 0b11000) >> 3);	// drop new encoder values in the open space
//
//enc_count1 = enc_count1 + lookup_table[enc_val1 & 0b1111]; // map the change in encoder values using the lookup table
//}

int main (void) {
	
	// Set up a toggle pin
	DDRC |= (1 << PC5);
	
	// SPI initialization
	DDRB |= (1 << DDB4);							//Set MISO as an output
	DDRB &= ~((1 << DDB3)|(1 << DDB5)|(1 << DDB2)); // Set MOSI, SCK, and SS pins as inputs (this step is redundant, but makes the code more readable).

	SPCR = (1 << SPE); // SPI activation -- ATmega configured as peripheral
	
	// Encoder initialization
	EIMSK |= ((1 << INT0)|(1 << INT1)); // Activity on INT0 or INT1 triggers an interrupt
	EICRA |= ((1<<ISC00)|(1<<ISC10));  // Any logical change on INT0 or INT1 generates an interrupt request
	
	//sei();
	
	PORTC |= ~(1 << PC5);
	
	SPDR = 0x00; // Load MISO line. This might not be necessary
	
	while (1) {

		if (SPSR & (1<<SPIF)) {
			
			PORTC ^= (1 << PC5); // toggle C5
			
			char teensy_request = SPDR;
			
			if (teensy_request == 0xFF) {
				//SPDR = enc_count0 >> 8;
				SPDR = 0xAA;
			}
			else if (teensy_request == 0x0F) {
				//SPDR = enc_count0 & 0xFF;
				SPDR = 0xBB;
			}
			if (teensy_request == 0xEE) {
				//SPDR = enc_count1 >> 8;
				SPDR = 0xCC;
			}
			else if (teensy_request == 0x0E) {
				//SPDR = enc_count1 & 0xFF;
				SPDR = 0xDD;
			}
			else {
				SPDR = 0x00;
			}
			
		}
	}
}