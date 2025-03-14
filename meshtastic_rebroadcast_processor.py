import paho.mqtt.client as mqtt
import serial
import json
import logging
import time
from cryptography.fernet import Fernet

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

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    logging.info(f"MQTT Connected with result code {rc}")
    client.subscribe(config["mqtt"]["topic"])

def on_message(client, userdata, msg):
    try:
        process_meshtastic_packet(msg.payload)
    except Exception as e:
        logging.error(f"Error processing message: {e}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(config["mqtt"]["broker"], config["mqtt"]["port"], 60)

try:
    ser_tx = serial.Serial(config["serial"]["tx_port"], config["serial"]["baudrate"])
except serial.SerialException as e:
    logging.error(f"Serial port error: {e}")
    exit(1)

fernet = Fernet(config["encryption"]["key"].encode())

def process_meshtastic_packet(payload):
    try:
        decrypted_payload = fernet.decrypt(payload).decode()
        filtered_data = filter_meshtastic_data(decrypted_payload)
        four33_packet = create_four33_packet(filtered_data)

        if time.time() - last_send_time < config["rate_limit"]["interval"]:
            logging.warning("Rate limit exceeded. Packet dropped.")
            return

        ser_tx.write(four33_packet.encode())
        global last_send_time
        last_send_time = time.time()

    except Exception as e:
        logging.error(f"Packet processing error: {e}")

def filter_meshtastic_data(data):
    return data #Modify to filter as needed

def create_four33_packet(data):
    return data #Modify to create the 433 packet format.

last_send_time = 0

mqtt_client.loop_forever()
