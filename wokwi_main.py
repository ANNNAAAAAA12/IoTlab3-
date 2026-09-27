import asyncio
import random
import json
from azure.iot.device.aio import IoTHubDeviceClient

DEVICE_ID = "esp32-wokwi-01"
HOSTNAME = "iotc-e438ddb4-2a84-4ea7-b296-bcff99643b3d.azure-devices.net"
KEY = "IRrqiazJyBWP0HdAAHOZV3W1EImTudCY6IS2478hbvI="

async def main():
    print(f"[WOKWI NODE] Iniciando para {DEVICE_ID}...")
    device_client = IoTHubDeviceClient.create_from_symmetric_key(
        symmetric_key=KEY,
        hostname=HOSTNAME,
        device_id=DEVICE_ID
    )

    await device_client.connect()
    print("\n--- [CAMINO 3: WOKWI ESP32 NODE] CONECTADO Y PUBLICANDO ---")

    while True:
        telemetria = {
            "temperatura": round(random.uniform(20.0, 26.0), 1),
            "humedad": round(random.uniform(50.0, 65.0), 1),
            "voltaje": round(random.uniform(3.1, 3.3), 2)
        }

        await device_client.send_message(json.dumps(telemetria))
        print(f"-> [Wokwi ESP32 - {DEVICE_ID}] Telemetría enviada: {telemetria}")
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
