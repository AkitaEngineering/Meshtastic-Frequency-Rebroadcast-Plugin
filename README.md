# Meshtastic Frequency Rebroadcast Plugin

This project implements a bridge between a 915 MHz Meshtastic network and a 433 MHz amateur radio network. It allows for the forwarding of Meshtastic packets to a long-range 433 MHz connection and back, enabling communication over greater distances.

## Overview

The system consists of the following components:

1.  **915 MHz Meshtastic Node (MQTT Publisher):** Receives Meshtastic packets and publishes them to an MQTT broker.
2.  **Packet Processing (meshtastic_rebroadcast_processor.py):** Subscribes to the MQTT broker, filters (if needed) and converts Meshtastic packets, and sends them to a 433 MHz transmitter via serial.
3.  **433 MHz Transmission (meshtastic_rebroadcast_433_tx.ino):** Receives serial data and transmits it using a 433 MHz radio.
4.  **433 MHz Reception (meshtastic_rebroadcast_433_rx.ino):** Receives 433 MHz transmissions and sends the data via serial.
5.  **Packet Re-encryption and 915 MHz Re-transmission (meshtastic_rebroadcast_retransmitter.py and Meshtastic):** Receives the 433Mhz data, re-encrypts it, and re-transmits it on the 915 Mhz Meshtastic network.

## Requirements

* **Hardware:**
    * 915 MHz Meshtastic nodes
    * 433 MHz radio transceivers (e.g., RFM95)
    * Microcontrollers (e.g., Arduino)
    * Computer or Raspberry Pi
    * Antennas appropriate for each frequency.
* **Software:**
    * Python 3.x
    * Arduino IDE
    * MQTT broker
    * Python cryptography library.
    * Serial communication libraries.
    * Meshtastic Python API.
* **Knowledge:**
    * Meshtastic
    * MQTT
    * Serial communication
    * Amateur radio principles
    * Basic Python and C++ coding knowledge.

## Installation

1.  **Set up Meshtastic:** Configure your 915 MHz Meshtastic nodes and enable MQTT publishing.
2.  **Install Python dependencies:**

    ```bash
    pip install paho-mqtt pyserial cryptography meshtastic
    ```

3.  **Install Arduino libraries:**
    * Install the `RH_RF95` library via the Arduino Library Manager.
    * Install the `SPI` library (usually included).
4.  **Configure `meshtastic_rebroadcast_config.json`:**
    * Create a `meshtastic_rebroadcast_config.json` file with your MQTT broker details, serial port settings, radio frequencies, and encryption keys.
    * Example `meshtastic_rebroadcast_config.json`:

    ```json
    {
      "mqtt": {
        "broker": "your_mqtt_broker",
        "port": 1883,
        "topic": "meshtastic/#"
      },
      "serial": {
        "tx_port": "/dev/ttyUSB0",
        "rx_port": "/dev/ttyUSB1",
        "baudrate": 9600
      },
      "radio": {
        "frequency": 433.0,
        "tx_power": 20
      },
      "encryption": {
        "key": "Your32ByteEncryptionKeyHere"
      },
      "rate_limit": {
        "interval": 1
      }
    }
    ```

    * **Important:** Replace `"Your32ByteEncryptionKeyHere"` with a secure 32-byte encryption key.
5.  **Upload Arduino code:**
    * Upload `meshtastic_rebroadcast_433_tx.ino` to your 433 MHz transmitter microcontroller.
    * Upload `meshtastic_rebroadcast_433_rx.ino` to your 433 MHz receiver microcontroller.
    * Adjust the frequency and power settings in the Arduino code to match your configuration.
6.  **Run the Python scripts:**

    ```bash
    python meshtastic_rebroadcast_processor.py
    python meshtastic_rebroadcast_retransmitter.py
    ```

## Usage

1.  Ensure all hardware is powered on and connected.
2.  Start the Python scripts.
3.  Send Meshtastic messages on the 915 MHz network.
4.  The messages will be forwarded to the 433 MHz network and back.

## Important Notes

* **Legal Compliance:** Ensure your transmissions comply with all applicable amateur radio regulations in your region.
* **Encryption:** Store encryption keys securely.
* **Testing:** Thoroughly test the system before deploying it.
* **Data Handling:** This implementation sends raw string data over the 433Mhz link. For more robust data handling, implement custom protobuf message structures.
* **Antennas:** Antenna selection and placement are critical for long-range communications.
* **Rate Limiting:** Adjust the rate limit in the config file to prevent flooding the 433Mhz network.
* **Serial Port Configuration:** Double check your serial port assignments in the config file.

## Contributing

Contributions are welcome! Please submit pull requests or bug reports.
