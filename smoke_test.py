# smoke_test.py
import os, json
from dotenv import load_dotenv

print("CWD:", os.getcwd())
print("Files here:", os.listdir())

# 1) load .env
load_dotenv()

print("Loaded PVWATTS_API_KEY:", os.getenv("PVWATTS_API_KEY"))

# DEBUG: print what key we actually have
print("Loaded PVWATTS_API_KEY:", os.getenv("PVWATTS_API_KEY"))

# 2) import handlers
from aws.fetch_irradiance import handler as fetch_irrad
from aws.calc_load        import handler as calc_load
from aws.size_system      import handler as size_sys

# 3) test irradiance
evt1 = {"queryStringParameters": {"lat": "37.7749", "lon": "-122.4194"}}
res1 = fetch_irrad(evt1, None)
sun = json.loads(res1["body"])["sun_hours"]
print(f"☀️  Sun hours: {sun:.2f}")

# 4) test load
apps = [
    {"watts": 100, "hours": 2},
    {"watts": 200, "hours": 1},
    {"watts": 15,  "hours": 2},
]
evt2 = {"body": json.dumps({"appliances": apps})}
res2 = calc_load(evt2, None)
load_wh = json.loads(res2["body"])["daily_load_wh"]
print(f"🔋 Daily load (Wh): {load_wh:.1f}")

# 5) test sizing
evt3 = {
    "body": json.dumps({
        "sun_hours": sun,
        "daily_load_wh": load_wh,
        "panel_eff": 0.8,
        "bat_v": 12,
        "dod": 0.5
    })
}
res3 = size_sys(evt3, None)
out = json.loads(res3["body"])
print(f"⚡ Panel W: {out['panel_w']} W, Battery: {out['battery_ah']} Ah")
