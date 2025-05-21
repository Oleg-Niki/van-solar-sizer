# aws/size_system.py
import json, math

def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    sun = body["sun_hours"]
    load = body["daily_load_wh"]
    eff = body.get("panel_eff", 0.8)
    bat_v = body.get("bat_v", 12)
    dod   = body.get("dod", 0.5)

#MAKE SURE THIS FORMULA CORRECT (BUT BEFORE CHECK IN FETCH_IRRADIANCE):
    panel_w    = math.ceil(load / (sun * eff))
    battery_ah = math.ceil((load / bat_v) / dod)

    return {
        "statusCode": 200,
        "body": json.dumps({"panel_w": panel_w, "battery_ah": battery_ah})
    }
