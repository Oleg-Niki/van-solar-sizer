# aws/fetch_irradiance.py
import os, json, requests
from dotenv import load_dotenv

load_dotenv()

PVWATTS_KEY = os.getenv("PVWATTS_API_KEY")
# Switch to the V8 endpoint:
PVWATTS_URL = "https://developer.nrel.gov/api/pvwatts/v8.json"

def handler(event, context):
    qs = event.get("queryStringParameters", {}) or {}
    lat = float(qs.get("lat", 0))
    lon = float(qs.get("lon", 0))

    params = {
        "api_key": PVWATTS_KEY,
        "lat": lat,
        "lon": lon,
        "system_capacity": 1,   # normalized to 1 kW
        # Required V8 parameters with sensible defaults:
        "tilt": lat,            # panel tilt = latitude
        "azimuth": 180,         # panels facing south
        "array_type": 1,        # 1 = fixed (roof mount)
        "module_type": 0,       # 0 = standard module
        "losses": 14            # 14% system losses
    }

    resp = requests.get(PVWATTS_URL, params=params)
    data = resp.json()

    # If there are API errors, bubble them up:
    if data.get("errors"):
        return {"statusCode": 500, "body": json.dumps({"error": data})}

    # V8 returns 'solrad_monthly' (an array) and 'solrad_annual'
    sun_hours = data["outputs"]["solrad_annual"] / 365.0
    return {"statusCode": 200, "body": json.dumps({"sun_hours": sun_hours})}
