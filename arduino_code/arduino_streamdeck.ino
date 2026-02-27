// Arduino code to read 4 buttons and send press/release signals over Serial.
// Designed for use with the Raspberry Pi Stream Deck Python script.

// Define the pins for the buttons (connected to ground when pressed)
const int button1Pin = 2; // Sends U/u
const int button2Pin = 3; // Sends L/l
const int button3Pin = 4; // Sends D/d
const int button4Pin = 5; // Sends R/r

// Variables to store the current and previous state of each button
int button1State = HIGH;
int button2State = HIGH;
int button3State = HIGH;
int button4State = HIGH;

int lastButton1State = HIGH;
int lastButton2State = HIGH;
int lastButton3State = HIGH;
int lastButton4State = HIGH;

void setup() {
  // Initialize Serial communication at 9600 baud rate
  Serial.begin(9600);

  // Initialize the button pins as inputs with internal pull-up resistors enabled
  // Pin reads HIGH when button is open, LOW when pressed (connected to GND)
  pinMode(button1Pin, INPUT_PULLUP);
  pinMode(button2Pin, INPUT_PULLUP);
  pinMode(button3Pin, INPUT_PULLUP);
  pinMode(button4Pin, INPUT_PULLUP);

  // Optional delay to ensure Serial is ready if needed by receiving device
  delay(100);
  // Serial.println("Arduino Ready"); // Optional debug message
}

void loop() {
  // Read the current state of each button
  button1State = digitalRead(button1Pin);
  button2State = digitalRead(button2Pin);
  button3State = digitalRead(button3Pin);
  button4State = digitalRead(button4Pin);

  // --- Check Button 1 (U/u) ---
  if (button1State != lastButton1State) {
    if (button1State == LOW) { // Pressed
      Serial.print('U');
    } else { // Released
      Serial.print('u');
    }
    delay(10); // Small delay for debounce/stability
  }

  // --- Check Button 2 (L/l) ---
  if (button2State != lastButton2State) {
    if (button2State == LOW) { // Pressed
      Serial.print('L');
    } else { // Released
      Serial.print('l');
    }
    delay(10);
  }

  // --- Check Button 3 (D/d) ---
  if (button3State != lastButton3State) {
    if (button3State == LOW) { // Pressed
      Serial.print('D');
    } else { // Released
      Serial.print('d');
    }
    delay(10);
  }

  // --- Check Button 4 (R/r) ---
  if (button4State != lastButton4State) {
    if (button4State == LOW) { // Pressed
      Serial.print('R');
    } else { // Released
      Serial.print('r');
    }
    delay(10);
  }

  // Update the last known state for each button
  lastButton1State = button1State;
  lastButton2State = button2State;
  lastButton3State = button3State;
  lastButton4State = button4State;

  // No main loop delay needed as button state change logic limits serial traffic
}
