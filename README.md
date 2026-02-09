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
```

## 📋 Requisitos

Si prefieres instalar las dependencias manualmente o configurar un entorno de desarrollo, este es el contenido sugerido para el archivo `requirements.txt`.

Incluye `pandas` dado que es altamente recomendado para el análisis de los datos históricos.

```text
certifi==2026.1.4
charset-normalizer==3.4.4
idna==3.11
numpy==2.2.6
pandas==2.3.3
pymodbus==3.7.4
python-dateutil==2.9.0.post0
pytz==2025.2
requests==2.32.5
six==1.17.0
tzdata==2025.3
urllib3==2.6.3
```

## 💡 Ejemplo Completo de Uso

El siguiente script muestra cómo inicializar el cliente, verificar la conexión y obtener tanto datos en tiempo real como históricos.

```python
from openfmb_client.client import OpenFMBClient, OpenFMBError

# 1. Initialize
client = OpenFMBClient(base_url="http://localhost:8000/")

# 2. Check connection (Good practice before control loops)
if not client.check_health():
    print("System is down!")
    exit(1)

# 3. Get Data
try:
    # Example: Real-time control check
    target_uuid = "00000001-0001-0020-0000-000000000001" # Replace with real UUID
    last_state = client.get_last_state(target_uuid)
    print(f"Current Voltage: {last_state['data'].get('voltage', 'N/A')}")
    
    # Example: Historical for Analysis
    from datetime import datetime, timedelta
    history = client.get_historical_data(
        target_uuid, 
        limit=50,
        start=datetime.now() - timedelta(hours=1)
    )
    print(f"Retrieved {len(history)} records.")
    print(f"First record timestamp: {history[0]['timestamp'] if history else 'N/A'}")

    # Example: List devices
    devices = client.get_devices()
    print(f"Available devices: {devices}")

except OpenFMBError as e:
    print(f"Control logic aborted: {e}")
```
