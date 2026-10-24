// Define the hardware pins
#define PIN_BTN_LEFT 5
#define PIN_BTN_RIGHT 4
#define PIN_BTN_MIDDLE 6

bool lastBtnL = HIGH;
bool lastBtnR = HIGH;
bool lastBtnM = HIGH;

// Variables for double-click timing
unsigned long lastMidPressTime = 0;
int midClickCount = 0;
bool midTimerActive = false;
const int doubleClickDelay = 400; // 400ms window to register a double-click

void setup() {
  Serial.begin(9600);
  pinMode(PIN_BTN_LEFT, INPUT_PULLUP);
  pinMode(PIN_BTN_RIGHT, INPUT_PULLUP);
  pinMode(PIN_BTN_MIDDLE, INPUT_PULLUP);
}

void loop() {
  bool currBtnL = digitalRead(PIN_BTN_LEFT);
  bool currBtnR = digitalRead(PIN_BTN_RIGHT);
  bool currBtnM = digitalRead(PIN_BTN_MIDDLE);

  // LEFT BUTTON: Single Click = Scroll Up
  if (currBtnL == LOW && lastBtnL == HIGH) {
    Serial.println("Scrolled UP");
    delay(50); 
  }

  // RIGHT BUTTON: Single Click = Scroll Down
  if (currBtnR == LOW && lastBtnR == HIGH) {
    Serial.println("Scrolled DOWN");
    delay(50);
  }

  // MIDDLE BUTTON: Double-Click Logic
  if (currBtnM == LOW && lastBtnM == HIGH) {
    midClickCount++;
    lastMidPressTime = millis();
    midTimerActive = true;
    delay(50); // debounce
  }

  if (midTimerActive && (millis() - lastMidPressTime > doubleClickDelay)) {
    if (midClickCount == 1) {
      Serial.println("Standard Left Click"); // Acts as Back/Cancel
    } else if (midClickCount >= 2) {
      Serial.println("EXECUTE");
    }
    midClickCount = 0;
    midTimerActive = false;
  }

  lastBtnL = currBtnL;
  lastBtnR = currBtnR;
  lastBtnM = currBtnM;
}
