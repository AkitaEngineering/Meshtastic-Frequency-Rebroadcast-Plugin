#include <RH_RF95.h>
#include <SPI.h>

#define RFM95_CS 10
#define RFM95_RST 9
#define RFM95_INT 2

RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup() {
  Serial.begin(9600);
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  delay(100);
  digitalWrite(RFM95_RST, LOW);
  delay(100);
  digitalWrite(RFM95_RST, HIGH);
  delay(100);

  if (!rf95.init()) {
    Serial.println("RFM95 initialization failed");
    while (1);
  }
  rf95.setFrequency(433.0);
  rf95.setRxGain(RH_RF95_RXGAIN_AUTO);
}

void loop() {
    if (rf95.available()) {
        uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
        uint8_t len = sizeof(buf);
        if (rf95.recv(buf, &len)) {
            Serial.write(buf, len);
            Serial.println();
        }
    }
}
