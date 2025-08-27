
// SPI_test_WIN_Avr_ATmega8.c

#include <avr/io.h>
#include <stdio.h>

#define F_CPU 16000000UL  // 16 MHz CPU Clock Frequency
#include <util/delay.h>

#define sbi(var, mask)   ((var) |= (uint8_t)(1 << mask))
#define cbi(var, mask)   ((var) &= (uint8_t)~(1 << mask))
#define SPIF 7


// SPI write read function
unsigned char DA_write(unsigned char spi_data)
{
	SPDR=spi_data;
	while ((SPSR & (1<<SPIF))==0);	// Wait until the data transfer is complete
	return SPDR;
}

int main (void)
{
	unsigned int adc_data;
	
	unsigned char   upper_half;
	unsigned char   lower_half;
	unsigned char   dummy_read;

	DDRB   = 0b00101100; //Set Output Ports for the SPI Interface
	DDRD   = 0b11100000; //Set ports 6, 7 and 8 as outputs for the LEDs
	ADCSRA = 0b10000111; // ADC on, /128 for a 16 MHz clock, interrupt off
	
	#define LEDs	PORTD
	#define red		0b01111111
	#define green	0b10111111
	#define yellow	0b11011111

	// SPI initialization
	SPCR=0b01010000;
	SPSR=0b00000001;

	while(1)
	{
		ADMUX  = 0b00000000; //Input on AD Channel 0
		
		ADCSRA = ADCSRA | 0b01000000;  // Start AD conversion

		while ((ADCSRA & 0b01000000) == 0b01000000); // Wait while AD conversion is executed

		adc_data = (ADCW << 2); // multiply by 2...
		
		if(adc_data > (3*4096)/5)
		{
			LEDs = red;
		}
		else if (adc_data < (2*4096)/5)
		{
			LEDs = yellow;
		}
		else
		{
			LEDs = green;
		}
		
		upper_half = 0x00; // Reset the upper value
		
		upper_half = (adc_data & 0x0F00) >> 8; // Take the upper portion of the value of x
		upper_half = upper_half + 0b00110000; // Add the control bits for the DA chip
		
		lower_half = adc_data & 0xFF; // Pull the less significant bits from x

		cbi(PORTB,2);								// Activate the chip - set chip select to zero
		dummy_read = DA_write(upper_half);			// Write/Read first byte
		dummy_read = DA_write(lower_half);  		// Write/Read second byte
		sbi(PORTB,2);								// Release the chip  - set chip select to one
		
	}

}





