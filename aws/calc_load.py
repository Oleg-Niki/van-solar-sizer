# aws/calc_load.py
import json

def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    apps = body.get("appliances", [])
    total_wh = sum(a["watts"] * a["hours"] for a in apps)
    return {"statusCode": 200, "body": json.dumps({"daily_load_wh": total_wh})}
