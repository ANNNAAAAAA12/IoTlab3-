import asyncio
import random
import json
from azure.iot.device.aio import ProvisioningDeviceClient, IoTHubDeviceClient

SCOPE_ID = "0ne010B81EB"
DEVICE_ID = "17ztq5dykcx"
DEVICE_KEY = "YphNrYx3fjPmdg49CpV6iiODIkCjcUrzTYyd9FrWXtk="
PROVISIONING_HOST = "global.azure-devices-provisioning.net"

async def main():
    print(f"[SDK PYTHON] Aprovisionando dispositivo {DEVICE_ID} vía DPS...")
    
    provisioning_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=PROVISIONING_HOST,
        registration_id=DEVICE_ID,
        id_scope=SCOPE_ID,
        symmetric_key=DEVICE_KEY
    )

    results = await provisioning_client.register()

    if results.status == "assigned":
        print(f"-> ¡Aprovisionamiento Exitoso! Hub asignado: {results.registration_state.assigned_hub}")

        device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=DEVICE_KEY,
            hostname=results.registration_state.assigned_hub,
            device_id=DEVICE_ID,
        )

        await device_client.connect()
        print("\n--- [CAMINO 1: SDK AZURE] CONECTADO Y PUBLICANDO ---")

        while True:
            telemetria = {
                "temperatura": round(random.uniform(20.0, 26.0), 1),
                "humedad": round(random.uniform(50.0, 65.0), 1),
                "voltaje": round(random.uniform(3.1, 3.3), 2)
            }
            
            await device_client.send_message(json.dumps(telemetria))
            print(f"-> [SDK Python - {DEVICE_ID}] Telemetría enviada: {telemetria}")
            await asyncio.sleep(10)
    else:
        print(f"Error en DPS: {results.status}")

if __name__ == "__main__":
    asyncio.run(main())
