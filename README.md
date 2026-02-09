# OpenFMB Python Client

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-stable-active)

**Librería cliente oficial para la interacción con la API de OpenFMB en entornos de microrredes.**

Esta librería abstrae la complejidad de las comunicaciones HTTP para ingenieros de control y científicos de datos. Proporciona una interfaz robusta, tipada y síncrona para la adquisición de telemetría en tiempo real y la extracción de históricos para análisis predictivo.

Diseñada para integrarse en lazos de control, scripts de automatización y notebooks de Jupyter.

## 📦 Instalación

La librería se instala directamente desde el repositorio de GitHub utilizando `pip`. Se recomienda el uso de entornos virtuales (`venv` o `conda`).

```bash
pip install git+https://github.com/perseo-openfmb/openfmb-client.git

## 📋 Requisitos

Si prefieres instalar las dependencias manualmente o configurar un entorno de desarrollo, este es el contenido sugerido para el archivo `requirements.txt`.

Incluye `pandas` dado que es altamente recomendado para el análisis de los datos históricos.

```text
certifi==2026.1.4
charset-normalizer==3.4.4
idna==3.11
numpy==2.2.6
openfmb-client @ git+https://github.com/perseo-openfmb/openfmb-client.git@99278713593a83b2d543bcd69ce4d7590baf8896
pandas==2.3.3
pymodbus==3.7.4
python-dateutil==2.9.0.post0
pytz==2025.2
requests==2.32.5
six==1.17.0
tzdata==2025.3
urllib3==2.6.3

## 💡 Ejemplo Completo de Uso

El siguiente script muestra cómo inicializar el cliente, verificar la conexión y obtener tanto datos en tiempo real como históricos.

```python
from openfmb_client.client import OpenFMBClient, OpenFMBError
from datetime import datetime, timedelta

# 1. Configuración e Inicialización
# Nota: Reemplaza la URL con la dirección de tu API
client = OpenFMBClient(base_url="[http://172.28.16.179:8000/](http://172.28.16.179:8000/)")

# 2. Verificar conexión (Buena práctica antes de iniciar lazos de control)
if not client.check_health():
    print("❌ El sistema está caído (System is down)")
    exit(1)

# 3. Obtención de Datos
try:
    # --- Ejemplo A: Chequeo de control en tiempo real ---
    target_uuid = "00000001-0001-0020-0000-000000000001" # UUID del dispositivo objetivo
    
    last_state = client.get_last_state(target_uuid)
    voltage = last_state['data'].get('voltage', 'N/A')
    print(f"⚡ Voltaje Actual: {voltage}")
    
    # --- Ejemplo B: Análisis de históricos ---
    history = client.get_historical_data(
        target_uuid, 
        limit=50,
        start=datetime.now() - timedelta(hours=1)
    )
    
    print(f"📊 Registros recuperados: {len(history)}")
    if history:
        print(f"   Fecha del primer dato: {history[0]['timestamp']}")

    # --- Ejemplo C: Listar dispositivos disponibles ---
    # Asegúrate de que tu API soporte este endpoint
    devices = client.list_devices()
    print(f"📡 Dispositivos en red: {devices}")

except OpenFMBError as e:
    print(f"⚠️ Lógica de control abortada: {e}")
```
