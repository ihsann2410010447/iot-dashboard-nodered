import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC_SENSOR = "iot/sensor"
TOPIC_KONTROL = "iot/kontrol"  # belum dipakai; disiapkan untuk menerima perintah
INTERVAL = 3  # detik

# Kompatibel dengan paho-mqtt 1.x dan 2.x
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "ESP32-Simulator")
except AttributeError:
    client = mqtt.Client("ESP32-Simulator")

client.connect(BROKER, PORT, 60)
client.loop_start()

print("ESP32 Simulator berjalan... Ctrl+C untuk stop")

try:
    while True:
        data = {
            "suhu": round(random.uniform(25, 32), 1),
            "kelembaban": round(random.uniform(55, 80), 1),
            "timestamp": datetime.now().isoformat(),
        }
        client.publish(TOPIC_SENSOR, json.dumps(data))
        print(f"→ Publish: {data}")
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    print("\nBerhenti.")
finally:
    client.loop_stop()
    client.disconnect()