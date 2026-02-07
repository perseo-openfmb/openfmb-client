# Author: Kevin Martinez
# Refactor and Documentation: Gemini-3.0
# Date: 2026-02-07
# Generate a library for OpenFMB API
# This library will provide functions to interact with the OpenFMB API

import requests
import logging
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from uuid import UUID

# Configuration for logging (User can override this)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OpenFMB-Client")

class OpenFMBError(Exception):
    """Base exception for OpenFMB API errors."""
    pass

class OpenFMBClient:
    """
    A client for interacting with the OpenFMB Async API.
    Designed for control applications requiring historical and real-time data.
    """

    def __init__(self, base_url: str, timeout: int = 5):
        """
        Args:
            base_url (str): The root URL of the API (e.g., 'http://localhost:8000')
            timeout (int): Request timeout in seconds. Critical for control loops
                           to avoid hanging indefinitely.
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        # Optimization: Connection pooling is handled automatically by Session

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Internal method to handle HTTP requests and errors uniformly."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, params=params, timeout=self.timeout)
            response.raise_for_status() # Raises HTTPError for 4xx/5xx codes
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout connecting to {url}")
            raise OpenFMBError(f"Request timed out after {self.timeout}s.")
            
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection failed to {url}")
            raise OpenFMBError("Could not connect to the OpenFMB API.")
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
            raise OpenFMBError(f"API Error: {e.response.status_code}")
            
        except ValueError:
            logger.error("Invalid JSON received")
            raise OpenFMBError("API returned invalid JSON.")

    def get_last_state(self, device_uuid: Union[str, UUID]) -> Dict[str, Any]:
        """
        Retrieves the latest measurement for a specific device.

        Args:
            device_uuid: The unique ID of the device (string or UUID object).

        Returns:
            Dict containing timestamp, uuid, and data payload.
        """
        endpoint = f"/devices/{str(device_uuid)}/last-state"
        data = self._request("GET", endpoint)
        
        # Unpack the specific key as per your API definition
        return data.get("latest_measurement", {})

    def get_historical_data(
        self, 
        device_uuid: Union[str, UUID], 
        limit: int = 100, 
        start: Optional[datetime] = None, 
        end: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves historical data for time-series analysis.

        Args:
            device_uuid: The unique ID of the device.
            limit: Max number of records (1-5000).
            start: Start datetime (inclusive).
            end: End datetime (inclusive).

        Returns:
            List of measurement dictionaries.
        """
        endpoint = f"/devices/{str(device_uuid)}/historical"
        params = {"limit": limit}

        # Handle datetime serialization automatically for the user
        if start:
            params["start"] = start.isoformat()
        if end:
            params["end"] = end.isoformat()

        response = self._request("GET", endpoint, params=params)
        return response.get("measurements", [])

    def check_health(self) -> bool:
        """Verifies if the API and Database are responsive."""
        try:
            res = self._request("GET", "/test-db")
            return "database_version" in res
        except OpenFMBError:
            return False

# -----------------------------------------------------------------------------
# Example Usage (Documentation for the user)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # 1. Initialize
    client = OpenFMBClient(base_url="http://172.28.16.179:8000/")

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

    except OpenFMBError as e:
        print(f"Control logic aborted: {e}")
