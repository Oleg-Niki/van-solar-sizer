# aws/fetch_irradiance.py
import os, json, requests
from dotenv import load_dotenv

load_dotenv()  # so PVWATTS_API_KEY comes from your .env

PVWATTS_KEY = os.getenv("PVWATTS_API_KEY")
PVWATTS_URL = "https://developer.nrel.gov/api/pvwatts/v6.json"

def handler(event, context):
    qs = event.get("queryStringParameters", {})
    lat, lon = qs.get("lat"), qs.get("lon")
    resp = requests.get(PVWATTS_URL, params={
        "api_key": PVWATTS_KEY,
        "lat": lat,
        "lon": lon,
        "system_capacity": 1,  # 1 kW normalized
    })
    data = resp.json()
    sun_hours = data["outputs"]["solrad_annual"] / 365.0
    return {"statusCode": 200, "body": json.dumps({"sun_hours": sun_hours})}
