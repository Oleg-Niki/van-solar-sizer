# sizing/views.py
import json
from django.shortcuts import render
from .forms import SystemDesignForm, ApplianceFormSet
from .models import SystemDesign, Calculation

from aws.fetch_irradiance import handler as fetch_irrad
from aws.calc_load        import handler as calc_load
from aws.size_system      import handler as size_sys

def design_request(request):
    sun_hours = daily_load_wh = panel_w = battery_ah = None
    submitted = False

    if request.method == 'POST':
        form = SystemDesignForm(request.POST)
        fs   = ApplianceFormSet(request.POST)

        if form.is_valid() and fs.is_valid():
            submitted = True
            data = form.cleaned_data
            apps = [
                cd for cd in (f.cleaned_data for f in fs)
                if cd.get("watts") is not None and cd.get("hours") is not None
]

            # 1) Sun hours
            evt1 = {"queryStringParameters":{
                "lat": str(data["latitude"]),
                "lon": str(data["longitude"])
            }}
            resp1    = fetch_irrad(evt1, None)
            sun_hours = json.loads(resp1["body"])["sun_hours"]

            # 2) Daily load
            evt2        = {"body": json.dumps({"appliances": apps})}
            resp2       = calc_load(evt2, None)
            daily_load_wh = json.loads(resp2["body"])["daily_load_wh"]

            # 3) Sizing
            evt3      = {"body": json.dumps({
                "sun_hours":      sun_hours,
                "daily_load_wh":  daily_load_wh,
                "panel_eff":      0.8,
                "bat_v":          float(data["battery_voltage"]),
                "dod":            float(data["depth_of_discharge"])
            })}
            resp3     = size_sys(evt3, None)
            sizing    = json.loads(resp3["body"])
            panel_w    = sizing["panel_w"]
            battery_ah = sizing["battery_ah"]
            
            if submitted:
                sd = SystemDesign.objects.create(
                    latitude=data['latitude'],
                    longitude=data['longitude'],
                    panel_watts=panel_w,
                    battery_ah=battery_ah
                )
                Calculation.objects.create(
                    system_design=sd,
                    daily_load_wh=daily_load_wh,
                    sun_hours=sun_hours,
                    panel_w=panel_w,
                    battery_ah=battery_ah
                )

    else:
        form = SystemDesignForm()
        fs   = ApplianceFormSet()

    return render(request, 'sizing/design_form.html', {
        'design_form':    form,
        'appliance_formset': fs,
        'submitted':      submitted,
        'sun_hours':      sun_hours,
        'daily_load_wh':  daily_load_wh,
        'panel_w':        panel_w,
        'battery_ah':     battery_ah,
    })
