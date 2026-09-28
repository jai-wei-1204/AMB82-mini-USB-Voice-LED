/* AMB82-mini USB serial LED controller. Commands: on-left, on-right, blink-left:N, blink-right:N, status */
#include <Arduino.h>

const int BLUE_LED = LED_B;   // AMB82-mini D23, HIGH = on
const int GREEN_LED = LED_G;  // AMB82-mini D24, HIGH = on
String ledState = "off";
String blinkSide;
int blinkTransitions = 0;
bool blinkOn = false;
unsigned long nextBlinkAt = 0;
const unsigned long BLINK_INTERVAL_MS = 350;

void sendState() { Serial.print("STATE:"); Serial.println(ledState); }
void setLeds(bool blue, bool green) { digitalWrite(BLUE_LED, blue ? HIGH : LOW); digitalWrite(GREEN_LED, green ? HIGH : LOW); }
void cancelBlink() { blinkTransitions = 0; blinkOn = false; }

void startBlink(const String &side, int count) {
  if (count < 1 || count > 20) { Serial.println("ERROR:count must be 1..20"); return; }
  cancelBlink();
  blinkSide = side;
  blinkTransitions = count * 2;  // Each blink is one ON and one OFF transition.
  nextBlinkAt = millis();
  ledState = "blinking-" + side + ":" + String(count);
  sendState();
}

void turnOn(const String &side) {
  cancelBlink();
  setLeds(side == "left", side == "right");
  ledState = side;
  sendState();
}

void applyCommand(String command) {
  command.trim(); command.toLowerCase();
  if (command == "status") { sendState(); return; }
  if (command == "on-left") turnOn("left");
  else if (command == "on-right") turnOn("right");
  else if (command.startsWith("blink-left:")) startBlink("left", command.substring(11).toInt());
  else if (command.startsWith("blink-right:")) startBlink("right", command.substring(12).toInt());
  else if (command.length()) Serial.println("ERROR:invalid command");
}

void serviceBlink() {
  if (!blinkTransitions || millis() < nextBlinkAt) return;
  blinkOn = !blinkOn;
  setLeds(blinkSide == "left" && blinkOn, blinkSide == "right" && blinkOn);
  --blinkTransitions;
  nextBlinkAt = millis() + BLINK_INTERVAL_MS;
  if (!blinkTransitions) {
    // The last transition is OFF, so the board's confirmed final state is off.
    ledState = "off";
    sendState();
  }
}

void setup() {
  Serial.begin(115200); delay(1500);
  pinMode(BLUE_LED, OUTPUT); pinMode(GREEN_LED, OUTPUT); setLeds(false, false);
  Serial.println("AMB82_USB_VOICE_LED_READY"); sendState();
}

void loop() {
  static String input;
  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n' || c == '\r') { applyCommand(input); input = ""; }
    else if (input.length() < 32) input += c;
  }
  serviceBlink();
}
