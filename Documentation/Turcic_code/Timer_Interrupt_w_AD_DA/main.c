//Timer_Interrupt.c

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>

#define F_CPU 16000000UL  // 16 MHz CPU Clock Frequency
#include <util/delay.h>

#define sbi(var, mask)   ((var) |= (uint8_t)(1 << mask))
#define cbi(var, mask)   ((var) &= (uint8_t)~(1 << mask))
#define SPIF 7

// All variables that are declared outside the interrupt function and are referenced or changed
// inside the interrupt function must be declared as volatile.  For example "volatile float Kp = 0;"

// SPI write read function
volatile unsigned char DA_write(volatile unsigned char spi_data)
{
	SPDR=spi_data;
	while ((SPSR & (1<<SPIF))==0);	// Wait until the data transfer is complete
	return SPDR;
}

// define variables to be used for ad/da conversion and spi communication
volatile unsigned int adc_data;

volatile unsigned char   upper_half;
volatile unsigned char   lower_half;
volatile unsigned char   dummy_read;

#define LEDs	PORTD
#define red		0b01111111
#define green	0b10111111
#define yellow	0b11011111

int main (void)
{

	DDRB   = 0b00101100; //Set Output Ports for the SPI Interface
	DDRD   = 0b11100000; //Set ports 6, 7 and 8 as outputs for the LEDs
	ADCSRA = 0b10000111; // ADC on, /128 for a 16 MHz clock, interrupt off

	// SPI initialization
	SPCR=0b01010000;
	SPSR=0b00000001;
	
		
	DDRC = (1 << 5); // Set Pin 5 on Port C as output

	TCCR1B |= (1 << WGM12); // Configure timer 1 for CTC mode

	TIMSK1 |= (1 << OCIE1A); // Enable CTC interrupt

	sei(); // Enable global interrupts

	// OCR1A = Target_Timer_Count = (Clock_Frequency / (Prescale * Target_Frequency)) – 1

	OCR1A = 15999;   //Set CTC compare value to 5000 Hz at 16 MHz AVR clock, with a prescaler of 1

	TCCR1B |= ((1 << CS10) | (0 << CS11) | (0 << CS12)); // No prescaler

	while(1){}

}

ISR(TIMER1_COMPA_vect)
{
	PORTC ^= (1 << 5); // Toggle Pin 5 on Port C
	
	
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