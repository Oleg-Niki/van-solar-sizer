from django import forms
from django.forms import formset_factory

class SystemDesignForm(forms.Form):
    latitude = forms.DecimalField(
        max_digits=8, decimal_places=5, label="Latitude"
    )
    longitude = forms.DecimalField(
        max_digits=8, decimal_places=5, label="Longitude"
    )
    panel_watts_input = forms.IntegerField(
        label="Panel wattage (W)",
        help_text="Nominal rating of your solar panel"
    )
    battery_voltage = forms.DecimalField(
        max_digits=4, decimal_places=1,
        initial=12.0, label="Battery voltage (V)"
    )
    depth_of_discharge = forms.DecimalField(
        max_digits=3, decimal_places=2,
        initial=0.5, label="Max depth of discharge (fraction)"
    )

class ApplianceForm(forms.Form):
    name = forms.CharField(max_length=100)
    watts = forms.FloatField(label="Power (W)")
    hours = forms.FloatField(label="Usage per day (h)")

# create a small formset of 3 appliances by default
ApplianceFormSet = formset_factory(ApplianceForm, extra=3)
