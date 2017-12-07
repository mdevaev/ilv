#include <Arduino.h>
#include <TimerOne.h>
#include <digitalWriteFast.h>

#define INLINE inline __attribute__((always_inline))
#define ASYMMETRICAL_FILAMENT 10


const uint8_t CLOCK_PIN = A1;
const uint8_t BLANK_PIN = A2;
const uint8_t LOAD_PIN = A0;
const uint8_t GRIDS_PIN = 9;
const uint8_t DRIVERS_PINS[6] = {12, 11, 10, 8, 7, 6};
const uint8_t FILAMENT_ENABLE_PIN = A3;
const uint8_t FILAMENT_AC_PINS[2] = {A4, A5};
const uint8_t READY_PIN = 13;

const uint16_t COLUMNS_MASKS[16] = {
	0b1000000000000000,
	0b0100000000000000,
	0b0010000000000000,
	0b0001000000000000,
	0b0000100000000000,
	0b0000010000000000,
	0b0000001000000000,
	0b0000000100000000,
	0b0000000010000000,
	0b0000000001000000,
	0b0000000000100000,
	0b0000000000010000,
	0b0000000000001000,
	0b0000000000000100,
	0b0000000000000010,
	0b0000000000000001,
};


static uint16_t screens[2][120];
static uint8_t current_screen = 0;
static uint8_t next_screen = 1;
static uint8_t translated_pixel_indexes[105];


INLINE void writeData(uint8_t column, uint16_t screen[]) {
	for (uint8_t index = 0; index < 20; ++index) {
		digitalWriteFast(GRIDS_PIN, column == index - 4);
		for (uint8_t driver = 1; driver <= 6; ++driver) {
			digitalWriteFast(DRIVERS_PINS[driver - 1], (bool)(screen[(driver * 20 - 20) + index] & COLUMNS_MASKS[column]));
		}
		digitalWriteFast(CLOCK_PIN, HIGH);
		digitalWriteFast(CLOCK_PIN, LOW);
	}
	digitalWriteFast(LOAD_PIN, HIGH);
	digitalWriteFast(LOAD_PIN, LOW);
}

INLINE void drawColumn() {
	static uint8_t column;
	writeData(column, screens[current_screen]);
	column = (column == 15 ? 0 : column + 1);
}

void pulseFilament() {
#ifdef ASYMMETRICAL_FILAMENT
	static uint8_t filament_mode;
#else
	static bool filament_mode;
#endif
	digitalWriteFast(FILAMENT_AC_PINS[0], filament_mode);
	digitalWriteFast(FILAMENT_AC_PINS[1], !filament_mode);
#ifdef ASYMMETRICAL_FILAMENT
	filament_mode = (filament_mode == ASYMMETRICAL_FILAMENT ? 0 : filament_mode + 1);
#else
	filament_mode = !filament_mode;
#endif
}

void buildTranslatedPixelIndexes() {
	for (uint8_t index = 0; index < 105; ++index) {
		if (index < 35) {
			translated_pixel_indexes[index] = 15 + ((index % 2) ? (51 - (index + 1) / 2) : (51 + index / 2));
		} else if (index < 70) {
			translated_pixel_indexes[index] = 15 + ((index % 2) ? (51 + (index + 1) / 2) : (51 - index / 2));
		} else {
			translated_pixel_indexes[index] = 15 + ((index % 2) ? (52 - (index + 1) / 2) : (52 + index / 2));
		}
	}
}


void setup() {
	pinModeFast(FILAMENT_AC_PINS[0], OUTPUT);
	pinModeFast(FILAMENT_AC_PINS[1], OUTPUT);
	pinModeFast(FILAMENT_ENABLE_PIN, OUTPUT);

	Timer1.initialize(200); // 500
	Timer1.attachInterrupt(pulseFilament);

	pinModeFast(CLOCK_PIN, OUTPUT);
	pinModeFast(BLANK_PIN, OUTPUT);
	pinModeFast(LOAD_PIN, OUTPUT);
	pinModeFast(GRIDS_PIN, OUTPUT);
	for (uint8_t driver = 0; driver < 6; ++driver) {
		pinModeFast(DRIVERS_PINS[driver], OUTPUT);
	}

	digitalWriteFast(BLANK_PIN, HIGH);
	delay(500);
	digitalWriteFast(BLANK_PIN, LOW);

	Serial.begin(115200);

	buildTranslatedPixelIndexes();

	pinModeFast(READY_PIN, OUTPUT);
	digitalWriteFast(READY_PIN, HIGH);
}


INLINE void cmdFilament() {
	int8_t enabled;
	while ((enabled = Serial.read()) == -1) {
		drawColumn();
	}
	digitalWriteFast(FILAMENT_ENABLE_PIN, enabled);
}

INLINE void cmdScreen() {
	for (uint8_t index = 0;;) {
		while (Serial.available() >= 2) {
			screens[next_screen][translated_pixel_indexes[index]] = (uint16_t)Serial.read() << 8;
			screens[next_screen][translated_pixel_indexes[index]] |= (uint16_t)Serial.read();
			if (index % 15 == 0) {
				drawColumn();
			}
			if (index == 104) {
				current_screen ^= next_screen;
				next_screen ^= current_screen;
				current_screen ^= next_screen;
				return;
			} else {
				++index;
			}
		}
		drawColumn();
	}
}

void loop() {
	while (true) {  // fast
		switch (Serial.read()) {
			case 0: cmdFilament(); break;
			case 1: cmdScreen(); break;
			default: break;
		}
		drawColumn();
	}
}
