#include <Arduino.h>
#include <TimerOne.h>
#include <digitalWriteFast.h>


#define INLINE inline __attribute__((always_inline))


#define CMD_SERIAL Serial
#define CMD_SERIAL_SPEED 115200

#define FILAMENT_ASYMMETRICAL 4
#define FILAMENT_PULSE_TIME 100 // Микросекунд


const uint8_t PIN_CLOCK = A0;
const uint8_t PIN_BLANK = A2;
const uint8_t PIN_LOAD = A1;

const uint8_t PIN_GRID_DRIVER = 6;
const uint8_t PIN_PIXEL_DRIVERS[6] = {9, 8, 7, 5, 4, 3};

const uint8_t PIN_PULSE_FILAMENT = 100;
const uint8_t PIN_ENABLE_DCDCS = A3;


// -----------------------------------------------------------------------------
static uint16_t screens[2][120];
static uint8_t current_screen = 0;
static uint8_t next_screen = 1;

static uint8_t pixel_map[105];
static uint16_t column_masks[16];


// -----------------------------------------------------------------------------
INLINE void writeColumnData(uint8_t column, uint16_t screen[]) {
	for (uint8_t pin = 0; pin < 20; ++pin) {
		digitalWriteFast(PIN_GRID_DRIVER, column == pin - 2);
		for (uint8_t driver = 1; driver <= 6; ++driver) {
			digitalWriteFast(PIN_PIXEL_DRIVERS[driver - 1], (bool)(screen[(driver * 20 - 20) + pin] & column_masks[column]));
		}
		digitalWriteFast(PIN_CLOCK, HIGH);
		digitalWriteFast(PIN_CLOCK, LOW);
	}
	digitalWriteFast(PIN_LOAD, HIGH);
	digitalWriteFast(PIN_LOAD, LOW);
}

INLINE void drawColumn(void) {
	static uint8_t column;
	writeColumnData(column, screens[current_screen]);
	column = (column == 15 ? 0 : column + 1);
}

void pulseFilament() {
#	ifdef FILAMENT_ASYMMETRICAL
	static uint8_t mode;
#	else
	static bool mode;
#	endif

	digitalWriteFast(PIN_PULSE_FILAMENT, !mode);
#	ifdef FILAMENT_ASYMMETRICAL
	mode = (mode == FILAMENT_ASYMMETRICAL ? 0 : mode + 1);
#	else
	mode = !mode;
#	endif
}

void buildPixelMap() {
	// Номер пикселя по порядку не соответствует номеру пикселя в распиновке экрана,
	// поэтому мы строим карту соответствий виртуальной позиции пикселя реальной распиновке.
	for (uint8_t index = 0; index < 105; ++index) {
		if (index < 35) {
			pixel_map[index] = 15 + ((index % 2) ? (51 - (index + 1) / 2) : (51 + index / 2));
		} else if (index < 70) {
			pixel_map[index] = 15 + ((index % 2) ? (51 + (index + 1) / 2) : (51 - index / 2));
		} else {
			pixel_map[index] = 15 + ((index % 2) ? (52 - (index + 1) / 2) : (52 + index / 2));
		}
	}
}

void buildColumnMasks() {
	// 0 = 0b1000000000000000
	// 1 = 0b0100000000000000
	// ... etc.
	for (int8_t index = 0; index < 16; ++index) {
		column_masks[index] = (uint16_t)1 << (15 - index);
	}
}


// -----------------------------------------------------------------------------
INLINE void cmdDcdcs() {
	int8_t enabled;
	while ((enabled = CMD_SERIAL.read()) == -1) {
		drawColumn();
	}
	digitalWriteFast(PIN_ENABLE_DCDCS, enabled);
}

INLINE void cmdScreen() {
	for (uint8_t index = 0;;) {
		while (CMD_SERIAL.available() >= 2) {
			screens[next_screen][pixel_map[index]] = (uint16_t)CMD_SERIAL.read() << 8;
			screens[next_screen][pixel_map[index]] |= (uint16_t)CMD_SERIAL.read();
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

void setup() {
	buildPixelMap();
	buildColumnMasks();

	pinModeFast(PIN_PULSE_FILAMENT, OUTPUT);
	pinModeFast(PIN_ENABLE_DCDCS, OUTPUT);

	Timer1.initialize(FILAMENT_PULSE_TIME);
	Timer1.attachInterrupt(pulseFilament);

	pinModeFast(PIN_CLOCK, OUTPUT);
	pinModeFast(PIN_BLANK, OUTPUT);
	pinModeFast(PIN_LOAD, OUTPUT);
	pinModeFast(PIN_GRID_DRIVER, OUTPUT);
	for (uint8_t driver = 0; driver < 6; ++driver) {
		pinModeFast(PIN_PIXEL_DRIVERS[driver], OUTPUT);
	}

	digitalWriteFast(PIN_BLANK, HIGH);
	delay(250);

	CMD_SERIAL.begin(CMD_SERIAL_SPEED);

	digitalWriteFast(PIN_BLANK, LOW);
	delay(250);
}

void loop() {
	while (true) {  // Так быстрее
		switch (CMD_SERIAL.read()) {
			case 0: cmdDcdcs(); break;
			case 1: cmdScreen(); break;
			default: break;
		}
		drawColumn();
	}
}
