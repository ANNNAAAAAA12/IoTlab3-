# Laboratorio 3: MQTT hacia Azure IoT Central
**Asignatura:** IoT 
**Institución:** Universidad Autónoma de Bucaramanga (UNAB)  
**Repositorio:** `https://github.com/ANNNAAAAAA12/IoTlab3-.git`  

---

## Descripción del Proyecto

Este proyecto demuestra la implementación y comparación de **tres flujos de telemetría independientes y concurrentes** hacia **Azure IoT Central** mediante el protocolo **MQTTS (puerto 8883 / TLS 1.2)**. Cada dispositivo transmite en tiempo real las tres variables obligatorias del sistema: `temperatura`, `humedad` y `voltaje`.

---

## Estructura del Repositorio

```text
.
├── sdk_python.py       # Camino 1: Transmisión con el SDK oficial (azure-iot-device)
├── mqtt_explicit.py   # Camino 2: Cliente MQTT desnudo (paho-mqtt + DPS + SAS Token)
├── wokwi_main.py      # Camino 3: Firmware en C++/Arduino para ESP32 (Wokwi)
├── README.md          # Documentación general y guía de uso
└── evidencias/        # Capturas de pantalla de validación y logs de ejecución
