#include <SoftwareSerial.h>
#include <ChainableLED.h>

// Grove LoRa (UART) sur D2 (RX) / D3 (TX)
SoftwareSerial loraSerial(2, 3); // RX, TX

// Grove Chainable LED sur D4 (data), D5 (clock)
ChainableLED leds(4, 5, 1); // dataPin, clockPin, nbLEDs

// Grove Dual Button sur D6
const int buttonPin = 6;

void setup() {
  // Initialisation
  pinMode(buttonPin, INPUT);
  loraSerial.begin(9600);
  Serial.begin(9600);

  leds.setColorRGB(0, 0, 0, 0); // éteint la LED au départ

  delay(3000); // Attente que le module soit prêt

  // Configuration P2P
  loraSerial.println("AT+MODE=TEST");
  delay(200);
  loraSerial.println("AT+TEST=RFCFG,868000000,7,125,5,15,14");
  delay(200);
}

void loop() {
  int buttonState = digitalRead(buttonPin) == LOW;

  if (buttonState == HIGH) {
    loraSerial.println("pressed");
    loraSerial.println("AT+TEST=TXLRSTR,\"Hello\"");
    Serial.println("Message envoyé");

    // LED verte
    leds.setColorRGB(0, 0, 255, 0);
  } else {
    // LED éteinte
    leds.setColorRGB(0, 0, 0, 0);
  }

  delay(200); // anti-rebond + éviter le spam LoRa
}
