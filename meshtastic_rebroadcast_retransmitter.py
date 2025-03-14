import serial
import json
import logging
from cryptography.fernet import Fernet
import meshtastic

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file="meshtastic_rebroadcast_config.json"):
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Config file '{config_file}' not found.")
        return None

config = load_config()
if not config:
    exit(1)

try:
    ser_rx = serial.Serial(config["serial"]["rx_port"], config["serial"]["baudrate"])
except serial.SerialException as e:
    logging.error(f"Serial port error: {e}")
    exit(1)

fernet = Fernet(config["encryption"]["key"].encode())

def process_433_packet():
    try:
        received_data = ser_rx.readline().decode().strip()
        encrypted_data = fernet.encrypt(received_data.encode())
        send_to_meshtastic(encrypted_data)

    except Exception as e:
        logging.error(f"433 packet processing error: {e}")

def send_to_meshtastic(data):
    try:
        interface = meshtastic.SerialInterface()
        interface.sendText(data.decode())
        interface.close()
    except Exception as e:
        logging.error(f"Meshtastic send error: {e}")

while True:
    process_433_packet()
