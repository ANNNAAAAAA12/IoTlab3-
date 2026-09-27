import asyncio
import time
import json
import random
import ssl
import base64
import hmac
import hashlib
import urllib.parse
from azure.iot.device.aio import ProvisioningDeviceClient
import paho.mqtt.client as mqtt

SCOPE_ID = "0ne010B81EB"
DEVICE_ID = "26a1012qbj0"
DEVICE_KEY = "d6ODIUmamaN88mljj0DeC605Rvho65ymOTrzR3CAhkg="
PROVISIONING_HOST = "global.azure-devices-provisioning.net"

async def get_assigned_hub():
    print(f"[DPS] Aprovisionando {DEVICE_ID} para obtener el Hub asignado...")
    provisioning_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=PROVISIONING_HOST,
        registration_id=DEVICE_ID,
        id_scope=SCOPE_ID,
        symmetric_key=DEVICE_KEY
    )
    results = await provisioning_client.register()
    if results.status == "assigned":
        hub = results.registration_state.assigned_hub
        print(f"-> ¡DPS Éxito! Hub asignado: {hub}")
        return hub
    else:
        raise Exception(f"Fallo en DPS: {results.status}")

def generate_sas_token(uri, key, expiry=3600):
    ttl = int(time.time()) + expiry
    sign_key = base64.b64decode(key)
    to_sign = f"{urllib.parse.quote_plus(uri)}\n{ttl}".encode('utf-8')
    raw_hmac = hmac.HMAC(sign_key, to_sign, hashlib.sha256).digest()
    signature = urllib.parse.quote_plus(base64.b64encode(raw_hmac))
    return f"SharedAccessSignature sr={urllib.parse.quote_plus(uri)}&sig={signature}&se={ttl}"

def run_mqtt(hostname):
    username = f"{hostname}/{DEVICE_ID}/?api-version=2021-04-12"
    password = generate_sas_token(f"{hostname}/devices/{DEVICE_ID}", DEVICE_KEY)

    client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311)
    client.username_pw_set(username=username, password=password)
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"\n--- [CAMINO 2: MQTT EXPLÍCITO] CONECTADO EXITOSAMENTE (rc={rc}) ---")
        else:
            print(f"\n--- [CAMINO 2: MQTT EXPLÍCITO] ERROR DE CONEXIÓN (rc={rc}) ---")

    client.on_connect = on_connect
    client.connect(hostname, 8883, keepalive=60)
    client.loop_start()

    time.sleep(2)
    try:
        while True:
            telemetria = {
                "temperatura": round(random.uniform(20.0, 26.0), 1),
                "humedad": round(random.uniform(50.0, 65.0), 1),
                "voltaje": round(random.uniform(3.1, 3.3), 2)
            }
            payload = json.dumps(telemetria)
            topic = f"devices/{DEVICE_ID}/messages/events/"
            info = client.publish(topic, payload, qos=1)
            print(f"-> [MQTT Explícito - {DEVICE_ID}] Telemetría enviada (MID: {info.mid}): {payload}")
            time.sleep(10)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    assigned_hub = asyncio.run(get_assigned_hub())
    run_mqtt(assigned_hub)
