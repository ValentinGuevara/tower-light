#include <SoftwareSerial.h>
#include <Grove_LED_Bar.h>

SoftwareSerial loraSerial(2, 3); // RX, TX sur D2, D3

Grove_LED_Bar bar(9, 8, 0);  // Clock pin, Data pin, Orientation

void setup() {
  Serial.begin(9600);
  loraSerial.begin(9600);

  bar.begin();

  // Configuration P2P
  loraSerial.println("AT+MODE=TEST");
  delay(200);
  loraSerial.println("AT+TEST=RFCFG,868000000,7,125,5,15,14");
  delay(200);
  
  // Démarre l’écoute
  loraSerial.println("AT+TEST=RXLRPKT");

  Serial.println("Récepteur LoRa prêt.");
}

void loop() {
  if (loraSerial.available()) {
    String hexMsg = loraSerial.readStringUntil('\n');
    hexMsg.trim();
    // Is hello hexadecimal in message
    if(hexMsg.indexOf("48656C6C6F") != -1) {
      bar.setLevel(10);
      delay(1000);            // Allumée 500 ms
      bar.setLevel(0);
      Serial.println("TOWER_ON");
    }
  } else {
    bar.setLevel(0);
  }
  delay(20);
}
